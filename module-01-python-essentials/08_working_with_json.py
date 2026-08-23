import json
from pathlib import Path

#Conversion between json and dictionary

d = {
    "name": "Abhishek",
    "skills": ["Java", "AI", "Catia"],
    "completed": [False, False, False]
}
print(type(d))

j = json.dumps(d, indent = 2)
print(type(j))

d2 = json.loads(j)
print(d2["skills"][0])


#Extracting information from json

d = json.loads('{"id": "call_001", "model": "gpt-4", "choices": [{"message": {"role": "assistant", "content": "The answer is 42."}}], "usage": {"prompt_tokens": 10, "completion_tokens": 6}}')
print(d)

model = d["model"]
message = d["choices"][0]["message"]["content"]
tokens = d["usage"]["prompt_tokens"] + d["usage"]["completion_tokens"]

print(f"Model                  : {model}")
print(f"Assistant's message    : {message}")
print(f"Total tokens           : {tokens}")


#Writing and Reading from Disc
BASE_DIR = Path(__file__).resolve().parent
students_file = BASE_DIR / "students.json"

l = [{"name": "Abhishek", "score": 98, "passed": True}, {"name": "Chandan", "score": 84, "passed": True}, {"name": "Anish", "score": 35, "passed": False}]

with open(students_file, "w") as f:
    json.dump(l, f, indent = 2)

with open(students_file, "r") as g:
    d = json.load(g)

print("The Students who Passed:")

for i in d:
    if i["passed"]:
        print(i["name"])
