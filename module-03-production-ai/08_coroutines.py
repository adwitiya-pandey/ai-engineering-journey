# Asynchronous Concurrency with Python Coroutines

import asyncio
import time
from math import sqrt


async def parallel_square_roots(number: int) -> float:
    await asyncio.sleep(6)
    return sqrt(number)


async def main(number: list) -> None:

    coro = [parallel_square_roots(n) for n in number]

    result = await asyncio.gather(*coro, return_exceptions= True)

    for integer, root in zip(number, result):
        if isinstance(root, Exception):
            print(f"Can not calculate square-root of {integer}!")
        else:
            print(f"Square Root of {integer} is {root}")


asyncio.run(main([4, 9, 16, 25, 100]))
asyncio.run(main([4, 9, 16, -25, 100]))


print("=" * 80)
# Another example of a concurrent process with exception handling

async def resilient_llm_fan_out(model: str) -> tuple[str, int]:
    """Simulate one LLM API call. Raises ConnectionError for unstable-llm."""
    if model == "unstable-llm":
        raise ConnectionError("Model unavailable")
    delay = len(model)                          # variable delay per model
    start = time.monotonic()
    await asyncio.sleep(delay)
    elapsed = round(time.monotonic() - start)
    return model, elapsed   


async def main(models: list[str]) -> None:
    """
    Call all models concurrently.
    Handles failures gracefully — one failure does not affect others.
    """
    coro = [resilient_llm_fan_out(model) for model in models]

    results = await asyncio.gather(*coro, return_exceptions= True)

    for model, result in zip(models, results):
        if isinstance(result, Exception):
            print(f"{model}: Failed — {type(result).__name__}: {result}")
        else:
            _, elapsed = result
            print(f"{model}: Response received in {elapsed}s")


names = ["gpt-4", "unstable-llm", "claude-3", "gemini"]
asyncio.run(main(names))


print("=" * 80)
# Running a coroutine in the background instead of running at once using asyncio.create_task()


async def make_tea():
    print("Kettle on...")
    await asyncio.sleep(3)
    return "Tea"

async def make_toast():
    print("Bread in toaster...")
    await asyncio.sleep(2)
    return "Toast"

async def breakfast():
    tea = asyncio.create_task(make_tea())
    toast = asyncio.create_task(make_toast())
    print("Both tasks started — doing other work!")
    start = time.monotonic()
    await asyncio.sleep(6)
    print(await tea, "is ready!")
    print(await toast, "is ready!")
    elapsed = round(time.monotonic() - start)
    print(f"Total runtime = {elapsed} seconds")

asyncio.run(breakfast())
