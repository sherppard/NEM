# -*- coding: utf-8 -*-
#!/usr/bin/env python


import datetime
import os,sys
import time
import threading

import configparser,argparse
import paramiko

def ensure_dir(name):
    d = os.path.dirname(name)
    if not os.path.exists(d):
        os.makedirs(d)


def readConfig(config_file, option, index):
    configData = configparser.ConfigParser()
    configData.read(config_file)
    value = configData.get(option, index)
    return value


def readOption(config_file, option):
    configData = configparser.ConfigParser()
    configData.read(config_file)
    lists = configData.options(option)
    return lists


def readExtend(config_file, option, index):
    # 扩展的变量替换特性，可以跨section去获取变量
    configData = configparser.ConfigParser()
    configData._interpolation = configparser.ExtendedInterpolation()
    configData.read(config_file)
    value = configData.get(option, index)
    return value


def ssh_buffer_recv( ssh_shell, command, *enter):
    """ command 不能为空
     *enter 接收两个参数 True Or False ,  delay
     （True,1） 不敲回车
     （False,10） 敲回车，命令执行等10秒延迟 """

    delay = 1

    # 读取script模块的变量方法
    # import sys
    # ssh_shell = sys.modules['__main__'].ssh_shell

    if enter:  # 不敲回车
        if enter[0]:
            ssh_shell.sendall(command)
        else:  # enter参数不为空时敲回车
            ssh_shell.sendall(command + "\n")
    else:   # enter参数为空时敲回车
        ssh_shell.sendall(command + "\n")

    not_done = True
    output = ""
    # self.clear_buffer()

    if enter:
        if enter[1] > 1:
            delay = enter[1]

    while not_done:
        time.sleep(float(delay))
        if ssh_shell.recv_ready():
            output += ssh_shell.recv(65535)
        else:
            not_done = False
    return output



def do_mission(f_host, f_user, f_passwd):

    print 'host %s mission start at %s .' % (f_host, time.ctime())

    # ########## 登录交换机
    # paramiko.util.log_to_file('paramiko.log')
    s = paramiko.SSHClient()
    # s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname=f_host, username=f_user, password=f_passwd)
    #global ssh_shell
    #ssh_shell = s.invoke_shell()
    n = f_host[-3:]
    m = 'ssh_shell_' + n
    globals()[m] = s.invoke_shell()

    o = 'hostname_' + n
    globals()[o] = ''



    # ########## 进入预设模式
    get_data = ''
    get_data += check_mode.set_mode( f_host, privPass, mode, 1)

    # ########## 敲命令
    for cmd in all_cmds:
        res = globals()[m].sendall(cmd.strip() + '\n')     # ssh_shell -->  globals()[m]
        time.sleep(float(1))
        # print ssh_shell.recv(14024)
        get_data = get_data + globals()[m].recv(65535)     # ssh_shell -->  globals()[m]

    # ########## 导入配置保存模块
    if save_config == 'yes':
        exec ("import module.save as check_save")
        get_data += check_save.save(device, f_host)

    if debug == 'open':
        print get_data

    ensure_dir('./'+output)

    hostnames = eval(o + ".rstrip('#')  ")
    print hostnames + ': Finished.'


    # ########## 将输出内容导出到文件
    wrip = open(output + "/" + date + "_" + name + ".txt", 'a+')
    wrip.write(splitWord + '\n')
    get_data = get_data.replace("\r\n", "\n")
    wrip.write(get_data + '\n')
    wrip.close()

    s.close()

    print 'host %s mission finished at %s .' % (f_host, time.ctime())

_ne2m_des = '''
NE2M 是一个类似ansible的工具，但是NE2M只负责管理网络设备，不支持操作系统的管理。
它只是要求的简单，易用，不仅可以在工作中使用，而且还可以供学习网络设备操作。
'''

argObj = argparse.ArgumentParser(description=_ne2m_des)

argObj.add_argument('-c', dest='config', action='store', help='specificed your config file path to run NE2M.')
argObj.add_argument('--config', dest='config', action='store', help='specificed your config file path to run NE2M.')
argObj.add_argument('--version', action='version', version='NE2M v1.0.0')

recv_arg = argObj.parse_args()

if recv_arg.config:
    config_path = recv_arg.config
else:
    config_path = '.\config\ASA_port_mapping_config'
    #config_path = '.\config\core_correlation_config'

# 当天时间
date = datetime.datetime.now().strftime("%Y-%m-%d")

# ################ config
run_hosts   = readConfig(config_path, 'run_config', 'run')
login_info  = readConfig(config_path, 'run_config', 'login')
command_set = readConfig(config_path, 'run_config', 'command-set')
output      = readConfig(config_path, 'run_config', 'folder')
name        = readConfig(config_path, 'run_config', 'filename')
save_config = readConfig(config_path, 'run_config', 'save_config')
debug       = readConfig(config_path, 'run_config', 'debug')

# ################ hosts
username = readConfig('hosts', login_info, 'username')
password = readConfig('hosts', login_info, 'password')
privPass = readConfig('hosts', login_info, 'privPass')

hkeys = readOption('hosts', run_hosts)
length = len(hkeys)

all_hosts = []
for i in range(0, length):
    all_hosts.append(readConfig('hosts', run_hosts, hkeys[i]))

print all_hosts

# ################## command

mode = readConfig('role/'+command_set, 'env', 'mode')
device = readConfig('role/'+command_set, 'env', 'device')

ckeys = readOption('role/'+command_set, 'commands')
length = len(ckeys)

all_cmds = []
for i in range(0,length):
    # globals()[ckeys[i]] = readExtend('command','commands',ckeys[i])
    # print globals()[ckeys[i]]
    all_cmds.append(readExtend('role/'+command_set, 'commands', ckeys[i]))

# ################## 导入设备模式模块
print mode
print device
exec("import module." + device + "_mode as check_mode")


# ####################################################
# ##                装载多线程任务                  ###
# ####################################################

threads = []

for host in all_hosts:
    splitWord = '-'*60+'\n'+'-'*23+host+'-'*23+'\n'+'-'*60+'\n'
    print splitWord

    t = threading.Thread(target=do_mission, args=(host, username, password))
    threads.append(t)
    #t.currentThread()

# 启动多线程任务

for i in threads:
    i.setDaemon(True)
    i.start()
    time.sleep(0.2)       # 加入顺序执行，最粗暴的方法
    threading.currentThread()

for i in threads:
    i.join()



print 'all mission compelete!'

