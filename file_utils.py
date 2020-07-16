def listfiles(folder):
    import os
    for root, folders, files in os.walk(folder):
        for filename in folders + files:
            if filename.endswith('.py'):
                yield os.path.join(root, filename)


def read_file(filename):
    #https://github.com/jendrikseipp/vulture
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
    #https://stackoverflow.com/a/24073625
    import subprocess
    import shlex
    cmd = shlex.split('file --mime-type {0}'.format(filename))
    result = subprocess.check_output(cmd)
    mime_type = result.split()[-1]
    return mime_type