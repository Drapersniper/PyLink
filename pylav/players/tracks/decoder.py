import asyncio
import struct

from dacite import from_dict

from pylav.logging import getLogger
from pylav.utils.vendored.lavalink_py.datarw import DataReader

LOGGER = getLogger("PyLav.Track.Decoder")


def decode_track(track: str) -> LavalinkTrackObject:
    """Decodes a base64 track string into a Track object.

    Parameters
    ----------
    track: :class:`str`
        The base64 track string.

    Returns
    -------
    :class:`tuple` of :class:`LavalinkTrackObject` and :class:`int`
    The first element is a LavalinkTrackObject and the second element is encoding version.
    """
    reader = DataReader(track)

    flags = (reader.read_int() & 0xC0000000) >> 30
    version = struct.unpack("B", reader.read_byte()) if flags & 1 != 0 else 1

    title = reader.read_utfm()
    author = reader.read_utfm()
    length = reader.read_long()
    identifier = reader.read_utf()
    is_stream = reader.read_boolean()
    uri = reader.read_nullable_utf()
    source = reader.read_utf()
    thumbnail = None
    isrc = None
    probe = None
    try:
        match source:
            case "youtube":
                thumbnail = f"https://img.youtube.com/vi/{identifier}/mqdefault.jpg"
            case "deezer" | "spotify" | "applemusic":
                isrc = reader.read_nullable_utfm()
                thumbnail = reader.read_nullable_utfm()
            case "yandexmusic":
                thumbnail = reader.read_nullable_utfm()
            case "local" | "http":
                # Probe info
                probe = reader.read_utfm()

        # Position
        _ = reader.read_long()
    except Exception as exc:
        # TODO: Downgrade log to trace for final release
        LOGGER.debug("Failed to decode track", exc_info=exc)

    return from_dict(
        data_class=LavalinkTrackObject,
        data={
            "encoded": track,
            "info": {
                "title": title,
                "author": author,
                "length": length,
                "identifier": identifier,
                "isStream": is_stream,
                "uri": uri,
                "isSeekable": not is_stream,
                "sourceName": source,
                "position": 0,
                "thumbnail": thumbnail,
                "isrc": isrc,
                "probeInfo": probe,
            },
        },
    )


async def async_decoder(track: str) -> LavalinkTrackObject:
    return await asyncio.to_thread(decode_track, track)
