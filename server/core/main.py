__author__ = 'yejianlin'

import redishelper
import serialize
from conf import hosts
import json,time,threading

class MainServer(object):
    def __init__(self):
        self.r = redishelper.RedisHelper()
        self.r.set("name",'kobe')
        self.save_config_to_redis()
        #print self.r.get('name')
        print self.r.keys()
    def start(self):
        self.data_handle()
        self.handle()

    def save_config_to_redis(self):
        serialize.push_all_config_redis(self,hosts.monitored_groups)

    def handle(self):   #接收客户端传来的数据
        chan_sub = self.r.subscribe()
        while True:
            hos_service_data = chan_sub.parse_response()
            hos_service_data = json.loads(hos_service_data[2])

            hos_service_data['time_stamp'] = time.time()

            service_data_key = 'ServiceData::%s::%s' % (hos_service_data['host'],hos_service_data['service'])
            self.r.set(service_data_key,json.dumps(hos_service_data))  #把数据存到redis

    def data_handle_run(self):
        serialize.data_process(self)

    def data_handle(self):
        '处理监控数据，独立线程'
        t =threading.Thread(target=self.data_handle_run)
        t.start()

    def alert_handle(self):
        '处理报警信息，独立线程'


