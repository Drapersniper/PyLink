"""
MIT License

Copyright (c) 2017-present Devoxin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import annotations

import struct
import typing
from base64 import b64decode, b64encode
from io import BytesIO

from pylav.utils.vendored.lavalink_py.utfm_codec import read_utfm


# noinspection SpellCheckingInspection
class DataReader:
    def __init__(self, ts: str) -> None:
        self._buf = BytesIO(b64decode(ts))

    def _read(self, count: int) -> bytes:
        return self._buf.read(count)

    def read_byte(self) -> bytes:
        return self._read(1)

    def read_boolean(self) -> bool:
        (result,) = struct.unpack("B", self.read_byte())
        return typing.cast(bool, result)

    def read_unsigned_short(self) -> int:
        (result,) = struct.unpack(">H", self._read(2))
        return typing.cast(int, result)

    def read_int(self) -> int:
        (result,) = struct.unpack(">i", self._read(4))
        return typing.cast(int, result)

    def read_long(self) -> int:
        (result,) = struct.unpack(">Q", self._read(8))
        return typing.cast(int, result)

    def read_utf(self) -> str:
        text_length = self.read_unsigned_short()
        return self._read(text_length).decode()

    def read_utfm(self) -> str:
        text_length = self.read_unsigned_short()
        utf_string = self._read(text_length)
        return read_utfm(text_length, utf_string)

    def read_nullable_utf(self) -> str | None:
        return self.read_utf() if self.read_boolean() else None

    def read_nullable_utfm(self) -> str | None:
        return self.read_utfm() if self.read_boolean() else None


class DataWriter:
    def __init__(self) -> None:
        self._buf = BytesIO()

    def _write(self, data: bytes) -> None:
        self._buf.write(data)

    def write_byte(self, byte: bytes) -> None:
        self._buf.write(byte)

    def write_boolean(self, boolean: bool) -> None:
        enc = struct.pack("B", 1 if boolean else 0)
        self.write_byte(enc)

    def write_unsigned_short(self, short: int) -> None:
        enc = struct.pack(">H", short)
        self._write(enc)

    def write_int(self, integer: int) -> None:
        enc = struct.pack(">i", integer)
        self._write(enc)

    def write_long(self, long_value: int) -> None:
        enc = struct.pack(">Q", long_value)
        self._write(enc)

    def write_utf(self, utf_string: str) -> None:
        utf = utf_string.encode("utf8")
        byte_len = len(utf)

        if byte_len > 65535:
            raise OverflowError("UTF string may not exceed 65535 bytes!")

        self.write_unsigned_short(byte_len)
        self._write(utf)

    def write_nullable_utf(self, utf_string: str | None) -> None:
        if utf_string is None:
            self.write_boolean(False)
        else:
            self.write_boolean(True)
            self.write_utf(utf_string)

    def finish(self) -> bytes:
        with BytesIO() as track_buf:
            byte_len = self._buf.getbuffer().nbytes
            flags = byte_len | (1 << 30)
            enc_flags = struct.pack(">i", flags)
            track_buf.write(enc_flags)

            self._buf.seek(0)
            track_buf.write(self._buf.read())
            self._buf.close()

            track_buf.seek(0)
            return track_buf.read()

    def to_base64(self) -> str:
        return b64encode(self.finish()).decode()
