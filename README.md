# NEM使用指南
cisco、huawei、h3c网络设备管理，类似ansible的用法，支持多线程下发命令，附带其他应用脚本
  
## role 任务

  role 任务，有三组配置[env]、[commands]、[variable]

**1.[env]配置**  

  device的参数，与在module的目录下文件名，去掉_mode.py  
  前面的那段文字就是参数，比如 cisco_asa_mode.py  
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
参照role文件夹下的[huawei-public-key-manage]


## module 模块  
  
  module 模块，是用来确定role的命令在什么样的环境执行  
  比如是特权模式，或者是配置模式下，输入命令后保存的脚本等  
  根据你的需要进行编写，目前支持cisco、cisco asa、huawei的设备
  
## hosts 主机列表  
  
  hosts 主机列表
  

## config 配置  

  config 配置
  
  [run_config]  
  run            = cisco                     ; 运行哪些主机  
  login          = login_cisco               ; 登录的账号密码组  
  command-set    = cisco-public-key-manage   ; 运行哪一套命令集  
  save_config    = yes / no                  ; 是否保存配置  
  debug          = open / close              ; 是否开启调试功能  


## script 任务启动脚本







