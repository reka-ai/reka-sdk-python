# This file was auto-generated by Fern from our API Definition.

import json
import typing
import urllib.parse
from json.decoder import JSONDecodeError

import httpx_sse

from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.jsonable_encoder import jsonable_encoder
from ..core.query_encoder import encode_query
from ..core.remove_none_from_dict import remove_none_from_dict
from ..core.request_options import RequestOptions
from ..core.unchecked_base_model import construct_type
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from ..types.chat_message import ChatMessage
from ..types.chat_response import ChatResponse
from ..types.chunk_chat_response import ChunkChatResponse
from ..types.http_validation_error import HttpValidationError
from ..types.tool import Tool
from ..types.tool_choice import ToolChoice

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class ChatClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def create_stream(
        self,
        *,
        messages: typing.Sequence[ChatMessage],
        model: str,
        frequency_penalty: typing.Optional[float] = OMIT,
        max_tokens: typing.Optional[int] = OMIT,
        presence_penalty: typing.Optional[float] = OMIT,
        seed: typing.Optional[int] = OMIT,
        stop: typing.Optional[typing.Sequence[str]] = OMIT,
        temperature: typing.Optional[float] = OMIT,
        tool_choice: typing.Optional[ToolChoice] = OMIT,
        tools: typing.Optional[typing.Sequence[Tool]] = OMIT,
        top_k: typing.Optional[int] = OMIT,
        top_p: typing.Optional[float] = OMIT,
        use_search_engine: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Iterator[ChunkChatResponse]:
        """
        Parameters
        ----------
        messages : typing.Sequence[ChatMessage]
            List of messages specifying the conversation so far.

        model : str
            See [Available Models](/available-models) for possible values.

        frequency_penalty : typing.Optional[float]
            Parameter which penalises tokens based on their frequency in the model's output so far. The larger the value, the higher the penalisation. 0.0 means no frequency penalty. Defaults to 0.0.

        max_tokens : typing.Optional[int]
            The maximum number of new tokens to be generated by the model. Note that this is limited by the model's context length. Defaults to 1024.

        presence_penalty : typing.Optional[float]
            Parameter which penalises tokens based on whether they have appeared in the model's output so far. The larger the value, the higher the penalisation. 0.0 means no presence penalty. Defaults to 0.0.

        seed : typing.Optional[int]
            Random seed used for generations. The same value forces the model to sample the same output.

        stop : typing.Optional[typing.Sequence[str]]
            A list of stop strings used to control generation. If the model generates one of these, it will stop.

        temperature : typing.Optional[float]
            Positive number representing the temperature to use for generation. Higher values will make the output more unformly random or *creative*. 0.0 means greedy decoding. Defaults to 0.4.

        tool_choice : typing.Optional[ToolChoice]
            Controls how the model may use the provided tools. Set to 'auto' to let the model decide whether or not to invoke a tool. Set to 'none' to disable tool use. Set to 'tool' to force the model to invoke a tool.

        tools : typing.Optional[typing.Sequence[Tool]]
            List of tools the model has access to.

        top_k : typing.Optional[int]
            Parameter which forces the model to only consider the tokens with the `top_k` highest probabilities at the next step. Defaults to 1024.

        top_p : typing.Optional[float]
            Parameter used to do nucleus sampling, i.e. only consider tokens comprising the `top_p` probability of the next token's distribution. Defaults to 0.95.

        use_search_engine : typing.Optional[bool]
            Whether to consider using search engine to complete the request. Note that even if this is set to `True`, the model might decide to not use search.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Yields
        ------
        typing.Iterator[ChunkChatResponse]


        Examples
        --------
        from reka import ChatMessage, Tool, ToolCall
        from reka.client import Reka

        client = Reka(
            api_key="YOUR_API_KEY",
        )
        response = client.chat.create_stream(
            frequency_penalty=1.1,
            max_tokens=1,
            messages=[
                ChatMessage(
                    content="string",
                    role="user",
                    tool_calls=[
                        ToolCall(
                            id="string",
                            name="string",
                            parameters={},
                        )
                    ],
                )
            ],
            model="string",
            presence_penalty=1.1,
            seed=1,
            stop=["string"],
            temperature=1.1,
            tool_choice="auto",
            tools=[
                Tool(
                    description="string",
                    name="string",
                    parameters={"string": {"key": "value"}},
                )
            ],
            top_k=1,
            top_p=1.1,
            use_search_engine=True,
        )
        for chunk in response:
            yield chunk
        """
        _request: typing.Dict[str, typing.Any] = {"messages": messages, "model": model, "stream": True}
        if frequency_penalty is not OMIT:
            _request["frequency_penalty"] = frequency_penalty
        if max_tokens is not OMIT:
            _request["max_tokens"] = max_tokens
        if presence_penalty is not OMIT:
            _request["presence_penalty"] = presence_penalty
        if seed is not OMIT:
            _request["seed"] = seed
        if stop is not OMIT:
            _request["stop"] = stop
        if temperature is not OMIT:
            _request["temperature"] = temperature
        if tool_choice is not OMIT:
            _request["tool_choice"] = tool_choice
        if tools is not OMIT:
            _request["tools"] = tools
        if top_k is not OMIT:
            _request["top_k"] = top_k
        if top_p is not OMIT:
            _request["top_p"] = top_p
        if use_search_engine is not OMIT:
            _request["use_search_engine"] = use_search_engine
        with self._client_wrapper.httpx_client.stream(
            method="POST",
            url=urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "chat"),
            params=encode_query(
                jsonable_encoder(
                    request_options.get("additional_query_parameters") if request_options is not None else None
                )
            ),
            json=jsonable_encoder(_request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(_request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        ) as _response:
            if 200 <= _response.status_code < 300:
                _event_source = httpx_sse.EventSource(_response)
                for _sse in _event_source.iter_sse():
                    yield typing.cast(ChunkChatResponse, construct_type(type_=ChunkChatResponse, object_=json.loads(_sse.data)))  # type: ignore
                return
            _response.read()
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(HttpValidationError, construct_type(type_=HttpValidationError, object_=_response.json()))  # type: ignore
                )
            try:
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

    def create(
        self,
        *,
        messages: typing.Sequence[ChatMessage],
        model: str,
        frequency_penalty: typing.Optional[float] = OMIT,
        max_tokens: typing.Optional[int] = OMIT,
        presence_penalty: typing.Optional[float] = OMIT,
        seed: typing.Optional[int] = OMIT,
        stop: typing.Optional[typing.Sequence[str]] = OMIT,
        temperature: typing.Optional[float] = OMIT,
        tool_choice: typing.Optional[ToolChoice] = OMIT,
        tools: typing.Optional[typing.Sequence[Tool]] = OMIT,
        top_k: typing.Optional[int] = OMIT,
        top_p: typing.Optional[float] = OMIT,
        use_search_engine: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ChatResponse:
        """
        Parameters
        ----------
        messages : typing.Sequence[ChatMessage]
            List of messages specifying the conversation so far.

        model : str
            See [Available Models](/available-models) for possible values.

        frequency_penalty : typing.Optional[float]
            Parameter which penalises tokens based on their frequency in the model's output so far. The larger the value, the higher the penalisation. 0.0 means no frequency penalty. Defaults to 0.0.

        max_tokens : typing.Optional[int]
            The maximum number of new tokens to be generated by the model. Note that this is limited by the model's context length. Defaults to 1024.

        presence_penalty : typing.Optional[float]
            Parameter which penalises tokens based on whether they have appeared in the model's output so far. The larger the value, the higher the penalisation. 0.0 means no presence penalty. Defaults to 0.0.

        seed : typing.Optional[int]
            Random seed used for generations. The same value forces the model to sample the same output.

        stop : typing.Optional[typing.Sequence[str]]
            A list of stop strings used to control generation. If the model generates one of these, it will stop.

        temperature : typing.Optional[float]
            Positive number representing the temperature to use for generation. Higher values will make the output more unformly random or *creative*. 0.0 means greedy decoding. Defaults to 0.4.

        tool_choice : typing.Optional[ToolChoice]
            Controls how the model may use the provided tools. Set to 'auto' to let the model decide whether or not to invoke a tool. Set to 'none' to disable tool use. Set to 'tool' to force the model to invoke a tool.

        tools : typing.Optional[typing.Sequence[Tool]]
            List of tools the model has access to.

        top_k : typing.Optional[int]
            Parameter which forces the model to only consider the tokens with the `top_k` highest probabilities at the next step. Defaults to 1024.

        top_p : typing.Optional[float]
            Parameter used to do nucleus sampling, i.e. only consider tokens comprising the `top_p` probability of the next token's distribution. Defaults to 0.95.

        use_search_engine : typing.Optional[bool]
            Whether to consider using search engine to complete the request. Note that even if this is set to `True`, the model might decide to not use search.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ChatResponse


        Examples
        --------
        from reka import ChatMessage
        from reka.client import Reka

        client = Reka(
            api_key="YOUR_API_KEY",
        )
        client.chat.create(
            model="reka-core",
            messages=[
                ChatMessage(
                    role="user",
                    content="What is the fifth prime number?",
                )
            ],
        )
        """
        _request: typing.Dict[str, typing.Any] = {"messages": messages, "model": model, "stream": False}
        if frequency_penalty is not OMIT:
            _request["frequency_penalty"] = frequency_penalty
        if max_tokens is not OMIT:
            _request["max_tokens"] = max_tokens
        if presence_penalty is not OMIT:
            _request["presence_penalty"] = presence_penalty
        if seed is not OMIT:
            _request["seed"] = seed
        if stop is not OMIT:
            _request["stop"] = stop
        if temperature is not OMIT:
            _request["temperature"] = temperature
        if tool_choice is not OMIT:
            _request["tool_choice"] = tool_choice
        if tools is not OMIT:
            _request["tools"] = tools
        if top_k is not OMIT:
            _request["top_k"] = top_k
        if top_p is not OMIT:
            _request["top_p"] = top_p
        if use_search_engine is not OMIT:
            _request["use_search_engine"] = use_search_engine
        _response = self._client_wrapper.httpx_client.request(
            method="POST",
            url=urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "chat"),
            params=encode_query(
                jsonable_encoder(
                    request_options.get("additional_query_parameters") if request_options is not None else None
                )
            ),
            json=jsonable_encoder(_request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(_request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return typing.cast(ChatResponse, construct_type(type_=ChatResponse, object_=_response.json()))  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                typing.cast(HttpValidationError, construct_type(type_=HttpValidationError, object_=_response.json()))  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncChatClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def create_stream(
        self,
        *,
        messages: typing.Sequence[ChatMessage],
        model: str,
        frequency_penalty: typing.Optional[float] = OMIT,
        max_tokens: typing.Optional[int] = OMIT,
        presence_penalty: typing.Optional[float] = OMIT,
        seed: typing.Optional[int] = OMIT,
        stop: typing.Optional[typing.Sequence[str]] = OMIT,
        temperature: typing.Optional[float] = OMIT,
        tool_choice: typing.Optional[ToolChoice] = OMIT,
        tools: typing.Optional[typing.Sequence[Tool]] = OMIT,
        top_k: typing.Optional[int] = OMIT,
        top_p: typing.Optional[float] = OMIT,
        use_search_engine: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.AsyncIterator[ChunkChatResponse]:
        """
        Parameters
        ----------
        messages : typing.Sequence[ChatMessage]
            List of messages specifying the conversation so far.

        model : str
            See [Available Models](/available-models) for possible values.

        frequency_penalty : typing.Optional[float]
            Parameter which penalises tokens based on their frequency in the model's output so far. The larger the value, the higher the penalisation. 0.0 means no frequency penalty. Defaults to 0.0.

        max_tokens : typing.Optional[int]
            The maximum number of new tokens to be generated by the model. Note that this is limited by the model's context length. Defaults to 1024.

        presence_penalty : typing.Optional[float]
            Parameter which penalises tokens based on whether they have appeared in the model's output so far. The larger the value, the higher the penalisation. 0.0 means no presence penalty. Defaults to 0.0.

        seed : typing.Optional[int]
            Random seed used for generations. The same value forces the model to sample the same output.

        stop : typing.Optional[typing.Sequence[str]]
            A list of stop strings used to control generation. If the model generates one of these, it will stop.

        temperature : typing.Optional[float]
            Positive number representing the temperature to use for generation. Higher values will make the output more unformly random or *creative*. 0.0 means greedy decoding. Defaults to 0.4.

        tool_choice : typing.Optional[ToolChoice]
            Controls how the model may use the provided tools. Set to 'auto' to let the model decide whether or not to invoke a tool. Set to 'none' to disable tool use. Set to 'tool' to force the model to invoke a tool.

        tools : typing.Optional[typing.Sequence[Tool]]
            List of tools the model has access to.

        top_k : typing.Optional[int]
            Parameter which forces the model to only consider the tokens with the `top_k` highest probabilities at the next step. Defaults to 1024.

        top_p : typing.Optional[float]
            Parameter used to do nucleus sampling, i.e. only consider tokens comprising the `top_p` probability of the next token's distribution. Defaults to 0.95.

        use_search_engine : typing.Optional[bool]
            Whether to consider using search engine to complete the request. Note that even if this is set to `True`, the model might decide to not use search.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Yields
        ------
        typing.AsyncIterator[ChunkChatResponse]


        Examples
        --------
        from reka import ChatMessage, Tool, ToolCall
        from reka.client import AsyncReka

        client = AsyncReka(
            api_key="YOUR_API_KEY",
        )
        response = await client.chat.create_stream(
            frequency_penalty=1.1,
            max_tokens=1,
            messages=[
                ChatMessage(
                    content="string",
                    role="user",
                    tool_calls=[
                        ToolCall(
                            id="string",
                            name="string",
                            parameters={},
                        )
                    ],
                )
            ],
            model="string",
            presence_penalty=1.1,
            seed=1,
            stop=["string"],
            temperature=1.1,
            tool_choice="auto",
            tools=[
                Tool(
                    description="string",
                    name="string",
                    parameters={"string": {"key": "value"}},
                )
            ],
            top_k=1,
            top_p=1.1,
            use_search_engine=True,
        )
        async for chunk in response:
            yield chunk
        """
        _request: typing.Dict[str, typing.Any] = {"messages": messages, "model": model, "stream": True}
        if frequency_penalty is not OMIT:
            _request["frequency_penalty"] = frequency_penalty
        if max_tokens is not OMIT:
            _request["max_tokens"] = max_tokens
        if presence_penalty is not OMIT:
            _request["presence_penalty"] = presence_penalty
        if seed is not OMIT:
            _request["seed"] = seed
        if stop is not OMIT:
            _request["stop"] = stop
        if temperature is not OMIT:
            _request["temperature"] = temperature
        if tool_choice is not OMIT:
            _request["tool_choice"] = tool_choice
        if tools is not OMIT:
            _request["tools"] = tools
        if top_k is not OMIT:
            _request["top_k"] = top_k
        if top_p is not OMIT:
            _request["top_p"] = top_p
        if use_search_engine is not OMIT:
            _request["use_search_engine"] = use_search_engine
        async with self._client_wrapper.httpx_client.stream(
            method="POST",
            url=urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "chat"),
            params=encode_query(
                jsonable_encoder(
                    request_options.get("additional_query_parameters") if request_options is not None else None
                )
            ),
            json=jsonable_encoder(_request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(_request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        ) as _response:
            if 200 <= _response.status_code < 300:
                _event_source = httpx_sse.EventSource(_response)
                async for _sse in _event_source.aiter_sse():
                    yield typing.cast(ChunkChatResponse, construct_type(type_=ChunkChatResponse, object_=json.loads(_sse.data)))  # type: ignore
                return
            await _response.aread()
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(HttpValidationError, construct_type(type_=HttpValidationError, object_=_response.json()))  # type: ignore
                )
            try:
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

    async def create(
        self,
        *,
        messages: typing.Sequence[ChatMessage],
        model: str,
        frequency_penalty: typing.Optional[float] = OMIT,
        max_tokens: typing.Optional[int] = OMIT,
        presence_penalty: typing.Optional[float] = OMIT,
        seed: typing.Optional[int] = OMIT,
        stop: typing.Optional[typing.Sequence[str]] = OMIT,
        temperature: typing.Optional[float] = OMIT,
        tool_choice: typing.Optional[ToolChoice] = OMIT,
        tools: typing.Optional[typing.Sequence[Tool]] = OMIT,
        top_k: typing.Optional[int] = OMIT,
        top_p: typing.Optional[float] = OMIT,
        use_search_engine: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ChatResponse:
        """
        Parameters
        ----------
        messages : typing.Sequence[ChatMessage]
            List of messages specifying the conversation so far.

        model : str
            See [Available Models](/available-models) for possible values.

        frequency_penalty : typing.Optional[float]
            Parameter which penalises tokens based on their frequency in the model's output so far. The larger the value, the higher the penalisation. 0.0 means no frequency penalty. Defaults to 0.0.

        max_tokens : typing.Optional[int]
            The maximum number of new tokens to be generated by the model. Note that this is limited by the model's context length. Defaults to 1024.

        presence_penalty : typing.Optional[float]
            Parameter which penalises tokens based on whether they have appeared in the model's output so far. The larger the value, the higher the penalisation. 0.0 means no presence penalty. Defaults to 0.0.

        seed : typing.Optional[int]
            Random seed used for generations. The same value forces the model to sample the same output.

        stop : typing.Optional[typing.Sequence[str]]
            A list of stop strings used to control generation. If the model generates one of these, it will stop.

        temperature : typing.Optional[float]
            Positive number representing the temperature to use for generation. Higher values will make the output more unformly random or *creative*. 0.0 means greedy decoding. Defaults to 0.4.

        tool_choice : typing.Optional[ToolChoice]
            Controls how the model may use the provided tools. Set to 'auto' to let the model decide whether or not to invoke a tool. Set to 'none' to disable tool use. Set to 'tool' to force the model to invoke a tool.

        tools : typing.Optional[typing.Sequence[Tool]]
            List of tools the model has access to.

        top_k : typing.Optional[int]
            Parameter which forces the model to only consider the tokens with the `top_k` highest probabilities at the next step. Defaults to 1024.

        top_p : typing.Optional[float]
            Parameter used to do nucleus sampling, i.e. only consider tokens comprising the `top_p` probability of the next token's distribution. Defaults to 0.95.

        use_search_engine : typing.Optional[bool]
            Whether to consider using search engine to complete the request. Note that even if this is set to `True`, the model might decide to not use search.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ChatResponse


        Examples
        --------
        from reka import ChatMessage
        from reka.client import AsyncReka

        client = AsyncReka(
            api_key="YOUR_API_KEY",
        )
        await client.chat.create(
            model="reka-core",
            messages=[
                ChatMessage(
                    role="user",
                    content="What is the fifth prime number?",
                )
            ],
        )
        """
        _request: typing.Dict[str, typing.Any] = {"messages": messages, "model": model, "stream": False}
        if frequency_penalty is not OMIT:
            _request["frequency_penalty"] = frequency_penalty
        if max_tokens is not OMIT:
            _request["max_tokens"] = max_tokens
        if presence_penalty is not OMIT:
            _request["presence_penalty"] = presence_penalty
        if seed is not OMIT:
            _request["seed"] = seed
        if stop is not OMIT:
            _request["stop"] = stop
        if temperature is not OMIT:
            _request["temperature"] = temperature
        if tool_choice is not OMIT:
            _request["tool_choice"] = tool_choice
        if tools is not OMIT:
            _request["tools"] = tools
        if top_k is not OMIT:
            _request["top_k"] = top_k
        if top_p is not OMIT:
            _request["top_p"] = top_p
        if use_search_engine is not OMIT:
            _request["use_search_engine"] = use_search_engine
        _response = await self._client_wrapper.httpx_client.request(
            method="POST",
            url=urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "chat"),
            params=encode_query(
                jsonable_encoder(
                    request_options.get("additional_query_parameters") if request_options is not None else None
                )
            ),
            json=jsonable_encoder(_request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(_request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return typing.cast(ChatResponse, construct_type(type_=ChatResponse, object_=_response.json()))  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                typing.cast(HttpValidationError, construct_type(type_=HttpValidationError, object_=_response.json()))  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
