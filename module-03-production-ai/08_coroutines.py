# Simplest coroutine call
import asyncio

async def say_hello():
    print("Hello, future AI Engineer!")
    await asyncio.sleep(5)      # pause for 5 seconds
    print("A few moments later — still here!")

# This is how you RUN a coroutine:
asyncio.run(say_hello())        # ← Creates event loop, runs it, closes it



# Simple Sequential Execution
async def retrieve_documents(query: str) -> list[str]:
    await asyncio.sleep(1)           # simulate DB lookup
    return ["doc_1", "doc_2", "doc_3"]

async def generate_answer(docs: list[str], query: str) -> str:
    await asyncio.sleep(2)           # simulate LLM call
    return f"Answer based on {len(docs)} docs for: '{query}'"

async def rag_pipeline(query: str) -> str:
    # Step 1 must finish before Step 2 starts — sequential is correct here
    # You cannot generate an answer before you have the documents
    docs   = await retrieve_documents(query)     # wait → get docs
    answer = await generate_answer(docs, query)  # wait → get answer
    return answer

result = asyncio.run(rag_pipeline("Explain transformers"))
print(result)



# Concurrent Fan-Out
async def call_llm(model: str, prompt: str) -> str:
    """Simulate calling one LLM"""
    delays = {"gpt-4": 3, "claude-3": 2, "gemini": 1}
    await asyncio.sleep(delays.get(model, 2))
    return f"{model}: Here is my answer to '{prompt}'"

async def llm_ensemble(prompt: str) -> list[str]:
    """Call 3 LLMs at once, collect all responses"""
    responses = await asyncio.gather(
        call_llm("gpt-4",    prompt),
        call_llm("claude-3", prompt),
        call_llm("gemini",   prompt),
        return_exceptions=True           # ← always in production
    )

    # Separate successes from failures
    results = []
    for model, response in zip(["gpt-4", "claude-3", "gemini"], responses):
        if isinstance(response, Exception):
            print(f"  ✗ {model} failed: {response}")
        else:
            results.append(response)
    return results

answers = asyncio.run(llm_ensemble("What is attention in transformers?"))
for a in answers:
    print(f"  ✓ {a}")



# Dynamic Fan-Out
from typing import Any

async def embed_document(doc: str) -> list[float]:
    """Simulate calling an embedding API for one document"""
    await asyncio.sleep(0.5)       # each embedding call takes 0.5s
    # In production: return await openai.embeddings.create(input=doc)
    return [0.1, 0.4, 0.9]        # fake embedding vector

async def embed_all_documents(docs: list[str]) -> list[list[float]]:
    """Embed ALL documents concurrently — not one by one"""
    print(f"Embedding {len(docs)} documents concurrently...")

    # This pattern: generate one coroutine per document, run all at once
    embeddings = await asyncio.gather(
        *[embed_document(doc) for doc in docs],   # ← the key pattern
        return_exceptions=True
    )

    # Handle any failures per document
    results = []
    for i, result in enumerate(embeddings):
        if isinstance(result, Exception):
            print(f"  ✗ Document {i} failed: {result}")
            results.append(None)
        else:
            results.append(result)

    return results

# 10 documents — without async: 10 × 0.5s = 5 seconds
# With async: max(0.5s) = 0.5 seconds
docs = [f"Document about topic {i}" for i in range(10)]
embeddings = asyncio.run(embed_all_documents(docs))
print(f"Got {len(embeddings)} embeddings in ~0.5s")



# Creating Background Tasks (Start Now, Collect Later)
async def warm_up_cache(user_id: int) -> dict:
    """Pre-load frequently used data while we do other setup"""
    await asyncio.sleep(2)
    return {"user_id": user_id, "preferences": ["concise", "technical"]}

async def validate_api_keys() -> bool:
    """Check all API keys are valid"""
    await asyncio.sleep(1)
    return True

async def initialise_agent(user_id: int) -> None:
    # Start cache warm-up IMMEDIATELY in background
    # We do not await here — execution continues to the next line
    cache_task = asyncio.create_task(warm_up_cache(user_id))

    # While cache is loading, validate API keys simultaneously
    keys_valid = await validate_api_keys()     # takes 1 second
    print(f"API keys valid: {keys_valid}")

    # NOW collect the cache result — it has been running this whole time
    # If it is already done (2s passed?), returns immediately
    # If not done yet, waits for the remainder
    cache = await cache_task
    print(f"Cache ready: {cache}")

asyncio.run(initialise_agent(user_id=42))



# Structured Concurrency
import asyncio

async def retrieve_from_db(db_name: str) -> list[str]:
    """Retrieve documents from one vector database"""
    await asyncio.sleep(1)
    if db_name == "broken_db":
        raise ConnectionError(f"{db_name} is unreachable")
    return [f"doc from {db_name}"]

async def multi_db_retrieval(query: str) -> None:
    """Retrieve from 3 databases concurrently using TaskGroup"""
    results: list = []

    try:
        async with asyncio.TaskGroup() as tg:
            # Create tasks — they start immediately
            task_pine  = tg.create_task(retrieve_from_db("pinecone"))
            task_weavy = tg.create_task(retrieve_from_db("weaviate"))
            task_bad   = tg.create_task(retrieve_from_db("broken_db"))

        # Code here only runs if ALL tasks succeeded
        # TaskGroup auto-awaits all tasks at the 'async with' exit
        results = task_pine.result() + task_weavy.result()

    except* ConnectionError as eg:
        # except* handles ExceptionGroup — a new Python 3.11 feature
        print(f"Some retrievals failed: {eg.exceptions}")

asyncio.run(multi_db_retrieval("What is a transformer?"))



# Delegating CPU bound tasks to a separate thread within async function
import time

def load_large_file(filepath: str) -> str:
    """Old synchronous function — we cannot change it"""
    time.sleep(2)                    # simulating slow disk read
    return f"Contents of {filepath}"

async def pipeline(query: str) -> None:
    print("Starting pipeline...")

    # Push blocking file load to a worker thread
    # Event loop is FREE during these 2 seconds
    file_contents = await asyncio.to_thread(
        load_large_file,             # the function — do NOT call it, just pass it
        "knowledge_base.txt"         # its argument
    )

    print(f"File loaded: {len(file_contents)} chars")
    print(f"Processing query: {query}")

asyncio.run(pipeline("What is RAG?"))
