# -*- coding: utf-8 -*-

import xlrd
import xlwt
import re
import datetime
import os
import time
from xlutils.copy import copy

def fetch_data(sw_type):
    # 未使用
    if sw_type == 'core':
        os.system('cd C:\Users\DELL\Desktop\github\NE2M\ && script.py --config .\config\core_correlation_config')
    elif sw_type == 'access':
        os.system('cd C:\Users\DELL\Desktop\github\NE2M\ && script.py --config .\config\correlation_config')

def mac_colon(mac):
    # 将excel里面的mac地址转换为冒号格式
    colon_mac = mac.upper()
    if '-' in mac:
        colon_mac = colon_mac.replace('-', ':')
    elif '.' in mac:
        colon_mac = colon_mac.replace('.','')
        num1 = colon_mac[0:2]
        num2 = colon_mac[2:4]
        num3 = colon_mac[4:6]
        num4 = colon_mac[6:8]
        num5 = colon_mac[8:10]
        num6 = colon_mac[10:12]
        str = ':'
        seq = (num1, num2, num3, num4, num5, num6)
        colon_mac = str.join(seq)
    return colon_mac

def mac_dotted(mac):
    # 将excel里面的mac地址转换为点分格式
    if '-' in mac:
        dotted_mac = mac.replace('-', '')
        dotted_mac = dotted_mac.lower()
        num1 = dotted_mac[0:4]
        num2 = dotted_mac[4:8]
        num3 = dotted_mac[8:12]
        str = '.'

        seq = (num1, num2, num3)
        dotted_mac = str.join(seq)
    elif '.' in mac:
        dotted_mac = mac
    return dotted_mac

def snoop_belong_sw(line_data):
    #通过dhcp snooping的信息去查找所属交换机，目前并未使用

    if 'GigabitEthernet1/0/47' in line_data:
        return 'sw5'

    num = filter_funtion('sw', line_data)
    num = num.replace('Port-channel','')

    num = 'sw' + num
    return num

def belong_sw(line_data):
    # 通过show mac address-table的主机名字去确定所属交换机
    # 这里最好用正则表达式匹配，否则XYJ-C2960_10 与 XYJ-C2960_1 会有冲突

    if 'XYJ-C2960_2' in line_data:
        return 'sw2'
    elif 'XYJ-C2960_3' in line_data:
        return 'sw3'
    elif 'XYJ-C2960_4' in line_data:
        return 'sw4'
    elif 'XYJ-C2960poe_5' in line_data:
        return 'sw5'
    elif 'XYJ-C2960p24_6' in line_data:
        return 'sw6'
    elif 'XYJ-C2960_7' in line_data:
        return 'sw7'
    elif 'XYJ-C2960_8' in line_data:
        return 'sw8'
    elif 'XYJ-C2960_9' in line_data:
        return 'sw9'
    elif 'XYJ-C2960_10' in line_data:
        return 'sw10'
    elif 'XYJ-C2960_11' in line_data:
        return 'sw11'
    elif 'XYJ-C2960_12' in line_data:
        return 'sw12'
    elif 'XYJ-C2960_13' in line_data:
        return 'sw13'
    elif 'XYJ-C2960_1' in line_data:
        return 'sw1'
    else:
        return None

def Fetch_ip(arp, snooping):

    ip_address1 = filter_funtion('ip', arp).strip()
    ip_address2 = filter_funtion('ip', snooping).strip()

    if ip_address1 and ip_address2:
        if ip_address1 == ip_address2:
            ip = ip_address1
        else:
            ip = ip_address2
    elif ip_address1:
        ip = ip_address1
    elif ip_address2:
        ip = ip_address2
    else:
        ip = ''

    return ip

def Fetch_vlan(arp, snooping):

    vlan = filter_funtion('vlan', arp)

    if vlan:
        vlan = vlan.replace('n', 'n ')
        vlan = vlan.strip()
        return vlan
    else:
        vlan = filter_funtion('vlan_snoop', snooping)
        vlan = vlan.strip()
        return vlan


def filter_funtion(do_what, line_data):
    # 过滤功能，提供多少数据处理，找出mac地址对于的IP、IP地址属性、vlan号、接口编号、交换机编号

    if do_what == 'ip':
        pattern = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line_data)
        try:
            data = pattern.group()
        except AttributeError:
            data = ''

    elif do_what == 'attr':
        pattern = re.search(r'dhcp', line_data)
        try:
            data = pattern.group()
        except AttributeError:
            data = 'fixed'

    elif do_what == 'vlan':
        pattern = re.search(r'Vlan\d{1,4}', line_data)
        if pattern:
            data = pattern.group()
        else:
            data = ''

    elif do_what == 'vlan_snoop':
        pattern = re.search(r'\s\d{1,4}\s', line_data)
        if pattern:
            data = 'Vlan' + pattern.group()
        else:
            data = ''

    elif do_what == 'int':
        pattern = re.search(r'\s[^\s]+$', line_data.strip())
        data = pattern.group()

    elif do_what == 'sw':
        pattern = re.search(r'Port-channel\d{1,2}', line_data.strip())
        data = pattern.group()

    #except UnboundLocalError:
    return data



date = datetime.datetime.now().strftime("%Y-%m-%d")

file_path1 = 'C:/Users/DELL/Desktop/github/NE2M/output/correlation_table/' + date + '_correlation_arp_dhcp_snooping.txt'
file_path2 = 'C:/Users/DELL/Desktop/github/NE2M/output/correlation_table/' + date + '_correlation_mac_address.txt'

while True:
    if os.path.exists(file_path1):
        # 判断当天的信息是否导出，
        # 如果导出，就执行下面的操作
        # 如果未导出，就用cmd去执行NE2M脚本导出
        # 打开核心交换机输出信息，里面有arp、dhcp snooping信息
        table = open(file_path1, 'r')
        all_data = table.readlines()
        break
    else:
        os.system('cd C:\Users\DELL\Desktop\github\NE2M\ && script.py --config .\config\core_correlation_config')

while True:
    if os.path.exists(file_path2):
        # 判断当天的信息是否导出，
        # 如果导出，就执行下面的操作
        # 如果未导出，就用cmd去执行NE2M脚本导出
        # 打开接入层交换机输出信息，里面有mac地址表信息
        access_sw_table = open(file_path2, 'r')
        access_sw_data = access_sw_table.readlines()
        break
    else:
        os.system('cd C:\Users\DELL\Desktop\github\NE2M\ && script.py --config .\config\correlation_config')


# 打开excel表格
mac_address = xlrd.open_workbook(u'C:\\Users\\DELL\\Desktop\\详细工作项\\加固计划\\关联表\\关联表.xls', formatting_info=True)
line = mac_address.sheet_by_name( u'关联表' )

print '总行数： ' + str(line.nrows)

# 将表格复制一份，用于将下面获取的信息写入表格
newb = copy(mac_address)
l = newb.get_sheet(0)

for i in range(1, line.nrows):
    # 读取excel表格每行数据
    data = line.row_values(i)

    # 读取mac地址列的值
    x = 6
    mac = data[x]

    # 读取上一次的ip地址值
    y = 5
    last_ip = data[y].strip()

    # 读取规划ip地址的值，用于确定是否写入公式
    z = 11
    assign_ip = data[z].strip()

    if mac:

        colon_mac = mac_colon(mac)
        dotted_mac = mac_dotted(mac)

        ip_address = ''
        sw_num = ''

        snooping_info = ''
        arp_info = ''
        # 本次mac地址匹配的时候，清空snooping_info，否则就按上一次的值使用

        int_num = ''
        int_info = ''  # int_info的作用域，判断错误。。。。

        for p in range(0, len(all_data)):
            # 读取核心交换机输出的每行信息
            if colon_mac in all_data[p]:
                print '\nHere is raw data:'
                print all_data[p]
                snooping_info = all_data[p]
                break
            else:
                snooping_info = ''

        for q in range(0, len(all_data)):
            if dotted_mac in all_data[q]:
                print all_data[q]
                arp_info = all_data[q]
                break
            else:
                arp_info = ''

        for j in range(0, len(access_sw_data)):
            # 读取接入层交换机输出的每行信息
            x = belong_sw(access_sw_data[j])
            if x:
                sw_num = x
            if dotted_mac in access_sw_data[j]:
                int_info = access_sw_data[j]
                int_num = filter_funtion('int', int_info).strip()
                break
                # 这里匹配接口号之后，就应该退出检索，否则sw_num的值不准
            if j == len(access_sw_data) - 1 :
                # 如果到最后一行都没有匹配到，就将sw_num设为空值
                if int_info == '':
                    sw_num = ''

        # sw_num = belong_sw(snooping_info)
        # 判断一下内容是否为空，如果为空应该如何处理？
        # arp 刷新时间研究，dhcp 租约时间研究
        ip_address = Fetch_ip(arp_info, snooping_info)
        ip_attr = filter_funtion('attr', snooping_info)
        vlan_info = Fetch_vlan(arp_info, snooping_info)


        # 到这里，所有数据获取完成，输出调试信息
        print '这是第 ' + str(i) +' 行'
        print '\nMAC地址: ' + str(mac) + '的其他关联信息如下...'
        print '交换机编号： ' + sw_num
        print 'IP地址： ' + ip_address
        print 'IP地址属性： ' + ip_attr
        print 'Vlan信息： ' + vlan_info
        print '接口编号：' + int_num

        update_time = time.strftime("%Y/%m/%d %H:%M", time.localtime())

        '''
        # 数据获取完成后，写入到excel表里面去
        l.write(i, 4, ip_attr)
        l.write(i, 5, ip_address)
        l.write(i, 9, vlan_info)
        l.write(i, 7, sw_num)
        l.write(i, 8, int_num)
        l.write(i, 14, update_time)
        '''

        if ip_address and vlan_info:
            # ip地址与vlan号是与的关系，他们是一对的存在
            # 如果没有获取到ip地址与vlan号，更不用谈接口编号了
            l.write(i, 5, ip_address)
            l.write(i, 9, vlan_info)

            if sw_num and int_num:
                # 交换机号与接口编号是与关系，他们也是一对的存在
                # 获取到这两个编号后，就可以对获取的时间进行更新
                l.write(i, 7, sw_num)
                l.write(i, 8, int_num)
                l.write(i, 14, update_time)

        if ip_address == '' and last_ip == '' :
            # 获取不到ip地址，上次ip地址为空，ip地址属性就为空
            ip_attr = ''
            l.write(i, 4, ip_attr)
        elif ip_address == '' and last_ip:
            # 获取不到ip地址，有上次ip地址，就什么都不做，保留之前的值
            pass
        elif ip_address:
            # 获取到了，就写入ip地址属性
            l.write(i, 4, ip_attr)

        if assign_ip:
            # 注意使用公式的时候，不要加上=符号
            # 只有规划好ip地址的用户，才需要进行比对操作
            l.write(i, 12, xlwt.Formula('IF(F' + str(i + 1) + '=L' + str(i + 1) + ',"","1")'))
            l.write(i, 13, xlwt.Formula('IF(J' + str(i + 1) + '=K' + str(i + 1) + ',"","1")'))


# 保存对excel表格的更改
try:
    newb.save(u'C:\\Users\\DELL\\Desktop\\详细工作项\\加固计划\\关联表\\关联表.xls')
    print '\n已经成功写入数据!'
except IOError:
    print '\n报错啦!!!'
    print '关联表已经被你用EXCEL打开了，保存不了，请关闭excel。'