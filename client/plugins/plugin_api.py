#coding:utf-8
__author__ = 'ye'



import cpu  #导入插件


def get_cpu_status():   #这些函数名和服务端传来的service一样

    return cpu.monitor()


def get_mem_status():
    #return memory.monitor()
    pass