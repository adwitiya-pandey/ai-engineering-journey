# Simulating RAG chunking in its simplest form

def chunk_text(text, chunk_size):
    for start in range(0, len(text), chunk_size):
        yield text[start : start + chunk_size]


for i in chunk_text("Hello World this is AI engineering", 5):
    print(i)



# Simulating an LLM's word by word response

import time

def simulate_llm_stream(response: str):
    words = response.split()

    for word in words:
        time.sleep(0.2)
        yield word

# Test:
text = "The old brass clock on the mantelpiece ticked with a steady, hypnotic rhythm that seemed to swallow the afternoon quiet. Outside the frosted window, autumn leaves danced in a frantic swirl before settling into the damp corners of the brick pathway. A faint scent of roasted coffee beans drifted from the kitchen, breaking the stillness of the empty room and reminding anyone passing by of simple, quiet comforts."

for word in simulate_llm_stream(text):
    print(word, end=" ", flush=True)
