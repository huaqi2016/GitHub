# -*- coding: utf-8 -*-
import MySQLdb
__author__ = 'zhoushengqiang'

class db_process(object):
    '''
    def __init__(self, hostname, username, password, dbname):
        self.hostname=hostname
        self.username=username
        self.password=password
        self.dbname=dbname
    '''
    def __init__(self):
        pass

    def db_connect(self, hostname, username, password, dbname):
        conn=MySQLdb.connect(host=hostname, user=username, passwd=password, db=dbname, charset="utf8")
        cur = conn.cursor()
        return (conn, cur)

    def select_all(self, conn, cur, sql):
        selectList=[]
        cur.execute(sql)
        data = cur.fetchall()
        for d in data:
            selectList.append(d[0])
        cur.close()
        conn.commit()
        conn.close()
        return selectList

    def select_data(self, conn, cur, sql, ids):
        selectList=[]
        for id in ids:
            exesql= sql%(int(id))
            cur.execute(exesql)
            data = cur.fetchone()
            print data
            selectList.append(data[0])
        cur.close()
        conn.commit()
        conn.close()
        return selectList

    def update_data(self, conn, cur, sql, ids, values):
        d=dict(zip(ids, values))
        print d
        for k in d.keys():
            exesql=sql%(int(k), str(d[k]))
            print exesql
            cur.execute(exesql)
        cur.close()
        conn.commit()
        conn.close()

    def delete_data(self, conn, cur, sql, ids):
        print ids
        for id in ids:
            exesql=sql%(int(id))
            cur.execute(exesql)
        cur.close()
        conn.commit()
        conn.close()

    def delete_all(self, conn, cur, sql):
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()

    def delete_tables(self, conn, cur, ts):
        for t in ts:
            cur.execute('delete from '+t)
        cur.close()
        conn.commit()
        conn.close()

    def insert_data(self, conn, cur, sql):
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()

if __name__ == '__main__':
    db = db_process()
    conn, cur = db.db_connect('192.168.22.62', 'root', '', 'ivollo')
    sql='update user_token set user_id =%d where access_token ="%s"'
    #db.update_data(conn, cur, sql, ['291', '292'], ['33bf4b6173ca584548012da8a5057ef3', '969c69b31e8f6257d95408708dc151fc'])
    ts=['sleep', 'sos']
    db.delete_tables(conn, cur, ts)