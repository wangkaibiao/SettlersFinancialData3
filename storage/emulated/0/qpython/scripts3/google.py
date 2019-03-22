# -*- coding: utf-8 -*-
try:
    from storage.baidu_cloud import qpython_sync
    qpython_sync("/scripts3/","★test_sync.py")
except:
    print("using,testing,2")

try:
    import androidhelper
    droid = androidhelper.Android()
    droid.makeToast("导入androidhelper成功")
except:
    print("不存在androidhelper库")
"""--------------------------------------------------------------------------"""
import urllib

def import_simplejson():
    try:
        import simplejson as json
    except ImportError:
        try:
            import json  # Python 2.6+
        except ImportError:
            try:
                from django.utils import simplejson as json  # Google App Engine
            except ImportError:
                raise(ImportError, "Can't load a json library") 
    return json

class Record(object):#表示单条搜索结果
    def __init__(self, adict):
        assert adict, dict
        setattr(self, 'title', adict['title'])
        setattr(self, 'htmlSnippet', adict['htmlSnippet'])
        setattr(self, 'link', adict['link'])
 
class GoogleSearch(SearchBase):
    key = ''
    cx = ''     
    url = 'https://www.googleapis.com/customsearch/v1' # 调用api的地址
     
    def __init__(self, q, page=1):# 初始化，q为搜索关键字，默认从第一页开始
        SearchModel.__init__(self, q)
        self._page = page
     
    def _get_data(self):
        start = (self._page - 1) * 10 + 1 # 计算起始位置         
        data = {'q': self._q.encode("utf-8")}
        q_str = urllib.parse.urlencode(data) # 使用urllib中的urlencode方法         
        abs_url = "https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&%s&start=%d" % \
        (self.key, self.cx, q_str, start)         
        data = urllib.request.urlopen(abs_url) # 使用urllib.request的urlopen方法更简单         
        resultContent = data.read() # 获取结果 
        return resultContent
     
    def _get_json(self):
        if getattr(self, '_json', None) is None:
            json = import_simplejson()
            self._json = json.loads(self._get_data()) # 加载json数据
        return self._json
 
    def _get_count(self): # 获取搜索结果数量
        _json = self._get_json()
        return int(_json['queries']['request'][0]['totalResults'])
     
    def _get_result_list(self):
        _json = self._get_json()
        return _json['items']
     
    def __call__(self):
        records = []
        try:
            results =  self._get_result_list()
            for r in results:
                record = Record(r)
                records.append(record)
        except KeyError:
            pass
            # print KeyError.message
        return self._get_count(), records
    
search = GoogleSearch(query, page)
count, results = search()