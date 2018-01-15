# -*- encoding: utf-8 -*-
import re
import sys
import xlwt
import datetime
import os


def txt_obId(filename):

    a = open(filename)
    b = open('./port_map/obId.txt', 'a+')

    temp = 0

    null_line = re.compile(r'^\r')

    for (num, value) in enumerate(a):
        if 'show run object' in value:
            temp = num

        if temp:
            if num > temp:
                m = null_line.search(value)
                if m:
                    break
                b.write(value)

    a.close()
    b.close()


def txt_portMap(filename):

    a = open(filename)
    b = open('./port_map/portMap.txt', 'a+')

    temp = 0

    null_line = re.compile(r'^\r')

    for (num, value) in enumerate(a):
        if '!' in value:    #  之前的写法  if 'show run nat' in value:
            temp = num

        if temp:
            if num > temp:
                m = null_line.search(value)
                if m:
                    break
                b.write(value)

    a.close()
    b.close()


def txt_obId_2(filename):

    a = open(filename,'r')
    b = open('./port_map/obId_2.txt', 'a+')

    null_line2 = re.compile(r'\n$')
    start_null = re.compile(r'^\s')
    start_service = re.compile(r'^\sservice')

    for (num, value) in enumerate(a):

        y = start_service.search(value)
        x = start_null.search(value)
        if x:                           # 把开头空格的部分删除
            if 'description' in value:  # 开头为空，同时有description，不写入这行
                pass
            elif y:                     # 空格service 开头的行不写
                pass
            else:
                value_proc = start_null.sub(' ', value)
                b.write(value_proc)
        elif x == None :                         # 把末尾的回车符删除
            if 'object service' in value:        # 不写入 object service 的行
                pass
            else:
                replaceedStr = null_line2.sub('', value)
                print replaceedStr
                b.write(replaceedStr)

    a.close()
    b.close()


def txt_portMap_2(filename):

    a = open(filename,'r')
    b = open('./port_map/portMap_2.txt', 'a+')

    null_line2 = re.compile(r'\n$')
    start_null = re.compile(r'^\s')

    for (num, value) in enumerate(a):

        x = start_null.search(value)
        if x:                           # 把开头空格的部分删除
            if 'dynamic' in value:
                pass
            else:
                value_proc = start_null.sub(' ', value)
                b.write(value_proc)
        else:                         # 把末尾的回车符删除
            if 'internet' in value:
                pass
            else:
                replaceedStr = null_line2.sub('', value)
                print replaceedStr
                b.write(replaceedStr)

    a.close()
    b.close()


def txt_portMap_3(filename):

    a = open(filename,'r')
    b = open('./port_map/portMap_3.txt', 'a+')

    temp = []
    group = []

    for (num, value) in enumerate(a):
        # 分割后转换为列表
        group = value.split(' ', 5)
        temp.append(group)

    # 排序
    mySort2(temp, 3)

    for i in temp:
        str = ' '
        back_group = str.join(i)  # 重组回行
        b.write(back_group)

    a.close()
    b.close()


def txt_portMap_4(filename):

    a = open(filename,'r')
    b = open('./port_map/portMap_4.txt', 'a+')

    # 替换一些字符串
    remove_front = re.compile(r'^object\snetwork\s')
    replace_int = re.compile(r'interface')
    replace_www = re.compile(r'www')
    replace_https = re.compile(r'https')

    for (num, value) in enumerate(a):
        value_proc = remove_front.sub('', value)
        value_proc = replace_int.sub('202.105.128.58', value_proc)
        value_proc = replace_www.sub('80', value_proc)
        value_proc = replace_https.sub('443', value_proc)


        b.write(value_proc)

    a.close()
    b.close()


def txt_portMap_5(filename):

    a = open(filename,'r')
    b = open('./port_map/portMap_5.txt', 'a+')

    temp = []
    group = []

    for (num, value) in enumerate(a):
        # 分割后转换为列表
        group = value.split(' ',8)
        temp.append(group)

    # 排序
    mySort2(temp, 4)

    for i in temp:
        str = ' '
        back_group = str.join(i)  # 重组回行
        b.write(back_group)

    a.close()
    b.close()


def txt_obId_3(filename):

    a = open(filename,'r')
    b = open('./port_map/obId_3.txt', 'a+')

    for (num, value) in enumerate(a):

        if 'subnet' in value:
            pass
        else:
            b.write(value)

    a.close()
    b.close()

def txt_obId_4(filename):

    a = open(filename,'r')
    b = open('./port_map/obId_4.txt', 'a+')

    temp = []
    group = []

    for (num, value) in enumerate(a):
        # 分割后转换为列表
        group = value.split(' ',5)
        temp.append(group)

    # 排序
    mySort2(temp,2)

    for i in temp:
        str = ' '
        back_group = str.join(i)  #重组回行
        b.write(back_group)

    a.close()
    b.close()

def txt_obId_5(filename):

    a = open(filename,'r')
    b = open('./port_map/obId_5.txt', 'a+')

    remove_front = re.compile(r'^object\snetwork\s')
    remove_middle = re.compile(r'\shost\s')

    for (num, value) in enumerate(a):

        value_proc = remove_front.sub('', value)
        value_proc = remove_middle.sub('\t', value_proc)

        b.write(value_proc)

    a.close()
    b.close()

def mySort2(A, indexCol = 0):

    N_Col = len(A[0])

    # indexCol 应该总是小于 N_Col
    # indexCol 第几列
    # N_Col 表的列数
    if indexCol < 0:
        indexCol = 0
    elif indexCol >= N_Col:
        indexCol = 0

    if indexCol != 0:
        for H in range(len(A)):
            # 每行的第一列数据与目的列数据交换，交换位置后方便sort函数直接调用
            (A[H][0], A[H][indexCol]) = (A[H][indexCol], A[H][0])

    A.sort(reverse=True)

    if indexCol != 0:
        for H in range(len(A)):
            # 排序完成后，第一列的数据回到原来的位置
            (A[H][0], A[H][indexCol]) = (A[H][indexCol], A[H][0])

def obj_to_json(filename):

    obj_json = {}
    a = open(filename, 'r')

    for (num, value) in enumerate(a):
        # 分割后转换为列表
        line = value.split('\t', 1)
        obj_json[line[0]] = line[1].strip()

    return obj_json

def write_to_excel(filename):

    a = open(filename, 'r')

    group = []
    data = xlwt.Workbook()
    table = data.add_sheet('Port Mapping', cell_overwrite_ok=True)

    # 首行样式
    style = xlwt.easyxf('alignment: horiz centre; '
                        'font: bold on, color red; '
                        'borders: left medium, top medium, bottom medium')

    # 0行用来初始化 列的含义
    table.write(0, 0, 'Protocol', style)
    table.write(0, 1, 'Object Name', style)
    table.write(0, 2, 'Inside IP', style)
    table.write(0, 3, 'Direction', style)
    table.write(0, 4, 'Inside Port', style)
    table.write(0, 5, 'Internet IP', style)
    table.write(0, 6, 'Outside Port', style)
    table.write(0, 7, 'Department', style)
    table.write(0, 8, 'Owner', style)
    table.write(0, 9, 'Usage', style)
    table.write(0, 10, 'Open Time', style)

    x = 1    # 行数
    y = 1    # 列数

    obj_json = obj_to_json('./port_map/obId_5.txt')

    for (num, value) in enumerate(a):
        # 分割后转换为列表
        line = value.split(' ', 8)
        # 再加入到group列表，group存放了整个表的数据
        group.append(line)

    # 写入表格前的准备
    merge_style = xlwt.easyxf('alignment: horiz centre, vert centre; '
                              'font: bold on; '
                              'borders: left thin, top thin, bottom thin, right thin')

    temp_Protocol = 0

    for line in range(len(group)):
        '''group[line]为每行的数据['abc','123','2012-11-11']
           Protocol、obId、insideIP...为每一行一列的数据，'abc'
           前面加 ‘_’ 是需要合并的列
        '''

        _Protocol = group[line][6].strip()

        if line == 0:
            c0r1 = line + 1
        elif beforePro == _Protocol:
            c0r2 = line + 1
            if line == len(group) - 1:
                '''
                最后一行跟前面一行的IP地址是相同的情况下
                只能做line数值如果到最后一行了，就执行合并单元格的操作'''
                table.write_merge(c0r1, c0r2, 0, 0, beforePro, merge_style)
        else:
            table.write_merge(c0r1, c0r2, 0, 0, beforePro, merge_style)
            c0r1 = c0r2 + 1

        beforePro = _Protocol


        obId = group[line][0]
        table.write(x, 1, obId.strip(), merge_style)


        _insideIP = obj_json.get(obId.strip())
        _insideIP = _insideIP.strip()

        if line == 0:
            c2r1 = line + 1
        elif before == _insideIP:
            c2r2 = line + 1
            if line == len(group) - 1:
                '''
                最后一行跟前面一行的IP地址是相同的情况下
                只能做line数值如果到最后一行了，就执行合并单元格的操作'''
                table.write_merge(c2r1, c2r2, 2, 2, before, merge_style)
        else:
            # 第一次就遇到两个IP都不相同的情况，c2r2还没来得及定义，就会报错
            if c2r2:
                # 对于连续三行IP不同的情况，c2r2会小于c2r1
                # 此时会报出 assert Error的异常
                if c2r2 < c2r1:
                    c2r2 = c2r1

                table.write_merge(c2r1, c2r2, 2, 2, before, merge_style)
                c2r1 = c2r2 + 1
            else:
                c2r2 = c2r1
                table.write_merge(c2r1, c2r2, 2, 2, before, merge_style)
                c2r1 = c2r2 + 1

            if line == len(group) - 1:
                c2r2 = c2r1
                '''
                最后一行跟前面一行的IP地址是相同的情况下
                只能做line数值如果到最后一行了，就执行合并单元格的操作'''
                table.write_merge(c2r1, c2r2, 2, 2, _insideIP, merge_style)

        before = _insideIP

        direction = group[line][2]
        table.write(x, 3, direction.strip(), merge_style)

        insidePort = group[line][7]
        table.write(x, 4, insidePort.strip(), merge_style)

        _outsideIP = group[line][4].strip()

        if line == 0:
            c5r1 = line + 1
        elif beforeIP == _outsideIP:
            c5r2 = line + 1
            if line == len(group) - 1:
                '''
                最后一行跟前面一行的IP地址是相同的情况下
                只能做line数值如果到最后一行了，就执行合并单元格的操作'''
                table.write_merge(c5r1, c5r2, 5, 5, beforeIP, merge_style)
        else:
            table.write_merge(c5r1, c5r2, 5, 5, beforeIP, merge_style)
            c5r1 = c5r2 + 1

        beforeIP = _outsideIP

        outsidePort = group[line][8]
        table.write(x, 6, outsidePort.strip(), merge_style)

        x += 1  # 行数加一

    # 设置列的宽度
    table.col(0).width = 256 * (10 + 1)
    table.col(1).width = 256 * (25 + 1)
    table.col(2).width = 256 * (15 + 1)
    table.col(3).width = 256 * (10 + 1)
    table.col(4).width = 256 * (10 + 1)
    table.col(5).width = 256 * (15 + 1)
    table.col(6).width = 256 * (12 + 1)
    table.col(7).width = 256 * (13 + 1)
    table.col(10).width = 256 * (10 + 1)

    a.close()
    data.save(date + '_PortMap' + '.xls')


if __name__ == "__main__":

    # 判断路径是否存在，不存在创建改文件夹
    workpath = './port_map'

    if not os.path.exists(workpath):
        os.makedirs(workpath)

    # 删除port_map下的所有文件
    temp_files = os.listdir('./port_map')

    for i in temp_files:
        os.remove('./port_map/' + i)

    # 执行任务
    today = datetime.date.today()
    date = today.strftime("%Y-%m-%d")

    txt_obId(date + '_port_mapping.txt')
    txt_obId_2('./port_map/obId.txt')
    txt_obId_3('./port_map/obId_2.txt')
    txt_obId_4('./port_map/obId_3.txt')
    txt_obId_5('./port_map/obId_4.txt')

    txt_portMap(date + '_port_mapping.txt')
    txt_portMap_2('./port_map/portMap.txt')
    txt_portMap_3('./port_map/portMap_2.txt')
    txt_portMap_4('./port_map/portMap_3.txt')
    txt_portMap_5('./port_map/portMap_4.txt')

    write_to_excel('./port_map/portMap_5.txt')



