# Creating a simple Pydantic model

from pydantic import BaseModel, Field, ValidationError


class RAGDocument(BaseModel):
    doc_id: str
    content: str
    source_url: str | None = None
    relevance_score: float = 0.0
    metadata: dict[str, str] = Field(default_factory=dict)


# Testing
print("--- RAGDocument: Expected Input ---")
valid_doc = RAGDocument(doc_id = "doc_01", content = "Raw text data.")
print(valid_doc.model_dump()) 

print("\n--- RAGDocument: Incorrect Input ---")
try:
    invalid_doc = RAGDocument(doc_id = "doc_02", content = "Data", relevance_score = "High")
except ValidationError as e:
    print(e)


# Creating a nested Pydantic model

class OpenAIMessage(BaseModel):
    role: str
    content: str


class ConversationHistory(BaseModel):
    messages: list[OpenAIMessage]


# Testing
print("\n--- ConversationHistory: Expected Input ---")
msg1 = OpenAIMessage(role = "system", content = "That's a great question.")
msg2 = OpenAIMessage(role = "user", content = "How much wood could a wood?")
msg3 = OpenAIMessage(role = "assistant", content = "Example is great!")

history = ConversationHistory(messages = [msg1, msg2, msg3])

hist = history.model_dump()

for i in hist['messages']:
    for key, value in i.items():
        print(f"{key}: {value}")


print("\n--- ConversationHistory: Incorrect Input ---")
try:
    invalid_history = ConversationHistory(messages=[{"role": "system", "content": "Init"}, {"role": "user"}])
except ValidationError as e:
    print(e)