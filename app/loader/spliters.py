from typing import Generator

from app.config import settings


def simple_splitter(
    raw_content: str, chunk_size: int = settings.default_chunk_size
) -> Generator[str, None, None]:
    """
    Splits the raw content into chunks of specified size.

    Args:
        raw_content (str): The raw content to be split.
        chunk_size (int, optional): The size of each chunk. Defaults to 8192.

    Yields:
        str: A chunk of the raw content.

    Returns:
        None
    """
    chunk = []
    chunk_length = 0

    for line in raw_content.splitlines(keepends=True):
        line_length = len(line)
        if chunk_length + line_length > chunk_size:
            yield "".join(chunk)

            chunk = [line]
            chunk_length = line_length
        else:
            chunk.append(line)
            chunk_length += line_length

    if chunk:  # Add the last chunk if it's not empty
        yield "".join(chunk)

    return
