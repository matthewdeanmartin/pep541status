import subprocess


def execute_get_text(command):
    try:
        result = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as err:
        raise

    return result