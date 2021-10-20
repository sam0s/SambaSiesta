#SIESTA PRIME
#sam0s
#10/19/2021

import paramiko
from credentz import *

DEFAULT_MEDIA_DIR = '/root/MEDIA_SERVER/'
CURRENT_PATH = []


ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=HOSTNAME,username='root',password=HOSTPASS)





while True:
    p=DEFAULT_MEDIA_DIR+('/'.join(CURRENT_PATH))
    print(p)
    stdin,stdout,stderr=ssh_client.exec_command(f"cd {p};ls")
    file_list = ['"'+i.strip()+'"' for i in stdout]
    for i in  enumerate(file_list):
        print(i[0],i[1].replace('"',''))
    cmd=input("command: ").split(" ")
    if cmd[0].startswith("nav"):
        CURRENT_PATH.append(file_list[int(cmd[1])])
    if cmd[0].startswith("back") and len(CURRENT_PATH)>0:
        CURRENT_PATH.pop()
    if cmd[0].startswith("play"):
        target = (p+"/"+file_list[int(cmd[1])]).replace('"','')
        ftp=ssh_client.open_sftp()

        ftp.chdir(DEFAULT_MEDIA_DIR)
        ftp.get(target,file_list[int(cmd[1])].replace('"',''))
        ftp.close()
    if cmd[0].startswith("exit"):
        ssh_client.close()
        break



#shell
#while True:
#    cmd=input("Command: ")
#    stdin,stdout,stderr=ssh_client.exec_command(cmd)
#    print(stdout.readlines())
