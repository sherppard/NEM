# -*- coding: utf-8 -*-
# This module is use by cisco device
# function: auto switch to setting mode
# version : 1.0.0
# change date : 2016-10-11
#
# privilege  --> [2960]
# login      --> <2960>


def set_mode( enable_password , current_mode ,*times):
    import re,sys

    print "=="*5 + 'jump: huawei_mode.py'

    ssh_buffer_recv = sys.modules['__main__'].ssh_buffer_recv

    login_pattern = re.compile('\>$')
    enable_pattern = re.compile('\]$')

    output_info = ''

    output_info = ssh_buffer_recv('\n',True,1)
    print 'output === \n' + output_info
    # 下面三行是测试代码
    # ss = login_pattern.search(ssh_buffer_recv('\n'))
    # print ss.group()
    # print current_mode

    if login_pattern.search(ssh_buffer_recv('\n')) and current_mode == 'privilege' :      # 如果 '>' & ']'  -->  ]
        print '1'
        output_info += ssh_buffer_recv('sys?',True,1)

        if re.search('system-view', output_info):
            output_info += ssh_buffer_recv('')
            print output_info
        else:
            output_info += ssh_buffer_recv('super 15')    # super 后面不一定是15
            if re.search('Password', output_info):
                output_info += ssh_buffer_recv(enable_password)
                print output_info

    elif login_pattern.search(ssh_buffer_recv('\n')) and current_mode == 'login' :       # 如果 '>' & '>'  -->   NULL

        output_info += ssh_buffer_recv('sys?',True,1)

        if re.search('system-view', output_info):
            print '2 : ' + "Action: None. Already in login mode."
        else:
            output_info += ssh_buffer_recv('super 15')    # super 后面不一定是15
            if re.search('Password', output_info):
                output_info += ssh_buffer_recv(enable_password)
                print '2 : ' + "Action: None. Enter 'super 15' into login mode."

    elif enable_pattern.search(ssh_buffer_recv('\n')) and current_mode == 'privilege' :    # 如果 ']' & ']'  -->  Null
        print '3 : ' + "Action: None. Already in system-view mode."

    elif enable_pattern.search(ssh_buffer_recv('\n')) and current_mode == 'login' :    # 如果 ']' & '>'  -->  Null , 需要重写
        print '4 : ' + "Action: switch to login mode."
        output_info += ssh_buffer_recv('quit')
        print output_info

    else:
        print '5 : ' + "Error: Unable to determine user privilege status."

    return output_info


