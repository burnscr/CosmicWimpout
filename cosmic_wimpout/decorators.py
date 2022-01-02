from functools import wraps


def validate_choice(valid_range=None):
    """Ensures the return value is an int within the specified range

    If `valid_range` is set as None, the validator will only
    ensure the return value is an int. No range will be enforced.

    If the value returned by the decorated function is invalid, the
    message "Invalid choice!" will be printed to the console and the
    decorated function will be called again. This repeats until the
    return value is valid.

    :param valid_range: range to enforce the return value with.  [default None]
    :return: an int constrained by the `valid_range`
    """
    def decorator(func):
        @wraps(func)
        def validator(*args, **kwargs):
            while True:
                result = func(*args, **kwargs)
                try:
                    choice = int(result)
                    # we only want to perform validation
                    #  if a valid range was specified
                    if valid_range is not None:
                        if choice not in valid_range:
                            print('Invalid choice!')
                            continue
                    return choice
                # if anything other than a ValueError is
                #  raised, it should not be suppressed
                except ValueError:
                    print('Invalid choice!')
        return validator
    return decorator
