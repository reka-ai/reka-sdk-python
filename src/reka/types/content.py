# This file was auto-generated by Fern from our API Definition.

import typing

from .chat_message_chunk_content_item import ChatMessageChunkContentItem
from .tool_output import ToolOutput

Content = typing.Union[str, typing.List[ChatMessageChunkContentItem], typing.List[ToolOutput]]
