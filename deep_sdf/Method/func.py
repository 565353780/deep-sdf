from typing import Union
from subprocess import Popen, DEVNULL

def runCMD(cmd: Union[str, list]) -> bool:
    subproc = Popen(cmd, stdout=DEVNULL)
    subproc.wait()
    return True

def processMesh(mesh_filepath, target_filepath, executable, additional_args) -> bool:
    command = [executable, "-m", mesh_filepath, "-o", target_filepath] + additional_args
    return runCMD(command)
