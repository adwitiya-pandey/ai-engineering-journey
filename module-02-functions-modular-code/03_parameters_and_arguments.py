# Introduces self with name and optional hobby
def introduce_yourself(name, hobby = "learning Python"):
    print(f"Hi, I am {name} and I enjoy {hobby}")

introduce_yourself("Alice")
introduce_yourself("Bob", hobby="playing chess")
print("-" * 20)

# Calculates and prints total of given prices
def calculate_total(*args):
    print("Total Bill:", sum(args))

calculate_total(15, 20.50, 5)
calculate_total(100, 200, 300, 400)
print("-" * 20)


# Prints agent name and each config setting
def create_agent_config(agent_name, **kwargs):
    print("Agent's Name:", agent_name)
    for key, value in kwargs.items():
        print(key, value)

create_agent_config("AlphaBot", memory="16GB", role="Assistant")
create_agent_config("DataMiner", mode="Scraping", threads=4, timeout=30)
print("-" * 20)


# Flexible report: subjects, grade, extra info
def flexible_report(student_name, *args, grade = "B", **kwargs):
    print(f"{student_name} of grade {grade} has taken the subjects {args}.")
    for key, value in kwargs.items():
        print(key, value)

flexible_report("Charlie", "Math", "Physics", grade="A", attendance="95%", conduct="Good")
flexible_report("Diana", "History", "Art")
print("-" * 20)


# Prints name, total and average of scores
def summarise_scores(student_name, *args):
    print(student_name)
    print(f"Total Score: {sum(args)} / {len(args) * 100}")
    print("Average Score:", sum(args) / len(args))

summarise_scores("Abhishek", 98, 94)
summarise_scores("Abhishek", 98, 94, 96)
summarise_scores("Abhishek", 98, 94, 100, 97)
print("-" * 20)


# Prints task and kwargs as key:value
def build_prompt(task, **kwargs):
    print(task)
    for key, value in kwargs.items():
        print(f"{key}: {value}")

build_prompt("Summarize the text", length="short", tone="professional")
build_prompt("Translate to Spanish", formal=True)
print("-" * 20)


# Flexible call_llm prints prompt, model, kwargs
def call_llm(prompt, model = "gemini-3.6-flash", **kwargs):
    print(f"Prompt: {prompt}")
    print(f"Model: {model}")
    for key, value in kwargs.items():
        print(f"{key}: {value}")

call_llm("What is an ant?")
call_llm("What is an ant?", "claude-mythos5")
call_llm("What is an ant?", "claude-mythos5", temperature = 0.98, max_tokens = 1024, language = 'English')
