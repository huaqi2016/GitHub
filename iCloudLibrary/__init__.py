#coding:utf-8
from db_process import db_process
from excel_process import excel_process
from http_process import http_process
from general_process import general_process
__author__ = 'zhoushengqiang'
version = '1.0'

class iCloudLibrary(excel_process, db_process, http_process, general_process):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

