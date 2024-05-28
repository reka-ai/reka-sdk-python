"""Chat-related server interactions (including VLM chat)"""

from __future__ import annotations

import base64
from typing import Any, Dict, List, Literal, Optional, TypedDict, cast

import reka.v2.api.driver as driver
from reka.v2.errors import InvalidConversationError


class ModelTurn(TypedDict):
    """A turn in a conversation output by the model."""

    type: Literal["model"]
    text: str


MediaType = Literal["image", "video", "audio"]


class HumanTurn(TypedDict, total=False):
    """A turn in a conversation authored by the human user."""

    text: str
    type: Literal["human"]

    # Optional media (image, video, or audio), can be set only for the first turn in the conversation.
    media_url: Optional[str]


def chat(
    human: Optional[str] = None,
    media_url: Optional[str] = None,
    media_filename: Optional[str] = None,
    conversation_history: Optional[List[HumanTurn | ModelTurn]] = None,
    retrieval_dataset: Optional[str] = None,
    model_name: str = "reka-flash",
    request_output_len: Optional[int] = None,
    temperature: Optional[float] = None,
    random_seed: Optional[int] = None,
    runtime_top_k: Optional[int] = None,
    runtime_top_p: Optional[float] = None,
    frequency_penalty: Optional[float] = None,
    presence_penalty: Optional[float] = None,
    length_penalty: Optional[float] = None,
    stop_words: Optional[List[str]] = None,
    extra_request_args: Optional[Dict[str, Any]] = None,
) -> ModelTurn:
    """Chat endpoint.

    Example usage:
    ```python
    import reka

    reka.API_KEY = "APIKEY"

    conversation_history = [
        {"type": "human", "text": "Hi, my name is John."},
        {"type": "model", "text": "Hi, I'm Reka's assistant."},
    ]
    response = reka.chat(
        human="What was my name?",
        conversation_history=conversation_history,
    )
    print(response) # {"type": "model", "text": "Your name is John.\\n\\n"}
    ```

    Args:
        human: latest message from human, this is optional if using `conversation_history` instead.
        media_url: an optional URL for the media (image, video, or audio) to chat about. This may only be set for the
            first turn (when conversation_history is empty). You can also send base64 media in the format data:image/{image_format};base64,{base64_image}
        media_filename: alternative to the `media_url` parameter, the location of a local file.``
        conversation_history: list of dicts, where each dict has a key "type"
            indicating the speaker, either "human" or "model", and a key "text"
            containing the message from the speaker. If not set, will default to
            an empty history. The first turn may also have "media_url" set.
        retrieval_dataset: Previously uploaded dataset to do retrieval on.
        model_name: Name of model. You can check available models  with `reka.get_models()`. Defaults to flash.
        request_output_len: Completion length in tokens.
        temperature: Softmax temperature, higher is more diverse.
        random_seed: Seed to obtain different results.
        runtime_top_k: Keep only k top tokens when sampling.
        runtime_top_p: Keep only top p quantile when sampling.
        frequency_penalty: Penalize repetitions. 0 means no penalty.
        presence_penalty: Penalize repetitions. 0 means no penalty.
        length_penalty: Penalize short answers. 1 means no penalty.
        stop_words: Optional list of words on which to stop generation.
        extra_request_args: Optional extra arguments to include in the request, useful for experimental API features.

    Raises:
        InvalidConversationError: if the conversation history is not valid.

    Returns:
        ModelTurn: A dict containing `{"type": "model", "text": <response from the model>}`. If `retrieval_dataset` is
            set, then this will also contain `"retrieved_chunks"`.

    """
    defined_hturn: Optional[HumanTurn] = None
    if human is not None:
        defined_hturn = {"type": "human", "text": human}
        if media_url is not None and media_filename is not None:
            raise ValueError("Must specify either `media_url` or `media_filename`")

        if media_url is not None:
            defined_hturn["media_url"] = media_url
        elif media_filename is not None:
            defined_hturn["media_url"] = _local_file_to_media_url(media_filename)

    full_conv = (conversation_history or []) + (
        [defined_hturn] if defined_hturn else []
    )
    _check_conversation_history(full_conv)

    json_dict = {
        key: value
        for key, value in [
            ("conversation_history", full_conv),
            ("retrieval_dataset", retrieval_dataset),
            ("model_name", model_name),
            ("request_output_len", request_output_len),
            ("temperature", temperature),
            ("random_seed", random_seed),
            ("runtime_top_k", runtime_top_k),
            ("runtime_top_p", runtime_top_p),
            ("frequency_penalty", frequency_penalty),
            ("presence_penalty", presence_penalty),
            ("length_penalty", length_penalty),
            ("stop_words", stop_words or []),
        ]
        if value is not None
    }

    if extra_request_args:
        json_dict.update(extra_request_args)

    response = driver.make_request(
        method="post",
        endpoint="chat",
        headers={"Content-Type": "application/json"},
        json=json_dict,
    )

    return cast(ModelTurn, response)


def _check_conversation_history(
    conversation_history: List[HumanTurn | ModelTurn],
) -> None:
    """Checks that a conversation is well constructed.

    Raises InvalidConversationError otherwise.
    """
    if len(conversation_history) == 0:
        raise InvalidConversationError(reason="Conversation history cannot be empty")

    for i, turn in enumerate(conversation_history):
        if i > 0 and ("media_url" in turn):
            raise InvalidConversationError(
                reason=f"Media is only supported for the first turn, found media keys in turn {i} '{turn}'."
            )

        valid_key_sets = [{"type", "text"}]
        if i == 0:
            valid_key_sets.append({"type", "text", "media_url"})

        turn_keys = set(turn.keys())
        if not any(turn_keys == valid_key_set for valid_key_set in valid_key_sets):
            expected_keys_str = " or ".join(map(str, valid_key_sets))
            raise InvalidConversationError(
                reason=f"Expected keys {expected_keys_str} for turn {i} '{turn}', got keys {turn_keys}."
            )

        for key, value in turn.items():
            if not isinstance(value, str):
                raise InvalidConversationError(
                    reason=f"Expected string for value of '{key}' in turn {i} '{turn}', got {type(value)}."
                )

        expected_type = ["human", "model"][i % 2]
        if turn["type"] != expected_type:
            raise InvalidConversationError(
                reason=(
                    f"Expected type '{expected_type}' for turn {i} '{turn}', got '{turn['type']}'. Conversations should "
                    "alternate between 'human' and 'model', starting with 'human'."
                )
            )


def _local_file_to_media_url(media_filename: str) -> str:
    with open(media_filename, "rb") as f:
        base64_media = base64.b64encode(f.read()).decode("ascii")

    return f"data:application/octet-stream;base64,{base64_media}"
