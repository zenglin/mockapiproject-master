class models_fun(object):
    """docstring for ClassName"""

    def __init__(self):
        pass

    def list_setting(self, data, intdata=30,dian='....'):
        if len(str(data)) > intdata:
            return '{}{}'.format(str(data)[0:intdata],dian)
        else:
            return str(data)
