[!] 生产环境谨慎使用！因对本工具的误操作导致的损失，项目作者不承担任何责任
# NEM   [Network Equipment Manage]   使用指南
cisco、huawei、h3c网络设备管理，类似ansible的用法，支持多线程下发命令，附带其他应用脚本  
目前只支持SSH的方式，不支持Telnet, 以后也不会支持telnet，因为不安全

## 运行环境
```
python2.7
依赖包： configparser、paramiko
```

## role 任务

  role 任务，有三组配置[env]、[commands]、[variable]

**1.[env]配置**  

  device的参数，与在module的目录下文件名，去掉`_mode.py`  
  前面的那段文字就是参数，比如 `cisco_asa_mode.py`  
  device = cisco_asa  

  mode的配置有以下几个参数  
  config     --> 2960(config)#  
  privilege  --> 2960#  
  login      --> <2960>  

**2.[commands]配置**  
需要用以下格式写入命令   
cmd1 = show run nat  
cmd2 = show run object  


**3.[variable]配置**  
用法参照role文件夹下的`[huawei-public-key-manage]`


## module 模块  
  
  module 模块，用来确定role的命令在什么样的环境执行  
  比如是特权模式，或者是配置模式下，输入命令后保存的脚本等  
  根据你的需要进行编写，目前支持cisco、cisco asa、huawei的设备  
  
## hosts 主机列表  
  
  两种类型的参数：  
  `[login_xxxx] ` 账号、密码、特权密码，格式如下： 
```
username = admin
password = 12345678
privPass = 12345678
```

  `[xxxx]` 主机列表，格式如下：  
```
host1 = 172.16.13.252
host2 = 172.16.13.251
host3 = 172.16.13.250
```

  举例：  
  `[login_cisco]`与`[cisco]`没有必然联系  
  只需要在`config`里面配置对应的`run`与`login`
  
## config 配置  

```
  [run_config]  
  run            = cisco                     ; 运行哪些主机     --> hosts -->  cisco  
  login          = login_cisco               ; 登录的账号密码组 -->  hosts -->  login_cisco  
  command-set    = cisco-public-key-manage   ; 运行哪一套命令集 -->  role/cisco-public-key-manage  
  save_config    = yes / no                  ; 是否保存配置  
  debug          = open / close              ; 是否开启调试功能  
```



## script 任务启动脚本
```
F:\PycharmProjects\NEM-master>python script.py --help
usage: script.py [-h] [-c CONFIG] [--config CONFIG] [--version]

NE2M 是一个类似ansible的工具，但是NE2M只负责管理网络设备，不支持操作系统的管理。
它只是要求的简单，易用，不仅可以在工作中使用，而且还可以供学习网络设备操作。

optional arguments:
  -h, --help       show this help message and exit
  -c CONFIG        specificed your config file path to run NE2M.
  --config CONFIG  specificed your config file path to run NE2M.
  --version        show program's version number and exit

例如：
python script.py -c config/ASA_port_mapping_config
```


## output 输出  
任务执行后，全部命令执行过程都进行记录，用于排错  
输出文件的命名规则： [date日期]_[role任务名称].txt  
例如：`2016-10-15_cisco-core-DHCPsnooping.txt`  
  
