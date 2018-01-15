# -*- coding: utf-8 -*-
# This module is use by cisco device
# function: auto switch to setting mode
# version : 1.0.0
# change date : 2016-10-11
#
# config     --> 2960(config)#
# privilege  --> 2960#
# login      --> <2960>

def print_all(module_):
    modulelist = dir(module_)
    length = len(modulelist)
    for i in range(0,length,1):
        print modulelist[i] + ' : ' + str(getattr(module_, modulelist[i]))




def set_mode( host , enable_password , current_mode , *times):
    import re,sys

    #print '='*80
    #print_all(sys.modules['__main__'])

    debug = sys.modules['__main__'].debug

    if debug == 'open':
        print "==" * 5 + 'jump: cisco_mode.py'

    n = host[-3:]
    m = 'ssh_shell_' + n

    shell = eval( "sys.modules['__main__']." + m )

    ssh_buffer_recv = sys.modules['__main__'].ssh_buffer_recv

    #print sys.modules['__main__']


    login_pattern = re.compile('\>$')
    enable_pattern = re.compile('#$')

    # 下面三行是测试代码
    # ss = login_pattern.search(ssh_buffer_recv('\n'))
    # print ss.group()
    # print current_mode

    output_info = ssh_buffer_recv( shell, '\n', True, 1)



    ### !!!!!!!!!! 下面这段是一个地雷，
    if times:
        if times[0] == 1:
            hostname = re.search(r'\r\n.*[>#]', output_info)
            hostname = hostname.group().strip('>')
            hostname = hostname.strip()
            hostname = hostname + '#'
            exec("sys.modules['__main__'].hostname_" + n + " = hostname")

        elif times[0] == 2:
            exec("hostname = sys.modules['__main__'].hostname_" + n )
    ### !!!!!!!!!! 到这里

    login = login_pattern.search(output_info)
    enable = enable_pattern.search(output_info)

    if login and current_mode == 'privilege' :      # 如果 '>' & '#'  -->  #
        output_info += ssh_buffer_recv( shell, 'enable')
        output_info += ssh_buffer_recv( shell, 'terminal length 0')
        if re.search('Password', output_info):
            output_info += ssh_buffer_recv( shell, enable_password)
            if debug == 'open':
                print '0001：goto privilege mode - 2960#'
                print output_info

    elif login and current_mode == 'config' :       # 如果 '>' & '(config)#'  -->   (config)#
        output_info += ssh_buffer_recv( shell, '\n'+ 'en')
        output_info += ssh_buffer_recv( shell, 'terminal length 0')
        if debug == 'open':
            print output_info
        if re.search('Password', output_info):
            output_info += ssh_buffer_recv( shell, enable_password)
            output_info += ssh_buffer_recv( shell, 'config terminal')          # 需要改成变量
            if debug == 'open':
                print '0002：goto privilege mode - 2960(config)#'
                print output_info

    elif login and current_mode == 'login' :       # 如果 '>' & '>'  -->   NULL
        print '0003 : ' + "Action: None. Already in login mode."

    elif enable and current_mode == 'privilege' :    # 如果 '#' & '#'  -->  Null

        print '0004: '+ hostname   # !!!!!!
        if hostname in output_info:
            output_info += ssh_buffer_recv( shell, 'terminal length 0')
        if re.search('\(config\)#', output_info):
            pass
        else:
            while True:
                #print output_info
                output_info += ssh_buffer_recv( shell, 'exit')
                if re.search(hostname, output_info):
                    break


        print '0004 : ' + "Action: None. Already in enable mode."

    elif enable and current_mode == 'config' :       # 如果 '#' & '(config)#'  -->   (config)#
        output_info += ssh_buffer_recv( shell, 'terminal length 0')
        output_info += ssh_buffer_recv( shell, 'config terminal')
        print '0005'

    else:
        print '0006 : ' + "Error: Unable to determine user privilege status."

    return output_info

