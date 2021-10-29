from django.utils.safestring import mark_safe


def tem_mark_safe(req_type):
    # 回显接口测试页面中请求类型,定义checked且不转义
    checked = ["", "", ""]
    if req_type == 'post':
        checked[0] = 'checked'
    elif req_type == 'get':
        checked[1] = 'checked'
    elif req_type == 'put':
        checked[2] = 'checked'
    html_a = '<td><input type="radio" name="req_type" value="post" ' + checked[
        0] + '/>POST''<input type="radio" name="req_type" value="get" ' + checked[
                 1] + '/>GET''<input type="radio" name="req_type" value="put" ' + checked[2] + '/>PUT</td>'
    mark_data = mark_safe(html_a)
    return mark_data
