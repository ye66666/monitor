#coding:utf-8



class BaseService(object):     #基类
    def __init__(self):
        self.name = 'BaseService'  #服务名
        self.interval = 300     #监控间隔
        self.plugin_name = 'your_plugin_name'   #插件名
        self.triggers = {}    #监控阀值