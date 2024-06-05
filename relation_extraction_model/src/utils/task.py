import asyncio
from concurrent.futures import ThreadPoolExecutor

from src.utils.cancellation_token import CancellationToken
from src.utils.relation_extraction import run_relation_extraction

# Create a default executor, which by default creates a new thread for each task
executor = ThreadPoolExecutor()
cancellation_tokens = {}


async def create_task_with_id(task_id: str, text: str):
    cancellation_token = CancellationToken()
    cancellation_tokens[task_id] = cancellation_token

    loop = asyncio.get_running_loop()

    try:
        result = await loop.run_in_executor(
            executor, run_relation_extraction, text, cancellation_token
        )
        return result
    except TimeoutError:
        pass
    finally:
        cancellation_tokens.pop(task_id, None)


async def cancel_task(task_id: str):
    cancellation_token: CancellationToken = cancellation_tokens.get(task_id)
    if cancellation_token:
        cancellation_token.cancel()  # This signals the function to stop its work
        return True
    return False
