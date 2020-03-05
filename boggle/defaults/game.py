import os


def read_from_file(filename, type="str"):
    pathname = os.path.join(os.getcwd(), filename)

    with open(pathname, mode="r") as f:
        if type == "str":
            return f.read().strip()

        words = []
        for line in f.readlines():
            words.append(line.strip())
        if type == "set":
            return set(words)

    raise ValueError("Invalid type. Supported types are 'str' and 'set'")
