from fastapi import UploadFile


async def process_plain_text(text: str) -> str:
    return text


async def read_plain_text(file: UploadFile) -> str:
    contents = await file.read()
    text = contents.decode("utf-8")
    result = await process_plain_text(text)

    return result
