from fastapi import UploadFile


async def process_plain_text(text):
    return text


async def read_plain_text(file: UploadFile) -> str:
    # Read uploaded file in-memory using async I/O
    contents = await file.read()
    # Decode the bytes to a string assuming the file is encoded in UTF-8
    text = contents.decode("utf-8")

    result = await process_plain_text(text)

    return result
