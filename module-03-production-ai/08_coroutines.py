# Asynchronous Concurrency with Python Coroutines

import asyncio
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