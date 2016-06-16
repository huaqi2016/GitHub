# -*- coding: utf-8 -*-

import json
from excel_process import excel_process
import time
import urllib
import urllib2
import re
import sys
import datetime
import copy
__author__ = 'zhoushengqiang'

header = '{"Authorization":"Bearer 01f0132df1e2b4ab1742053382bc6ec6"}'
rets=[]
rest=[]
class http_process(object):
    def __init__(self):
        pass

    def general_data(self, fp):
        exp = excel_process()
        req_bodys = exp.readExcel(fp)
        return req_bodys

    def health_data(self, fp, tab):
        excel_data=[]  #读取的excel数据
        detailsList=[] #不加detail头的detail数据
        general_dict={"distance":144.0, "endTime":2, "energy":32.69, "startTime":1, "steps":206, "type":6, "userId":300}
        tempDict={} #加了detail头的detail数据
        gbody={}     #加了general的数据
        gbodys=[]    #request列表
        bodys=[]    #三个detail作为一个request
        ret={}
        expList=[]
        exp= excel_process()
        excel_data=exp.readExcelExp(fp, tab)
        for i in excel_data.keys(): #excel三行数据组成一个detail
            detailsList.append(excel_data[i])
            expList.append(i)
        for i in range(len(detailsList)):
            t=[]
            t.append(detailsList[i])
            tempDict["details"] = t
            gbody = dict(tempDict, **general_dict)    #两个dict相加
            gbodys.append(gbody.copy())
        for i in range(0, len(gbodys), 1):  # 三个detail作为一个request
            bodys.append(gbodys[i:i+1])
        for body in bodys:
            ret["data"]=body
            rets.append(ret.copy())
        reqbody = dict(zip(expList, rets))
        return reqbody

    def help_data(self, fp, tab):
        excel_data=[]  #读取的excel数据
        detailsList=[] #不加detail头的detail数据
        tempDict={} #加了detail头的detail数据
        gbody={}     #加了general的数据
        gbodys=[]    #request列表
        bodys=[]    #三个detail作为一个request
        expList=[]
        exp= excel_process()
        excel_data=exp.readExcelExp(fp, tab)
        for k in excel_data.keys():
            if excel_data[k].has_key('timestamp'):
                excel_data[k]['timestamp'] = ((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds())*1000
            gbodys.append(excel_data[k])
            expList.append(k)
        ret = dict(zip(expList, gbodys))
        print ret
        return ret

    def user_json_data(self, fp, tab):
        excel_data=[]  #读取的excel数据
        detailsList=[] #不加detail头的detail数据
        tempDict={} #加了detail头的detail数据
        gbody={}     #加了general的数据
        gbodys=[]    #request列表
        bodys=[]    #三个detail作为一个request
        expList=[]
        exp= excel_process()
        excel_data=exp.readExcelExp(fp, tab)
        print excel_data
        for k in excel_data.keys():
            print json.dumps(excel_data[k])
            gbody["detailJson"]=json.dumps(excel_data[k])
            gbodys.append(gbody.copy())
            expList.append(k)
        ret = dict(zip(expList, gbodys))
        print ret
        return ret

    def suggest_data(self, fp, tab):
        excel_data=[]  #读取的excel数据
        detailsList=[] #不加detail头的detail数据
        tempDict={} #加了detail头的detail数据
        gbody={}     #加了general的数据
        gbodys=[]    #request列表
        bodys=[]    #三个detail作为一个request
        expList=[]
        exp= excel_process()
        excel_data=exp.readExcelExp(fp, tab)
        for k in excel_data.keys():
            t=[]
            t.append(excel_data[k])
            gbody["data"]=json.dumps(t)
            gbodys.append(gbody.copy())
            expList.append(k)
        ret = dict(zip(expList, gbodys))
        print ret
        return ret

    def iCloud_http_general(self, req_url, req_bodys, header, methods):
        '''
        9icloud
        '''
        global rest
        #hp=http_process()
        for req_body in req_bodys:
            print req_body
            rest=self.http_general(req_url, req_body, header, methods)
        print rest
        return rest

    def http_general(self, req_url, req_body, header, methods):
        if req_body is None:
            test_data_urlencode = None
        else:
            test_data_urlencode = urllib.urlencode(req_body)
            test_data_urlencode = test_data_urlencode.encode('utf-8')
            #print "REQ BODY IS %s"%test_data_urlencode

        headerdata = json.loads(header)
        req = urllib2.Request(url=req_url, data=test_data_urlencode, headers=headerdata)
        req.get_method = lambda : methods   #等价于 return methods
        res_data = urllib2.urlopen(req)
        res = res_data.read().decode('utf-8')
        print res
        return res

    def icloud_get_urllib(self, req_url, headkey, headvalue):
        request= urllib2.Request(req_url)
        #request.add_header('Authorization', 'Bearer 01f0132df1e2b4ab1742053382bc6ec6')
        request.add_header(headkey, headvalue)
        res_data=urllib2.urlopen(request)
        res = res_data.read().decode('utf-8')
        time.sleep(3)
        return res

    def process_encode(self, body):
        keys=[]
        values=[]
        for k in body.keys():
            if isinstance(body[k], unicode):
                keys.append(k)
                values.append(body[k].encode('utf-8'))
            else:
                keys.append(k)
                values.append(str(body[k]).decode('utf-8'))
        #print dict(zip(keys, values))
        return dict(zip(keys, values))

    def http_exp(self, url, path, tab, header, methods):
        retList=[]
        if path in [None, '']:
            response=self.http_general(url, None, header, methods)
            return response
        ep = excel_process()
        dicts=ep.readExcelExp(path, tab)
        '''
        reg=re.compile('/help/user/save|/help/data/push|/help/record/save')
        m=reg.search(url)
        if m is not None:
            dicts=self.help_data(path, tab)
        '''
        reg=re.compile('/health/user/suggest')
        n=reg.search(url)
        if n is not None:
            dicts=self.suggest_data(path, tab)

        reg=re.compile('/users/detail')
        p=reg.search(url)
        if p is not None:
            dicts=self.user_json_data(path, tab)
        for k in dicts.keys():
            print '-------------------------------------------'
            print dicts[k]   ###这个log不要删

            dicts[k]=self.process_encode(dicts[k])

            response=self.http_general(url, dicts[k], header, methods)
            m=re.search(str(k[2:5]), response)  #str(k[2:5])  ---> 10200变成200
            print 'EXPECT result is %s'%str(k[2:5])
            if m is not None:
                print "SUCCESS"
                retList.append('SUCCESS')
            else:
                print "FAILED"
                retList.append('FAILED')
        print retList
        return retList

    def http_help(self, url, path, tab, header, methods):
        retList=[]
        if path in [None, '']:
            response=self.http_general(url, None, header, methods)
            return response
        dicts=self.help_data(path, tab)
        for k in dicts.keys():
            print '-------------------------------------------'
            test_data_urlencode=json.dumps(dicts[k])
            print test_data_urlencode  ###这个log不要删
            header='{"Authorization":"Bearer 01f0132df1e2b4ab1742053382bc6ec6", "Content-Type":"application/json"}'
            headerdata = json.loads(header)
            req = urllib2.Request(url=url, data=test_data_urlencode, headers=headerdata)
            req.get_method = lambda : methods   #等价于 return methods
            res_data = urllib2.urlopen(req)
            response = res_data.read().decode('utf-8')
            print response
            m=re.search(str(k[2:5]), response)  #str(k[2:5])  ---> 10200变成200
            print 'EXPECT result is %s'%str(k[2:5])
            if m is not None:
                print "SUCCESS"
                retList.append('SUCCESS')
            else:
                print "FAILED"
                retList.append('FAILED')
        print retList
        return retList

    def http_health_save(self, url, path, tab, header, methods):
        '''
        健康服务接口：数据存储服务专用API
        :param url:
        :param path:
        :param tab:
        :param header:
        :param methods:
        :return:
        '''
        retList=[]
        dicts=self.health_data(path, tab)
        print dicts
        for k in dicts.keys():
            print '-------------------------------------------'
            l1=[]
            l2=[]
            tmpd=dicts[k]['data'][0]['details'][0]
            #l1=[x.encode(sys.stdout.encoding) for x in tmpd.keys()]
            l1=[x.encode('utf-8') for x in tmpd.keys()]
            for v in tmpd.values():
                l2.append(int(v))
            d= dict(map(None, l1, l2))

            dicts[k]['data'][0]['details'].pop(0)
            dicts[k]['data'][0]['details'].append(d)
            dicts[k]['data'][0]['startTime']=((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds())*1000
            dicts[k]['data'][0]['endTime']=((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds())*1000
            dicts[k]['data']=str(dicts[k]['data']).replace("'", '"')
            print dicts[k]    ###这个log不要删
            test_data_urlencode = urllib.urlencode(dicts[k])
            test_data_urlencode = test_data_urlencode.encode('utf-8')
            headerdata = json.loads(header)
            req = urllib2.Request(url=url, data=test_data_urlencode, headers=headerdata)
            req.get_method = lambda : methods   #等价于 return methods
            res_data = urllib2.urlopen(req)
            res = res_data.read().decode('utf-8')
            print res
            m=re.search(str(k[2:5]), res)  #str(k[2:5])  ---> 10200变成200
            print 'EXPECT result is %s'%str(k[2:5])
            if m is not None:
                print "SUCCESS"
                retList.append('SUCCESS')
            else:
                print "FAILED"
                retList.append('FAILED')
        print retList
        return retList

    def add_dict(self, d1, d2):
        d={}
        d=dict(d1, **d2)
        return d

if __name__ == '__main__':
    hp=http_process()
    #hp.http_help('http://192.168.22.61/v1/help/data/push', 'E:\\script\\test\\robotframework\\case\\help.xlsx', 'push', header, 'POST')
    #hp.http_help('http://192.168.22.61/v1/help/user/save', 'E:\\script\\test\\robotframework\\case\\help.xlsx', 'save', header, 'POST')
    #hp.http_health_save('http://192.168.22.61/v1/health/data/save', 'E:\\script\\test\\robotframework\\case\\health_data.xlsx', 'save', header, 'POST')
    #hp.http_exp('http://192.168.22.61/v1/health/user/suggest', 'E:\\script\\test\\oauth\\case\\health_suggest_type_5.xlsx', 'suggest', header, 'POST')
    hp.http_exp('http://192.168.22.61/v1/users/detail', 'E:\\script\\test\\robotframework\\case\\user.xlsx', 'modifyinfo', header, 'PUT')