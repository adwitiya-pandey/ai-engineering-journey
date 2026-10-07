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

<!-- PROJECT_STRUCTURE_START -->
## Project Structure

```text
ai-engineering-journey/
├── module-01-python-essentials/
│   ├── 05_first_llm_api_call.py
│   ├── 08_working_with_json.py
│   ├── pyproject.toml
│   ├── students.json
│   └── uv.lock
├── module-02-functions-modular-code/
│   ├── 03_parameters_and_arguments.py
│   ├── 06_lambda_functions.py
│   ├── pyproject.toml
│   └── uv.lock
├── module-03-production-ai/
│   ├── 01_classes_and_OOP_fundamentals.py
│   ├── 02_inheritance_and_method_overriding.py
│   ├── 04_decorators.py
│   ├── 05_generators.py
│   ├── 07_pydantic_basics.py
│   ├── 08_coroutines.py
│   ├── 10_exception_handling.py
│   ├── pyproject.toml
│   └── uv.lock
├── module-05-simple-chatbot/
│   ├── app/
│   │   └── .gitkeep
│   ├── src/
│   │   └── llm_chat/
│   │       ├── providers/
│   │       │   ├── __init__.py
│   │       │   ├── _shared.py
│   │       │   ├── anthropic_provider.py
│   │       │   ├── gemini_provider.py
│   │       │   └── openai_provider.py
│   │       ├── __init__.py
│   │       ├── __main__.py
│   │       ├── cli.py
│   │       ├── client.py
│   │       ├── config.py
│   │       ├── errors.py
│   │       ├── retry.py
│   │       └── validation.py
│   ├── tests/
│   │   ├── test_client.py
│   │   ├── test_retry.py
│   │   └── test_validation.py
│   ├── .python-version
│   ├── project-tree.md
│   ├── pyproject.toml
│   ├── README.md
│   └── uv.lock
├── .gitignore
├── .python-version
├── generate_tree.ps1
├── generate-tree.bat
├── generate-tree.ps1
├── LICENSE
├── pyproject.toml
├── README.md
└── uv.lock
```
<!-- PROJECT_STRUCTURE_END -->

### Updating the Project Structure

Run:

```powershell
generate-tree.bat
```

or:

```powershell
.\generate-tree.ps1
```

The script automatically refreshes the `Project Structure` section of this README.
