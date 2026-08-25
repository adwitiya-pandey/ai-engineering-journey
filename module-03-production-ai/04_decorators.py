# Implementing Sanity Check for Input

import functools

def check_not_empty(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            first_arg = args[0]
        elif kwargs:
            first_arg = next(iter(kwargs.values()))
        else:
            first_arg = ""

        # Check if the first argument is an empty string
        if first_arg == "":
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
print(summarise(text="The sky is light blue."))


# Validating the input value of a function through a decorator


def validate_score(min_val: float, max_val: float):
    """
    Decorator factory that validates whether the first argument of the
    decorated function falls within [min_val, max_val] (inclusive).
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Determine the value of the first argument
            if args:
                score = args[0]
            elif kwargs:
            # If passed via keyword argument, take the first keyword value
                score = next(iter(kwargs.values()))
            else:
                raise ValueError("Expected at least one argument to validate.")

            # Validate range
            if not (min_val <= score <= max_val):
                raise ValueError(
                    f"Score {score} is out of range. Expected a value between {min_val} and {max_val} (inclusive)."
                )

            return func(*args, **kwargs)
        return wrapper
    return decorator


@validate_score(min_val=0, max_val=100)
def record_accuracy(accuracy: float) -> str:
    return f"Model accuracy recorded: {accuracy}%"


# --- Testing the decorator ---

# 1. Valid test cases
print(record_accuracy(95.5))            # Positional arg
print(record_accuracy(0))               # Lower bound
print(record_accuracy(100))             # Upper bound
print(record_accuracy(accuracy=88.2))   # Keyword arg

# 2. Invalid test cases
test_invalid_scores = [-5.0, 105.0]

for invalid_score in test_invalid_scores:
    try:
        record_accuracy(invalid_score)
    except ValueError as e:
        print(f"Caught expected error: {e}")
