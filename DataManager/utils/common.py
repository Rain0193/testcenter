# -*- coding: utf-8 -*-
import logging
import datetime

from DataManager.utils.operation import add_register_data, add_project_data, add_module_data, add_td_data, add_record_data, reset_password_data, forget_password_data

from DataManager.models import ModuleInfo, Record

logger = logging.getLogger('qacenter')

def register_info_logic(**kwargs):
    """

    :param kwargs:
    :return:
    """
    return add_register_data(**kwargs)

def get_ajax_msg(msg, success):
    """
    ajax提示信息
    :param msg: str：msg
    :param success: str：
    :return:
    """
    return success if msg is 'ok' else msg

def init_filter_session(request, type=True):
    """
    init session
    :param request:
    :return:
    """
    if type:
        request.session['user'] = ''
        request.session['name'] = ''
        request.session['belong_project'] = ''
        request.session['belong_module'] = ''
    else:
        del request.session['user']
        del request.session['name']
        del request.session['belong_project']
        del request.session['belong_module']

def reset_password_info_logic(**kwargs):
    """
    修改密码信息逻辑处理
    :param kwargs: dict: 密码信息
    :return:
    """
    if kwargs.get('old_password') == 'd41d8cd98f00b204e9800998ecf8427e':
        return '旧密码不能为空'
    if kwargs.get('new_password') == 'd41d8cd98f00b204e9800998ecf8427e':
        return '新密码不能为空'

    return reset_password_data(**kwargs)


def forget_password_info_logic(**kwargs):
    """
       忘记密码信息逻辑处理
       :param kwargs: dict: 邮箱信息
       :return:
       """
    if kwargs.get('email') is '':
        return '邮箱不能为空'

    return forget_password_data(**kwargs)



def project_info_logic(type=True, **kwargs):
    """
    项目信息逻辑处理
    :param type: boolean:True 默认新增项目
    :param kwargs: dict: 项目信息
    :return:
    """
    if kwargs.get('project_name') is '':
        return '项目名称不能为空'
    if kwargs.get('responsible_name') is '':
        return '负责人不能为空'
    if kwargs.get('test_user') is '':
        return '测试人员不能为空'

    return add_project_data(type, **kwargs)

def set_filter_session(request):
    """
    update session
    :param request:
    :return:
    """
    # 出现数据工厂DataManager登录，DeviceManager没有进入index页面，重新初始化下面session
    request.session['user'] = ''
    request.session['name'] = ''
    request.session['belong_project'] = ''
    request.session['belong_module'] = ''

    if 'user' in request.POST.keys():
        request.session['user'] = request.POST.get('user')
    if 'name' in request.POST.keys():
        request.session['name'] = request.POST.get('name')
    if 'belong_project' in request.POST.keys():
        request.session['belong_project'] = request.POST.get('belong_project')
    if 'belong_module' in request.POST.keys():
        request.session['belong_module'] = request.POST.get('belong_module')

    filter_query = {
        'user': request.session['user'],
        'name': request.session['name'],
        'belong_project': request.session['belong_project'],
        'belong_module': request.session['belong_module'],
    }

    return filter_query

def module_info_logic(type=True, **kwargs):
    """
    模块信息逻辑处理
    :param type: boolean: True:默认新增模块
    :param kwargs: dict: 模块信息
    :return:
    """
    if kwargs.get('module_name') is '':
        return '模块名称不能为空'
    if kwargs.get('belong_project') == '请选择所属项目':
        return '请选择项目，没有请先添加哦'
    if kwargs.get('test_user') is '':
        return '测试人员不能为空'
    if kwargs.get('dev_user') is '':
        return '开发人员不能为空'

    return add_module_data(type, **kwargs)

def td_info_logic(type=True, **kwargs):
    """
    事务信息逻辑处理
    :param type: boolean: True:默认新增事务模板
    :param kwargs: dict: 模块信息
    :return:
    """

    '''
        动态展示模块
    '''
    if 'params' not in kwargs.keys():
        flag = kwargs.pop('flag')
        if flag == 'module':
            return load_modules(**kwargs)

    else:
        if kwargs.get('title') is '':
            return '事务名称不能为空'
        if kwargs.get('project') == '0':
            return '请选择项目，没有请先添加哦'
        if kwargs.get('belong_project') == '请选择':
            return '请选择模块，没有请先添加哦'
        if kwargs.get('url') is '':
            return '事务url地址不能为空'

        return add_td_data(type, **kwargs)


def load_modules(**kwargs):
    """
    加载对应项目的模块信息，用户前端ajax请求返回
    :param kwargs:  dict：项目相关信息
    :return: str: module_info
    """
    belong_project = kwargs.get('name').get('project')
    module_info = ModuleInfo.objects.filter(belong_project__project_name=belong_project) \
        .values_list('id', 'module_name').order_by('-create_time')
    module_info = list(module_info)
    string = ''
    for value in module_info:
        string = string + str(value[0]) + '^=' + value[1] + 'replaceFlag'
    return string[:len(string) - 11]

def record_info_logic(**kwargs):
    """
    调用历史信息逻辑处理
    :param kwargs: dict: 调用信息
    :return:
    """
    return add_record_data(**kwargs)


def get_total_values():
    total = {
        'yDatas': []
    }
    today = datetime.date.today()
    for i in range(-11, 1):
        begin = today + datetime.timedelta(days=i)
        end = begin + datetime.timedelta(days=1)

        pv = Record.objects.filter(create_time__range=(begin, end)).count()

        if not pv:
            pv = 0

        total['yDatas'].append(pv)

    return total