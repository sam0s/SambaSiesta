#SIESTA PRIME
#sam0s
#10/19/2021

import paramiko
from credentz import *

#Variables to store current working directory
DEFAULT_MEDIA_DIR = '/root/MEDIA_SERVER/'
CURRENT_PATH = []

#Open SSH connection with desired host
ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#these constants are stored in credentz.py for security
ssh_client.connect(hostname=HOSTNAME,username='root',password=HOSTPASS)



#Function that is called during download process
def progress_callback(data_in,data_total):
    mb_in=round((data_in/1000)/1000,2)
    mb_total=round((data_total/1000)/1000,2)#mb
    #calc percentage of download
    percent=int((data_in/data_total)*100)

    #make download progress bar
    progress_bar="["
    progress_bar+=("#"*int(percent/10))
    progress_bar+=(" "*(10-int(percent/10)))
    progress_bar+="]"

    #display download status progress, percentage, and MB
    print(f"{progress_bar} {percent}% ({mb_in}MB / {mb_total}MB)")

def main():
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
        ftp.get(target,file_list[int(cmd[1])].replace('"',''),callback=progress_callback)
        ftp.close()
    if cmd[0].startswith("exit"):
        ssh_client.close()
        return 0
    return 1

while __name__ == '__main__':
    #loop until end condition
    _x=main()
    if _x==0:
        break


#shell
#while True:
#    cmd=input("Command: ")
#    stdin,stdout,stderr=ssh_client.exec_command(cmd)
#    print(stdout.readlines())
