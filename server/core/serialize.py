#coding:utf-8

import json,time
from conf import hosts


def push_all_config_redis(main_redis,monitored_groups):
    host_config_dict = {}
    for group in monitored_groups:    #循环主机组
        #print group.name
        for h in group.hosts:      #循环主机
            #print host,group.services
            if h not in host_config_dict:    #给每主机配个字典
                host_config_dict[h] = {}

            for s in group.services:      #循环每个主机的监控服务并添加到字典里
                host_config_dict[h][s.name] = [
                    s.plugin_name,
                    s.interval
                ]

    for h,v in host_config_dict.items():
        host_config_key = "HostConfig::%s" % h
        main_redis.r.set(host_config_key,json.dumps(v))

def fetch_all_config(monitored_groups):
    host_config_dict = {}
    for group in monitored_groups:    #循环主机组
        #print group.name
        for h in group.hosts:      #循环主机
            #print host,group.services
            if h not in host_config_dict:    #给每主机配个字典
                host_config_dict[h] = {}

            for s in group.services:      #循环每个主机的监控服务并添加到字典里
                host_config_dict[h][s.name] = s

    for h,v in host_config_dict.items():
        print h,v
    return host_config_dict

def data_process(main_ins):   #处理数据
    print '--going to handle monitor data--'
    all_host_configs = fetch_all_config(hosts.monitored_groups)

    for ip,service_dic in all_host_configs.items():
        for service_name,s_instance in service_dic.items():
            service_redis_key = "ServiceData::%s::%s" % (ip,service_name)
            s_data = main_ins.r.get(service_redis_key)
            if s_data:
                s_data = json.loads(s_data)  #客户端传来的数据
                print '####>',s_data
                #和时间戳、阀值比较
                time_stamp = s_data['time_stamp']
                if time.time() - time_stamp < s_instance.interval:
                    #时间没问题后检查数据是否有效
                    if s_data['data']['status'] == 0: #有效
                        print '\033[31;1mHost[%s] Service[%s] data valid\033[0m' % (ip,service_name)
                        print service_name,s_data['data']
                        for item_key,val_dic in s_instance.triggers.items():
                            service_item_handle(main_ins,item_key,val_dic,s_data)

                    else:
                        print '\033[31;1mHost[%s] Service[%s] plugin error\033[0m' %(ip,service_name)

                else:
                    expird_time = time.time() - time_stamp - s_instance.interval
                    print '\033[31;1mHost[%s] Service[%s] data expired[%s] sece\033[0m' % (ip,service_name,expird_time)


            else:
                print '\033[31;1mNo Data Found in redis for service [%s] host[%s]\033[0m' %(service_name,ip)




def service_item_handle(main_ins,item_key,val_dic,client_service_data):
    print '====>',item_key,client_service_data['data'][item_key]
    #阀值比较
    item_data = client_service_data['data'][item_key]
    warning_val = val_dic['warning']
    critical_val = val_dic['critical']
    oper = val_dic['operator']
    oper_func = getattr(operator,oper)   #材用operator模块来实现比较



    if val_dic['data_type'] is float:
        item_data = float(item_data)

        warning_res = oper_func(item_data,warning_val)
        critical_res = oper_func(item_data,critical_val)

        if critical_res:   #严重的
            print '\033[41;1mCRITICAL::\033[0mHost[%s] Service[%s] 阀值[%s] 当前值[%s]' % (
                client_service_data['host'],client_service_data['service'],critical_val,item_data
            )
        elif warning_res:   #告警
             print '\033[43;WARAING::\033[0mHost[%s] Service[%s] 阀值[%s] 当前值[%s]' % (
                client_service_data['host'],client_service_data['service'],warning_val,item_data
            )

        else:    #正常
            print '\033[43;NORMAL::\033[0mHost[%s] Service[%s] 阀值[%s] 当前值[%s]' % (
                client_service_data['host'],client_service_data['service'],warning_val,item_data
            )