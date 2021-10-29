from defmethod.Log import logger
from django.db.models import Q


class Querymethod(object):

    def match_value(self, databody, conditionValue, req_type):
        '''
        依据接口设置匹配规则，获取请求参数中的value；以此作为查询条件
        :param databody: 接口请求参数数据-type=dict()
        :param conditionValue: 接口配置的匹配规则条件-type=dict()
        :return: 根据匹配规则,返回请求体中value
        '''

        # 递归引用列表取key,直至到value为'True', 'true'结束
        def key_list(key_data, lista=list()):
            for keys, values in key_data.items():
                if type(values) == type({}) or str(values) in ('True', 'true'):
                    lista.append(keys)
                    True if str(values) in ('True', 'true') else key_list(values)
                elif type(values) == type([]):
                    lista.append(keys)
                    lista.append(0)
                    key_list(values[0], lista)
                else:
                    if lista == []:
                        lista.append(keys)
                    break
            return lista

        # 依据分号切割规则数据，再依次根据规则匹配databody对应值
        if str(conditionValue).replace(' ', '') != '{}':
            re_listdata = []
            for key_data in str(conditionValue).split(";"):
                re_data = databody
                try:
                    lista = key_list(eval(key_data))
                    for value in lista:
                        re_data = re_data[value]
                except  KeyError:
                    if len(str(conditionValue).split(";")) == 1:
                        return False
                    lista.clear()
                else:
                    re_listdata.append(re_data)
                    lista.clear()
            re_data = re_listdata
            re_data = re_data[0] if req_type == 'GET' else re_data
        else:
            logger.warning('未找到到匹配的数据值,匹配规则=' + str(conditionValue))
            re_data = False
        return re_data


class DataCheck(object):
    '''数据必填+类型校验'''

    def __init__(self, code=['code', '-1'], msg=['msg'], data=['data', None]):
        self.key_list = []
        self.code = code
        self.msg = msg
        self.data = data

    # 校验必填项以及数据类型，如果不匹配抛出异常
    def __value_type(self, dict_b, type_a):
        dict_data = dict_b
        try:
            for keys in self.key_list:
                dict_data = dict_data[keys]
            if type(dict_data) != type(type_a) and type_a != True:
                raise ValueError('[{}]字段类型校验失败，期望传入类型为:{}'.format(keys, type(type_a)))
        except KeyError:
            if type_a == True:
                keys = str(keys)
                keys = 'list无元素' if keys == '0' else keys
                raise ValueError('必填校验失败,缺少必要参数:' + keys)

    def check(self, check_a, dict_b):
        try:
            # 为空不做校验，与页面规则一致
            if check_a == {}:
                return True
            re_data = self.get_dict_allkeys(check_a, dict_b)
        except Exception as ex:
            # 校验检查不通过,返回的报文；可通过类属性修改自定义key
            ex = str(ex).strip('()')
            re_data = {self.code[0]: self.code[1], self.msg[0]: ex, self.data[0]: self.data[1]}
            logger.error('入参不符合校验规则={},请求返回值={}'.format(check_a, re_data))
        return re_data

    # 无限遍历dict所有key，递归方式调用
    def get_dict_allkeys(self, check_a, dict_b):
        # 使用isinstance检测数据类型,dict递归
        if isinstance(check_a, dict):
            for x in range(len(check_a)):
                temp_key = list(check_a.keys())[x]
                temp_value = check_a[temp_key]
                if type(temp_value) in (type({}), type([])):
                    self.key_list.append(temp_key)
                self.get_dict_allkeys(temp_value, dict_b)  # 递归遍历
            # 回退dict的上一层结构
            self.key_list = self.key_list[:-1]
        elif isinstance(check_a, list):
            for key_a in check_a:
                if isinstance(key_a, dict):
                    # for x in range(len(key_a)):
                    # 递归到列表+元素位置0,即只支持列表第一个作为校验点
                    temp_key = list(key_a.keys())[0]
                    temp_value = key_a[temp_key]
                    self.key_list.append(0)
                    self.key_list.append(temp_key)
                    self.get_dict_allkeys(temp_value, dict_b)
                # 必填校验,兼容true,True
                if str(key_a) in ('true', 'True'):
                    self.__value_type(dict_b, True)
                    continue
                # 数据类型校验，目前校验str/int/bool(兼容缩写及全拼)
                if str(key_a) in ('str', 'string', "<class 'str'>"):
                    self.__value_type(dict_b, str())
                elif str(key_a) in ('int', 'integer', "<class 'int'>"):
                    self.__value_type(dict_b, int())
                elif str(key_a) in ('bool', 'boolean', "<class 'bool'>"):
                    self.__value_type(dict_b, bool())
            # 回退dict的上一层结构
            self.key_list = self.key_list[:-1]
        return True


class Currency(object):
    '''其他方法定义汇总使用'''

    def test_data(data):
        try:
            re_data = data['test_data'] if data['test_data'] != None else None
            logger.info('后门属性参数[test_data]=True,请求返回值=' + str(re_data))
        except:
            re_data = None
        return re_data

    # 获取后缀的url
    def find_path(self, sub, path, arg):
        # 兼容请求时url最后一位带了'/'
        path = path[:-1] if path[-1] == '/' else path
        index_list, index = [], path.find(sub)
        # 根据path定位'/'位置
        while index != -1:
            index_list.append(index)
            index = path.find(sub, index + 1)
        # 根据arg长度截取得到后缀url
        if len(index_list) > 0:
            index = index_list[-len(arg)]
            return path[index + 1:]
        else:
            return -1

    # sql语句中的or和and拼接方法
    def Q_model(self, list_a, re_dataid):
        re_con = Q()
        qvalue = Q()
        qvalue.connector = 'OR'
        for list_value in list_a:
            qvalue.children.append(('QueryValue', list_value))
        qurl_id = Q()
        qurl_id.connector = 'OR'
        qurl_id.children.append(('CustomUrl_id', re_dataid))
        re_con.add(qvalue, 'AND'), re_con.add(qurl_id, 'AND')
        return re_con
