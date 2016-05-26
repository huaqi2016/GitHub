#coding:utf-8
__author__ = 'zhou shengqiang '

class general_process(object):
    def __init__(self):
        pass

    def dictproc(self, d, item):
        ret=[]
        for i in d:
            i.pop(item)
            ret.append(i)
        return ret


if __name__ == '__main__':
    d=[{'a':1, 'b':2}, {'c':1, 'b':2}]
    gp=general_process()
    gp.dictproc(d, 'b')
