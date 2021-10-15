class models_fun(object):
    """docstring for ClassName"""
    def __init__(self):
        pass
    def list_setting(self, data, intdata=30,dian='....'):
        if len(str(data)) > intdata:
            return '{}{}'.format(str(data)[0:intdata],dian)
        else:
            return str(data)
    def pathurl(self,url):
        url_a = url[:-1] if url[-1] == '/' else url
        url_b = url_a[1:] if url_a[0] == '/' else url_a
        return url_b
