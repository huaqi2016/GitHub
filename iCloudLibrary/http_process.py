#coding=utf-8

import json
from excel_process import excel_process
import time
import urllib
import urllib2
import re
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

    def health_data(self, fp):
        excel_data=[]  #读取的excel数据
        detailsList=[] #不加detail头的detail数据
        general_dict={"distance":144.0, "endTime":1459853880000, "energy":32.69, "startTime":1459853460000, "steps":206, "type":6}
        tempDict={} #加了detail头的detail数据
        gbody={}     #加了general的数据
        gbodys=[]    #request列表
        bodys=[]    #三个detail作为一个request
        exp= excel_process()
        excel_data=exp.readExcel(fp)
        for i in range(0, len(excel_data), 1): #excel三行数据组成一个detail
            detailsList.append(excel_data[i:i+1])
        for i in range(len(detailsList)):
            tempDict["details"] = detailsList[i]
            gbody = dict(tempDict, **general_dict)    #两个dict相加
            gbodys.append(gbody)
        for i in range(0, len(gbodys), 3):  # 三个detail作为一个request
            bodys.append(gbodys[i:i+3])
        for body in bodys:
            ret={"data":str(body).replace("'", '"')}
            rets.append(ret)
        return rets

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
        else:
            ep = excel_process()
            dicts=ep.readExcelExp(path, tab)
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

    def add_dict(self, d1, d2):
        d={}
        d=dict(d1, **d2)
        return d

if __name__ == '__main__':
    hp=http_process()
    #datas=hp.general_data('E:\\script\\test\\oauth\\case\\nickname_change.xlsx')
    #hp.http_general("http://192.168.22.61/users/friends/300", None, '{"Authorization":"Bearer 33bf4b6173ca584548012da8a5057ef3"}', 'POST')
    #hp.http_general("http://192.168.22.61/users/friends/300", None, '{"Authorization":"Bearer 01f0132df1e2b4ab1742053382bc6ec6"}', 'POST')
    #hp.http_general('http://192.168.22.61/v1/album/create', {u'caption': u'\u3002', u'description': u'\u3002', u'permit': 0}, header, 'PUT')
    #hp.http_exp('http://192.168.22.61/album/create', 'E:\\script\\test\\robotframework\\case\\album.xlsx', 'AlbumCreate', header, 'POST')
    #hp.http_exp('http://192.168.22.61/album/91', None, None, header, 'DELETE')
    #hp.process_encode({u'caption': u'\u3002', u'description': u'\u3002', u'permit': 0})