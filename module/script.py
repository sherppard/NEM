# -*- coding: utf-8 -*-
#!/usr/bin/env python
import paramiko
import time,datetime
import configparser

def readConfig(config_file,option,index):
    configData = configparser.ConfigParser()
    configData.read(config_file)
    value = configData.get(option,index)
    return value

def readOption(config_file,option):
    configData = configparser.ConfigParser()
    configData.read(config_file)
    lists = configData.options(option)
    return lists

# 扩展的变量替换特性，可以跨section去获取变量
def readExtend(config_file,option,index):
    configData = configparser.ConfigParser()
    configData._interpolation = configparser.ExtendedInterpolation()
    configData.read(config_file)
    value = configData.get(option,index)
    return value

def ssh_buffer_recv(command,*enter):
    # command 不能为空
    # *enter 接收两个参数 True Or False ,  delay
    # （True,1） 不敲回车
    # （False,10） 敲回车，命令执行等10秒延迟

    import time

    delay = 1

    # 读取script模块的变量方法
    # import sys
    # ssh_shell = sys.modules['__main__'].ssh_shell

    if enter:  # 不敲回车
        if enter[0]== True :
            ssh_shell.sendall(command)
        else:  # enter参数不为空时敲回车
            ssh_shell.sendall(command + "\n")
    else:   # enter参数为空时敲回车
        ssh_shell.sendall(command + "\n")

    not_done = True
    output = ""
    #self.clear_buffer()

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

hostname = ''

if __name__=='__main__':


    date = datetime.datetime.now().strftime("%Y-%m-%d")

################# config
    run_hosts = readConfig('config','run_config','run')
    login_info = readConfig('config','run_config','login')
    command_set = readConfig('config','run_config','command-set')
    output = readConfig('config','run_config','folder')
    name = readConfig('config','run_config','filename')
    save_config = readConfig('config','run_config','save_config')

################# hosts
    username = readConfig('hosts',login_info,'username')
    password = readConfig('hosts',login_info,'password')
    privPass = readConfig('hosts',login_info,'privPass')

    hkeys = readOption('hosts', run_hosts)
    length = len(hkeys)

    all_hosts = []
    for i in range(0,length):
        all_hosts.append(readConfig('hosts', run_hosts ,hkeys[i]))

    print all_hosts

################### command

    mode = readConfig('role/'+command_set,'env','mode')
    device = readConfig('role/'+command_set,'env','device')

    ckeys = readOption('role/'+command_set,'commands')
    length = len(ckeys)

    all_cmds = []
    for i in range(0,length):
        #globals()[ckeys[i]] = readExtend('command','commands',ckeys[i])
        #print globals()[ckeys[i]]
        all_cmds.append(readExtend('role/'+command_set,'commands',ckeys[i]))

################### 导入设备模式模块
    print mode
    print device
    exec("import module."+ device +"_mode as check_mode")


#####################################################
###                开始执行任务                   ###
#####################################################

    for host in all_hosts:
        splitWord = '-'*60+'\n'+'-'*23+host+'-'*23+'\n'+'-'*60+'\n'
        print splitWord

########### 登录交换机
        #paramiko.util.log_to_file('paramiko.log')
        s=paramiko.SSHClient()
        #s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname = host,username=username, password=password)
        ssh_shell = s.invoke_shell()

########### 进入预设模式
        get_data = ''
        get_data += check_mode.set_mode ( privPass , mode , 1 )

########### 敲命令
        for cmd in all_cmds:
            res = ssh_shell.sendall( cmd.strip() + '\n')
            time.sleep(float(1))
            #print ssh_shell.recv(14024)
            get_data = get_data + ssh_shell.recv(14024)

########### 导入配置保存模块
        if save_config == 'yes':
            exec("import module.save as check_save")
            get_data += check_save.save(device)

        wrip=open(output+"/"+date+"_"+name+".txt",'a+')
        wrip.write(splitWord +'\n')
        wrip.write(get_data +'\n')
        wrip.close()
##
        s.close()
