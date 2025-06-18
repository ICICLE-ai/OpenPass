import os
import Helper.globals as globals

# Get current pid
def getPid(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            flask_pid = int(file.read())
            return flask_pid
    return -1


def setPid(filepath, pid):
    with open(filepath, 'w') as file:
        file.write(str(pid))

def checkPid(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True