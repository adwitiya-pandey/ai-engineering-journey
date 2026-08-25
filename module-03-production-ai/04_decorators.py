# Implementing Sanity Check for Input

import functools

def check_not_empty(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not args[0]:
            print("Error: Input cannot be empty.")
        else:
            result = func(*args, **kwargs)
            return result
    return wrapper

@check_not_empty
def summarise(text: str) -> str:
    return "Summary: " + text


print(summarise(''))
print(summarise('What a nice day!'))
print(summarise.__name__)