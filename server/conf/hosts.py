#coding:utf-8

import templates



web_clusters = templates.LinuxGenericTemplate()

web_clusters.hosts = ['192.168.1.1',
                      '192.168.1.11',
                      '192.168.1.101',
                      '172.16.5.5'
                      ]

mysql_groups = templates.Linux2()

mysql_groups.hosts = ['192.168.2.22',
                      '172.16.2.2',
                      '172.16.5.5'

                      ]

monitored_groups = [web_clusters,mysql_groups]

'''

if __name__ == "__main__":

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
        print h,v
'''



