#coding:utf-8

from services import linux

class BaseTemplate(object):
    def __init__(self):
        self.name = 'your template name'
        self.hosts = []
        self.services = []


class LinuxGenericTemplate(BaseTemplate):
    def __init__(self):
        super(LinuxGenericTemplate,self).__init__()
        self.name = 'LinuxCommonServices'
        self.services = [
            linux.CPU(),
            linux.Memory(),
            #linux.Network()
        ]

class Linux2(BaseTemplate):
    def __init__(self):
        super(Linux2,self).__init__()
        self.name = 'Linux2'
        self.services = [
            linux.CPU(),
            #linux.Memory(),
            linux.Network()
        ]
