log_function_calls = True


def write_file(file_name, data):
    from time import time

    with open(file_name, "a+") as f:
        f.write(str(time()))
        f.write("\t")
        f.write(data)
        f.write("\n")


def function_calls(func):
    if log_function_calls:

        def fcall(*args, **kwargs):
            write_file("function_calls", "{},{},{}".format(func.__name__, args, kwargs))

        return fcall
    else:
        return func


"""
@function_calls
def test(*args,**kwargs):
    return 1+1

test(1)
"""
