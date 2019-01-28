# NEM使用指南
cisco、huawei、h3c网络设备管理，类似ansible的用法，支持多线程下发命令，附带其他应用脚本
  
## role 角色

  角色，有三组配置[env]、[commands]、[variable]

**[env]配置**  

  device的参数，与在module的目录下文件名，去掉_mode.py  
  前面的那段文字就是参数，比如 cisco_asa_mode.py  
  device = cisco_asa  

  mode的配置有以下几个参数  
  config     --> 2960(config)#  
  privilege  --> 2960#  
  login      --> <2960>  

**[commands]配置**  
需要用以下格式写入命令   
cmd1 = show run nat  
cmd2 = show run object  
