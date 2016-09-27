#coding:utf-8
__author__ = 'ye'

import redishelper
from conf import settings
import json,time
import threading
from plugins import plugin_api


class MainClient(object):
    def __init__(self):
        self.r = redishelper.RedisHelper()
        self.ip = settings.ClientIP
        self.host_config = self.get_host_config()

    def start(self):

        self.handle()

    def get_host_config(self):
        config_key = 'HostConfig::%s' % self.ip
        config = self.r.get(config_key)
        #print config,config_key
        #print self.r.keys()
        if config:      #判断是否存在主机
            config = json.loads(config)

        return config

    def handle(self):

        if self.host_config:
            #print self.host_config
            while True:
                for service,val in self.host_config.items():
                    if len(val) <3:  #确保第一次客户端运行正常,且添加时间戳到字典里
                        self.host_config[service].append(0)
                    plugin_name,interval,last_run_time = val
                    if time.time() - last_run_time < interval:  #和轮循时间对比
                        next_run_time = interval - (time.time()-last_run_time)
                        print 'Service [%s] next run time is in [%s] secs' % (service,next_run_time)
                    else:
                        print '\033[32;1mgoing to run the [%s] again!\033[0m' % service
                        self.host_config[service][2] = time.time()  #更新时间戳

                        #下面启用监控插件
                        t = threading.Thread(target=self.call_plugin,args=(service,plugin_name))
                        t.start()
                time.sleep(1)
        else:

            print "\033[31;1mConnot get host config\033[0m"

    def call_plugin(self,service_name,plugin_name):    #调用监控插件函数
        func = getattr(plugin_api,plugin_name)   #映射获取到函数

        service_data = func()     #获取到插件返回的结果

        #传到服务端
        report_data = {
            'host':self.ip,
            'service':service_name,
            'data':service_data
        }

        self.r.public(json.dumps(report_data))   #把数据序列化发布到服务端
