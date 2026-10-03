# Trying the try-except-else-finally block

import json


def safe_parse_llm_response(raw_string: str):
    try:
        result = json.loads(raw_string)
        response = result["answer"]
    except json.JSONDecodeError:
        print("The JSON is malformed.")
        return None
    except KeyError:
        print("The key 'answer' does not exist.")
        return None
    else:
        print("Successfully parsed response")
    finally:
        print(
            "Parsing attempt complete"
        )  # finally runs even after else has triggered return

    return response


print(safe_parse_llm_response('{"answer": "Paris is the capital of France"}'))
print("=" * 80)
print(safe_parse_llm_response("not valid json at all"))
print("=" * 80)
print(safe_parse_llm_response('{"question": "What is the capital?"}'))
print("=" * 80)
