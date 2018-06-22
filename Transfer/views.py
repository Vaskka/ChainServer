import json

# Create your views here.
from django.http import HttpResponse
from Transfer.models import Activity, User

from utils import util

'''
问题：
1. 待处理多对一的转账
2. 待定制异常处理移动端不同的请求参数和不同的情况
'''


# 注册
def do_register(request):

    pass


# 登陆
def do_login(request):

    pass


# 处理发起交易的请求
def do_transfer(request):

    try:
        # 待处理无此参数的异常
        a_user_phone = str(request.GET.get('a_user_phone'))
        b_user_phone = str(request.GET.get('b_user_phone'))
        money = float(request.GET.get('money'))

        # 检查用户是否存在
        is_a_exist = User.objects.filter(user_phone=a_user_phone).exists()
        is_b_exist = User.objects.filter(user_phone=b_user_phone).exists()

        if not is_a_exist or not is_b_exist:
            return HttpResponse(util.get_json(1, 'user is not exist', 'error', '0', '0'))

        # 检查转账者的余额
        balance = User.objects.get(user_phone=a_user_phone)
        if balance.balance < money:
            return HttpResponse(util.get_json(1, 'balance less', 'error', '0', '0'))
            pass

        # 更新Activity表
        Activity.objects.filter(a_user_phone=a_user_phone).update(status='wait_verify', money=money, b_user_phone=b_user_phone)
        Activity.objects.filter(a_user_phone=b_user_phone).update(status='wait_to_verified', money=money, b_user_phone=a_user_phone)

        pass
    except Exception:
        return HttpResponse(util.get_json(1, 'Unknown error', 'error', '0', '0'))
        pass

    return HttpResponse(util.get_json(0, 'success', 'wait_verify', a_user_phone, b_user_phone))
    pass


# 处理请求收款的轮询
def do_deal_receive(request):
    b_user_phone = str(request.GET.get('user_phone'))
    a_user_phone = Activity.objects.get(a_user_phone=b_user_phone).b_user_phone
    # result = util.get_json(0, 'request for the verify', 'wait_to_verified', a_user_phone, b_user_phone)
    a_user_name = User.objects.get(user_phone=a_user_phone).user_name
    money = float(Activity.objects.get(a_user_phone=b_user_phone).money)
    result = {
        'code': 0,
        'msg': 'request for the verify',
        'status': 'wait_to_verified',
        'a_user_info': {
            'user_phone': a_user_phone,
            'user_name': a_user_name
        },
        'money': money
    }

    Activity.objects.filter(a_user_phone=b_user_phone).update(status='hold')
    return json.dumps(result)
    pass


# 处理结束验证的请求
def do_complete_verify(request):
    try:
        user_phone = str(request.GET.get('user_phone'))
        do_init(user_phone)
        status = str(request.GET.get('status'))
        if status == 'success' or status == 'fail':
            Activity.objects.filter(b_user_phone=user_phone).update(status=status)
            return HttpResponse(util.get_json(0, 'success', 'hold', '0', '0'))
            pass
        else:
            return HttpResponse(util.get_json(1, 'Unknown error', 'error', '0', '0'))

        pass
    except Exception:
        return HttpResponse(util.get_json(1, 'Unknown error', 'error', '0', '0'))
        pass


# 处理验证成功的轮询
def deal_verify_success(request):
    user_phone = str(request.GET.get('user_phone'))
    transfer_money = float(Activity.objects.get(a_user_phone=user_phone).money)
    current_money = float(User.objects.get(user_phone=user_phone).balance)
    result_money = current_money - transfer_money

    User.objects.filter(user_phone=user_phone).update(balance=result_money)

    do_init(user_phone)
    pass


# 处理验证失败的轮询
def deal_verify_fail(request):
    user_phone = str(request.GET.get('user_phone'))

    do_init(user_phone)
    pass


'''
通用处理
'''


# 交给不同的轮询处理函数
def route_to_deal(request):
    user_phone = str(request.GET.get('user_phone'))
    result = Activity.objects.get(a_user_phone=user_phone)
    status = result.status

    if status == 'hold':
        return util.get_json(0, 'success', 'hold', '0', '0')
    elif status == 'wait_verify':
        return util.get_json(0, 'success', status, '0', '0')
    elif status == 'wait_to_verified':
        return do_deal_receive(request)
    elif status == 'success':
        deal_verify_success(request)
        return util.get_json(0, 'identify verify success', 'success', '0', '0')
    elif status == 'fail':
        deal_verify_fail(request)
        return util.get_json(1, 'identify verify failed', 'fail', '0', '0')
    pass


# 处理通用轮询
def do_common_query(request):
    status = request.GET.get('status')
    if status == 'request':
        return HttpResponse(route_to_deal(request))
        pass
    return HttpResponse(util.get_json(1, 'parameter error', 'error', '0', '0'))
    pass


# 初始化某个用户的Activity字段
def do_init(user_phone):
    Activity.objects.filter(a_user_phone=user_phone).update(status='hold', money=0.00, b_user_phone='0')
    pass
