from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)  # 返回 403 Forbidden 错误
        return f(*args, **kwargs)
    return decorated_function

def supplier_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'supplier':
            abort(403)  # 返回 403 Forbidden 错误
        return f(*args, **kwargs)
    return decorated_function