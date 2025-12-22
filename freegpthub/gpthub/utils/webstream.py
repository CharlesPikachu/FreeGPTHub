'''
Function:
    Implementation of StreamSanitizer
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import sys
import json
import codecs
import asyncio
import functools
from itertools import chain
from dataclasses import dataclass, field
from typing import (
    Any, AsyncGenerator, AsyncIterable, Callable, Dict, Generator, Iterable, List, Literal, Optional, Union
)


'''settings'''
EncodingType = Literal[
    "utf-8", "utf-16", "utf-32", "ascii", "latin1", "cp1252", "iso-8859-1", "iso-8859-2", "windows-1250",
    "windows-1251", "windows-1252", "gbk", "big5", "shift_jis", "euc-jp", "euc-kr",
]


'''compileregexes'''
def compileregexes(patterns: Optional[List[Union[str, re.Pattern[str]]]]) -> Optional[List[re.Pattern[str]]]:
    if not patterns: return None
    out: List[re.Pattern[str]] = []
    for i, p in enumerate(patterns):
        try:
            if isinstance(p, str): out.append(re.compile(p))
            elif isinstance(p, re.Pattern): out.append(p)
            else: raise ValueError(f"Pattern at index {i} must be a string or compiled regex pattern, got {type(p).__name__}")
        except re.error as e:
            raise ValueError(f"Invalid regex pattern at index {i}: '{p}' - {e}")
    return out


'''processchunk'''
def processchunk(chunk: str, intro_value: str, to_json: bool, skip_markers: List[str], strip_chars: Optional[str], yield_raw_on_error: bool, 
                 error_handler: Optional[Callable[[Exception, str], Optional[Any]]] = None, skip_regexes: Optional[List[re.Pattern[str]]] = None, 
                 extract_regexes: Optional[List[re.Pattern[str]]] = None) -> Union[str, Dict[str, Any], Any, None]:
    if not isinstance(chunk, str) or not chunk: return None
    sanitized_chunk = chunk
    if intro_value and len(chunk) >= len(intro_value) and chunk[: len(intro_value)] == intro_value: sanitized_chunk = chunk[len(intro_value) :]
    if strip_chars is not None: sanitized_chunk = sanitized_chunk.strip(strip_chars)
    else: sanitized_chunk = sanitized_chunk.lstrip()
    if not sanitized_chunk or any(marker == sanitized_chunk for marker in skip_markers): return None
    if extract_regexes:
        extracted_content = None
        for rx in extract_regexes:
            m = rx.search(sanitized_chunk)
            if not m: continue
            if m.groups(): extracted_content = m.group(1) if len(m.groups()) == 1 else str(m.groups())
            else: extracted_content = m.group(0)
            break
        if extracted_content is None:
            if not to_json: return None
        else:
            sanitized_chunk = extracted_content
    if skip_regexes and any(rx.search(sanitized_chunk) for rx in skip_regexes): return None
    if to_json:
        try:
            if (len(sanitized_chunk) >= 2 and sanitized_chunk[0] not in "{[" and sanitized_chunk[-1] not in "}]"): sanitized_chunk = sanitized_chunk.strip()
            return json.loads(sanitized_chunk)
        except Exception as e:
            if error_handler:
                try:
                    handled = error_handler(e, sanitized_chunk)
                    if handled is not None: return handled
                except Exception:
                    pass
            return sanitized_chunk if yield_raw_on_error else None
    return sanitized_chunk


'''decodebytessync'''
def decodebytessync(byte_iter: Iterable[bytes], encoding: EncodingType, errors: str, buffer_size: int) -> Generator[str, None, None]:
    try: decoder = codecs.getincrementaldecoder(encoding)(errors=errors)
    except LookupError: decoder = codecs.getincrementaldecoder("utf-8")(errors=errors)
    buffer = bytearray(buffer_size)
    view = memoryview(buffer)
    for b in byte_iter:
        if not b: continue
        try:
            if len(b) <= buffer_size:
                buffer[: len(b)] = b
                text = decoder.decode(view[: len(b)], final=False)
            else: text = decoder.decode(b, final=False)
            if text: yield text
        except UnicodeDecodeError: yield f"[Encoding Error: Could not decode bytes with {encoding}]\n"
    try:
        tail = decoder.decode(b"", final=True)
        if tail: yield tail
    except UnicodeDecodeError:
        yield f"[Encoding Error: Could not decode final bytes with {encoding}]\n"


'''decodebytesasync'''
async def decodebytesasync(byte_aiter: AsyncIterable[bytes], encoding: EncodingType, errors: str, buffer_size: int) -> AsyncGenerator[str, None]:
    try: decoder = codecs.getincrementaldecoder(encoding)(errors=errors)
    except LookupError: decoder = codecs.getincrementaldecoder("utf-8")(errors=errors)
    buffer = bytearray(buffer_size)
    view = memoryview(buffer)
    async for b in byte_aiter:
        if not b: continue
        try:
            if len(b) <= buffer_size:
                buffer[: len(b)] = b
                text = decoder.decode(view[: len(b)], final=False)
            else:
                text = decoder.decode(b, final=False)
            if text: yield text
        except UnicodeDecodeError: yield f"[Encoding Error: Could not decode bytes with {encoding}]\n"
    try:
        tail = decoder.decode(b"", final=True)
        if tail: yield tail
    except UnicodeDecodeError: yield f"[Encoding Error: Could not decode final bytes with {encoding}]\n"


'''splitcompletelines'''
def splitcompletelines(buf: str, line_delimiter: Optional[str]) -> tuple[list[str], str]:
    if not buf: return [], ""
    if line_delimiter is not None:
        parts = buf.split(line_delimiter)
        if len(parts) == 1: return [], buf
        return parts[:-1], parts[-1]
    parts_ke = buf.splitlines(True)
    if not parts_ke: return [], buf
    complete: list[str] = []
    remainder = ""
    for i, p in enumerate(parts_ke):
        if p.endswith("\n") or p.endswith("\r"):
            complete.append(p.rstrip("\r\n"))
        else:
            if i == len(parts_ke) - 1: remainder = p
            else: complete.append(p)
    return complete, remainder


'''StreamSanitizer'''
@dataclass(slots=True)
class StreamSanitizer:
    intro_value: str = "data:"
    to_json: bool = True
    skip_markers: Optional[List[str]] = None
    strip_chars: Optional[str] = None
    start_marker: Optional[str] = None
    end_marker: Optional[str] = None
    content_extractor: Optional[Callable[[Union[str, Dict[str, Any]]], Optional[Any]]] = None
    yield_raw_on_error: bool = True
    encoding: EncodingType = "utf-8"
    encoding_errors: str = "replace"
    buffer_size: int = 8192
    line_delimiter: Optional[str] = None
    error_handler: Optional[Callable[[Exception, str], Optional[Any]]] = None
    skip_regexes: Optional[List[Union[str, re.Pattern[str]]]] = None
    extract_regexes: Optional[List[Union[str, re.Pattern[str]]]] = None
    object_mode: Literal["as_is", "json", "str"] = "json"
    raw: bool = False
    output_formatter: Optional[Callable[[Any], Any]] = None
    debug: bool = False
    _skip_markers_eff: List[str] = field(init=False, repr=False)
    _skip_rx: Optional[List[re.Pattern[str]]] = field(init=False, repr=False, default=None)
    _extract_rx: Optional[List[re.Pattern[str]]] = field(init=False, repr=False, default=None)
    '''postinit'''
    def __post_init__(self) -> None:
        self._skip_markers_eff: List[str] = self.skip_markers or []
        self._skip_rx: Optional[List[re.Pattern[str]]] = compileregexes(self.skip_regexes)
        self._extract_rx: Optional[List[re.Pattern[str]]] = compileregexes(self.extract_regexes)
    '''_fmt'''
    def _fmt(self, item: Any) -> Any:
        return self.output_formatter(item) if self.output_formatter else item
    '''_rawsync'''
    def _rawsync(self, data: Any) -> Generator[Any, None, None]:
        if isinstance(data, (bytes, bytearray)):
            yield data.decode(self.encoding, self.encoding_errors)
            return
        if isinstance(data, str):
            yield data
            return
        if hasattr(data, "__iter__"):
            for x in data:
                if x is None: continue
                if isinstance(x, (bytes, bytearray)): yield x.decode(self.encoding, self.encoding_errors)
                else: yield x
            return
        if data is not None: yield data
    '''_rawasync'''
    async def _rawasync(self, data: Any) -> AsyncGenerator[Any, None]:
        if isinstance(data, (bytes, bytearray)):
            yield data.decode(self.encoding, self.encoding_errors)
            return
        if isinstance(data, str):
            yield data
            return
        if hasattr(data, "__aiter__"):
            async for x in data:
                if x is None: continue
                if isinstance(x, (bytes, bytearray)): yield x.decode(self.encoding, self.encoding_errors)
                else: yield x
            return
        if hasattr(data, "__iter__"):
            for x in data:
                if x is None: continue
                if isinstance(x, (bytes, bytearray)): yield x.decode(self.encoding, self.encoding_errors)
                else: yield x
            return
        if data is not None: yield data
    '''iter'''
    def iter(self, data: Any) -> Generator[Any, None, None]:
        if self.raw:
            yield from self._rawsync(data)
            return
        if data is None: return
        if isinstance(data, (dict, list, int, float, bool)):
            if self.object_mode == "as_is":
                yield self._fmt(data)
                return
            if self.object_mode == "str": data = str(data)
            else:
                try: data = json.dumps(data)
                except Exception: data = str(data)
        text_iter: Iterable[str]
        if isinstance(data, (bytes, bytearray)): text_iter = decodebytessync([bytes(data)], self.encoding, self.encoding_errors, self.buffer_size)
        elif isinstance(data, str): text_iter = [data]
        elif hasattr(data, "read") and callable(data.read):
            try:
                payload = data.read()
                if isinstance(payload, (bytes, bytearray)): text_iter = decodebytessync([bytes(payload)], self.encoding, self.encoding_errors, self.buffer_size)
                else: text_iter = [str(payload)]
            except Exception:
                text_iter = [str(data)]
        elif hasattr(data, "__iter__"):
            it = iter(data)
            first = next(it, None)
            if first is None: return
            stream = chain([first], it)
            if isinstance(first, (bytes, bytearray)): text_iter = decodebytessync((bytes(x) for x in stream), self.encoding, self.encoding_errors, self.buffer_size,)
            elif isinstance(first, str): text_iter = (x for x in stream if x is not None)
            else: text_iter = (str(x) for x in stream if x is not None)
        else:
            text_iter = [str(data)]
        buf, line_buf, found_start = "", "", self.start_marker is None
        end_keep = (len(self.end_marker) - 1) if self.end_marker else 0
        start_keep = (len(self.start_marker) - 1) if self.start_marker else 0
        start_keep = max(start_keep, 256) if self.start_marker else 0
        def _emitlinesfromtext(text: str) -> Generator[Any, None, None]:
            nonlocal line_buf
            if not text: return
            line_buf += text
            lines, line_buf = splitcompletelines(line_buf, self.line_delimiter)
            for ln in lines:
                use_extract = self._extract_rx if not self.content_extractor else None
                res = processchunk(ln, self.intro_value, self.to_json, self._skip_markers_eff, self.strip_chars, self.yield_raw_on_error, self.error_handler, self._skip_rx, use_extract)
                if res is None: continue
                if self.content_extractor:
                    try: final = self.content_extractor(res)
                    except Exception as e:
                        if self.debug: print(f"[StreamSanitizer] content_extractor error: {e}", file=sys.stderr)
                        continue
                    if final is None: continue
                    if self._extract_rx and isinstance(final, str):
                        extracted = None
                        for rx in self._extract_rx:
                            m = rx.search(final)
                            if not m: continue
                            if m.groups(): extracted = m.group(1) if len(m.groups()) == 1 else str(m.groups())
                            else: extracted = m.group(0)
                            break
                        if extracted is not None: yield self._fmt(extracted)
                    else: yield self._fmt(final)
                else:
                    yield self._fmt(res)
        try:
            for chunk in text_iter:
                if not chunk: continue
                buf += chunk
                if not found_start and self.start_marker:
                    idx = buf.find(self.start_marker)
                    if idx == -1:
                        buf = buf[-start_keep:] if start_keep else ""
                        continue
                    found_start = True
                    buf = buf[idx + len(self.start_marker) :]
                if found_start and self.end_marker:
                    idx = buf.find(self.end_marker)
                    if idx != -1:
                        active = buf[:idx]
                        buf = buf[idx + len(self.end_marker) :]
                        yield from _emitlinesfromtext(active)
                        if line_buf: yield from _emitlinesfromtext(self.line_delimiter or "\n")
                        found_start = self.start_marker is None
                        continue
                    if end_keep and len(buf) > end_keep:
                        active = buf[: len(buf) - end_keep]
                        buf = buf[len(buf) - end_keep :]
                        yield from _emitlinesfromtext(active)
                    else: continue
                else:
                    yield from _emitlinesfromtext(buf)
                    buf = ""
            if found_start:
                if self.end_marker: yield from _emitlinesfromtext(buf)
                else: yield from _emitlinesfromtext(buf)
                buf = ""
            if line_buf:
                rem = line_buf
                line_buf = ""
                for out in _emitlinesfromtext(rem + (self.line_delimiter or "\n")): yield out
        except Exception as e:
            if self.debug: print(f"[StreamSanitizer] stream error: {e}", file=sys.stderr)
    '''aiter'''
    async def aiter(self, data: Any) -> AsyncGenerator[Any, None]:
        if self.raw:
            async for x in self._rawasync(data): yield x
            return
        if data is None: return
        if isinstance(data, (dict, list, int, float, bool)):
            if self.object_mode == "as_is":
                yield self._fmt(data)
                return
            if self.object_mode == "str":
                data = str(data)
            else:
                try: data = json.dumps(data)
                except Exception: data = str(data)
        async def _as_text_aiter(obj: Any) -> AsyncGenerator[str, None]:
            if isinstance(obj, (bytes, bytearray)):
                async for t in decodebytesasync(_single_bytes_async(bytes(obj)), self.encoding, self.encoding_errors, self.buffer_size): yield t
                return
            if isinstance(obj, str):
                yield obj
                return
            if hasattr(obj, "read") and callable(obj.read):
                try:
                    payload = obj.read()
                    if isinstance(payload, (bytes, bytearray)):
                        async for t in decodebytesasync(_single_bytes_async(bytes(payload)), self.encoding, self.encoding_errors, self.buffer_size): yield t
                    else:
                        yield str(payload)
                    return
                except Exception:
                    yield str(obj)
                    return
            if hasattr(obj, "__aiter__"):
                it = obj.__aiter__()
                first = None
                async for first in it: break
                if first is None: return
                async def _chain(first_item, rest_it):
                    yield first_item
                    async for y in rest_it: yield y
                stream = _chain(first, it)
                if isinstance(first, (bytes, bytearray)):
                    async for t in decodebytesasync((bytes(x) async for x in stream), self.encoding, self.encoding_errors, self.buffer_size): yield t
                elif isinstance(first, str):
                    async for x in stream:
                        if x: yield x
                else:
                    async for x in stream:
                        if x is not None: yield str(x)
                return
            if hasattr(obj, "__iter__"):
                it = iter(obj)
                first = next(it, None)
                if first is None: return
                stream = chain([first], it)
                if isinstance(first, (bytes, bytearray)):
                    for t in decodebytessync((bytes(x) for x in stream), self.encoding, self.encoding_errors, self.buffer_size): yield t
                elif isinstance(first, str):
                    for x in stream:
                        if x: yield x
                else:
                    for x in stream:
                        if x is not None: yield str(x)
                return
            yield str(obj)
        async def _single_bytes_async(b: bytes) -> AsyncGenerator[bytes, None]: yield b
        buf, line_buf, found_start = "", "", self.start_marker is None
        end_keep = (len(self.end_marker) - 1) if self.end_marker else 0
        start_keep = (len(self.start_marker) - 1) if self.start_marker else 0
        start_keep = max(start_keep, 256) if self.start_marker else 0
        async def _emitlinesfromtext(text: str) -> AsyncGenerator[Any, None]:
            nonlocal line_buf
            if not text: return
            line_buf += text
            lines, line_buf2 = splitcompletelines(line_buf, self.line_delimiter)
            line_buf = line_buf2
            for ln in lines:
                use_extract = self._extract_rx if not self.content_extractor else None
                res = processchunk(ln, self.intro_value, self.to_json, self._skip_markers_eff, self.strip_chars, self.yield_raw_on_error, self.error_handler, self._skip_rx, use_extract)
                if res is None: continue
                if self.content_extractor:
                    try: final = self.content_extractor(res)
                    except Exception as e:
                        if self.debug: print(f"[StreamSanitizer] content_extractor error: {e}", file=sys.stderr)
                        continue
                    if final is None: continue
                    if self._extract_rx and isinstance(final, str):
                        extracted = None
                        for rx in self._extract_rx:
                            m = rx.search(final)
                            if not m: continue
                            if m.groups(): extracted = m.group(1) if len(m.groups()) == 1 else str(m.groups())
                            else: extracted = m.group(0)
                            break
                        if extracted is not None: yield self._fmt(extracted)
                    else:
                        yield self._fmt(final)
                else:
                    yield self._fmt(res)
        try:
            async for chunk in _as_text_aiter(data):
                if not chunk: continue
                buf += chunk
                if not found_start and self.start_marker:
                    idx = buf.find(self.start_marker)
                    if idx == -1:
                        buf = buf[-start_keep:] if start_keep else ""
                        continue
                    found_start = True
                    buf = buf[idx + len(self.start_marker) :]
                if found_start and self.end_marker:
                    idx = buf.find(self.end_marker)
                    if idx != -1:
                        active = buf[:idx]
                        buf = buf[idx + len(self.end_marker) :]
                        async for out in _emitlinesfromtext(active): yield out
                        if line_buf:
                            async for out in _emitlinesfromtext(self.line_delimiter or "\n"): yield out
                        found_start = self.start_marker is None
                        continue
                    if end_keep and len(buf) > end_keep:
                        active = buf[: len(buf) - end_keep]
                        buf = buf[len(buf) - end_keep :]
                        async for out in _emitlinesfromtext(active): yield out
                    else:
                        continue
                else:
                    async for out in _emitlinesfromtext(buf): yield out
                    buf = ""
            if found_start:
                async for out in _emitlinesfromtext(buf): yield out
            if line_buf:
                rem = line_buf
                line_buf = ""
                async for out in _emitlinesfromtext(rem + (self.line_delimiter or "\n")): yield out
        except Exception as e:
            if self.debug: print(f"[StreamSanitizer] async stream error: {e}", file=sys.stderr)
    '''call'''
    def __call__(self, data: Any) -> Union[Generator[Any, None, None], AsyncGenerator[Any, None]]:
        if hasattr(data, "__aiter__"): return self.aiter(data)
        return self.iter(data)
    '''decorator'''
    def decorator(self, func=None):
        def _wrap(f):
            if asyncio.iscoroutinefunction(f):
                @functools.wraps(f)
                async def aw(*args, **kwargs):
                    res = await f(*args, **kwargs)
                    return self(res)
                return aw
            else:
                @functools.wraps(f)
                def sw(*args, **kwargs):
                    res = f(*args, **kwargs)
                    return self(res)
                return sw
        return _wrap if func is None else _wrap(func)