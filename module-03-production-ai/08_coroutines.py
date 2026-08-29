import asyncio

async def say_hello():
    print("Hello, future AI Engineer!")
    await asyncio.sleep(5)      # pause for 5 seconds
    print("A few moments later — still here!")

# This is how you RUN a coroutine:
asyncio.run(say_hello())        # ← Creates event loop, runs it, closes it