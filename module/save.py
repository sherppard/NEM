# -*- coding: utf-8 -*-
# This module is use by cisco device
# function: auto switch to setting mode
# version : 1.0.0
# change date : 2016-10-11
#
# privilege  --> [2960]
# login      --> <2960>


def save(device_type, host):

    print '=='*5+'jump to save.py'

    import sys
    exec("import module."+ device_type +"_mode as check_mode")

########## 检查模式
    set_mode = check_mode.set_mode
    password = sys.modules['__main__'].privPass
    cisco_save_mode = 'privilege'
    huawei_save_mode = 'login'
    output_info = ''

    ssh_buffer_recv = sys.modules['__main__'].ssh_buffer_recv

    n = host[-3:]
    m = 'ssh_shell_' + n

    shell = eval("sys.modules['__main__']." + m)

########## 根据设备类型输出保存指令
    if device_type == 'cisco':
        output_info += set_mode(host, password, cisco_save_mode, 2)
        output_info += ssh_buffer_recv(shell, 'write', False, 8)

    elif device_type == 'huawei':
        output_info += set_mode(host, password, huawei_save_mode, 2)
        output_info += ssh_buffer_recv(shell, 'save\nY',False,8)

    return output_info




