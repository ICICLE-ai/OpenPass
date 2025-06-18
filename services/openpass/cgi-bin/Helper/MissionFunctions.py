#!/usr/bin/python3

import os
import signal
import time
import subprocess

import Helper.globals as globals


def getMissionCMD(mission_file, output_file, image_folder, params):
    mission_path = f'{globals.cgi_path}/Missions/{mission_file}'
    
    cmd = ['python3', mission_path, output_file, image_folder]
    cmd += params
   
    return cmd

def stopPrevMission(output_path=None):
    if os.path.exists(globals.current_mission_pid_path):
        #print("<br> Found File")
        with open(globals.current_mission_pid_path, 'r') as pid_file:
            pid = int(pid_file.read().strip())
            #print(f"<br> PID: {pid}")
            
            try:
                os.kill(pid, signal.SIGTERM)
                #print(f"<br> Killed {pid}")
                time.sleep(globals.wait)
            except OSError:
                #print("<br> No previous mission or failed to kill previous mission")
                pass
    
    if (output_path is not None) and (os.path.exists(output_path)):
        os.remove(output_path)

def startMission(mission_file, output_file, image_folder, params):
    output_path = f'{globals.htdocs_path}/{output_file}'

    stopPrevMission(output_path)

    cmd = getMissionCMD(mission_file, output_file, image_folder, params)
    process = subprocess.Popen(cmd,
                 stdin=subprocess.DEVNULL,
                 stdout=subprocess.DEVNULL,
                 stderr=subprocess.DEVNULL,
                 start_new_session=True,
                 preexec_fn=(lambda: signal.signal(signal.SIGHUP, signal.SIG_IGN)))
    
    with open(globals.current_mission_pid_path, 'w') as pid_file:
        pid_file.write(str(process.pid))

    return process

if __name__ == '__main__':
    stopPrevMission()