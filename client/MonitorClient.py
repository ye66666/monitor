#coding:utf-8

import sys,os
from core import main

base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_dir)
#print base_dir

if __name__ == '__main__':
    server = main.MainClient()
    server.start()
