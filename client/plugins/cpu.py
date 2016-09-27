#coding:utf-8

import commands

def monitor(frist_inval=1):
    shell_command = 'sar 1 3|grep "^Average:"'
    status,result = commands.getstatusoutput(shell_command)
    if status !=0:
        value_dict = {'status':status}
    else:
        value_dict = {}
        user,nice,system,iowait,steal,idle = result.split()[2:]
        value_dict = {
            'user':user,
            'nice':nice,
            'system':system,
            'iowait':iowait,
            'steal':steal,
            'idle':idle,
            'status':status
        }

    return value_dict