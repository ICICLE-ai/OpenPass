import sys
import io
from contextlib import redirect_stdout

import Helper.globals as globals

def CopyMSFrom(port, ms_name, src_path, dst_path):
    sys.argv = [
        "mscopy.py", "--port", str(port),
        f"{ms_name}:{src_path}", dst_path
    ]
    mscopy_path = f"{globals.cgi_path}/mscopy.py"

    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        with open(mscopy_path, "r") as script_file:
            exec(script_file.read())
    
    output = output_buffer.getvalue()
    return ("DONE" in output)

def CopyMSTo(port, ms_name, src_path, dst_path):
    sys.argv = [
        "mscopy.py", "--port", str(port),
        src_path, f"{ms_name}:{dst_path}"
    ]
    mscopy_path = f"{globals.cgi_path}/mscopy.py"

    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        with open(mscopy_path, "r") as script_file:
            exec(script_file.read())

    output = output_buffer.getvalue()
    return ("DONE" in output)