# AI Engineering Journey

A hands-on portfolio documenting progress through a self-designed 24-module (v4) AI engineering curriculum, from Python fundamentals to production AI systems.

## Curriculum index

This index lists the module folders currently present in the repository.

| Module | Folder | What it proves | Status |
| --- | --- | --- | --- |
| 01 | [module-01-python-essentials](./module-01-python-essentials/) | Python fundamentals, JSON handling, and a first LLM API call | In progress |
| 02 | [module-02-functions-modular-code](./module-02-functions-modular-code/) | Function parameters, arguments, and lambda expressions | In progress |
| 03 | [module-03-production-ai](./module-03-production-ai/) | Object-oriented Python, decorators, generators, validation, coroutines, and exception handling | In progress |
| 05 | [module-05-simple-chatbot](./module-05-simple-chatbot/) | A tested, modular multi-provider chatbot with validation and retry handling | In progress |

## How to run a module

Each module is an independent uv project. From the repository root, enter a module folder, sync its dependencies, and run the relevant command:

```powershell
cd <module-folder>
uv sync
uv run <module-command>
```

The command varies by module; check that module's files for its runnable scripts or tests.
