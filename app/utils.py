#coding:utf8


from flask_login import UserMixin
from dateutil import rrule
from app import login_manager
from limsMsql import select_user


# 自定义用户账号密码
class User(UserMixin):
    pass

# 如果用户名存在则构建一个新的用户类对象，并使用用户名作为ID
# 如果不存在，必须返回None
@login_manager.user_loader
def load_user(username):
    if query_user(username) is not None:
        curr_user = User()
        curr_user.id = username
        return curr_user


# 用户记录表
# users = [
#     {'username': 'admin', 'password': 'admin123456'},
#     {'username': 'alan', 'password': 'alan123456'},
#     {'username': 'liangjun_gao', 'password': 'gao123456'},
# ]

# 通过用户名，获取用户记录，如果不存在，则返回None
def query_user(username):
    users = select_user(username)
    for user in users:
        if user['username'] == username:
            return user


def workdays(start,end=None, holidays=0, days_off=None,count=None):
    if days_off is None:
        days_off = 5, 6
    workdays = [x for x in range(7) if x not in days_off]
    days = rrule.rrule(rrule.DAILY, dtstart=start, byweekday=workdays, count=count)
    return list(days)[-1]




