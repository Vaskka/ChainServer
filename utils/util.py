import json


def get_json(code, msg, status, a_user_phone, b_user_phone):
    return json.dumps({'code': code, 'msg': msg, 'status': status, 'a_user_phone': a_user_phone, 'b_user_phone': b_user_phone})
    pass
