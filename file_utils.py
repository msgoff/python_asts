def listfiles(folder, file_type=False, skip_venv=True):
    import os
    import re

    for root, folders, files in os.walk(folder):
        for filename in folders + files:
            if bool(skip_venv):
                # need a better test for python venv
                if not re.findall(
                    r"/venv/bin/|/python\d+.*?/site-packages|/lib/python\d+.\d+",
                    root + filename,
                ):
                    if bool(file_type):
                        if bool(filename.endswith(file_type)):
                            yield os.path.join(root, filename)
                    else:
                        if not os.path.isdir(root + filename):
                            yield os.path.join(root, filename)
            else:
                if bool(file_type):
                    if bool(filename.endswith(file_type)):
                        yield os.path.join(root, filename)
                else:
                    if not os.path.isdir(root + filename):
                        yield os.path.join(root, filename)


def read_file(filename):
    # https://github.com/jendrikseipp/vulture
    # vulture - Find dead code.
    # Python >= 3.2
    import tokenize

    try:
        # Use encoding detected by tokenize.detect_encoding().
        with tokenize.open(filename) as f:
            return f.read()
    except (SyntaxError, UnicodeDecodeError) as err:
        print(err)


def get_file_type(filename):
    # https://stackoverflow.com/a/24073625
    import subprocess
    import shlex

    cmd = shlex.split("file --mime-type {0}".format(filename))
    result = subprocess.check_output(cmd)
    mime_type = result.split()[-1]
    return mime_type


def get_file_checksum(file_name):
    try:
        import hashlib

        f = open(file_name, "rb")
        data = f.read()
        f.close()
        m = hashlib.md5()
        m.update(data)
        return {file_name: m.hexdigest()}
    except Exception as e:
        print(e)


def mkdir(path):
    import os

    try:
        os.mkdir(path)
    except Exception as e:
        print(e)


def copy_file_named_checksum(file_name, folder_name, file_type):
    import os
    import shutil

    new_file_name = list(get_file_checksum(file_name).values())[0] + ".{}".format(
        file_type
    )
    cwd = os.getcwd()
    copy_path = cwd + "\\" + folder_name + new_file_name
    try:
        print(file_name, copy_path)
        shutil.copy(file_name, copy_path)
    except Exception as e:
        print(e)
