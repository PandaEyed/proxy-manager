from app import create_app, db
from app.models import User

def create_user(username, email, password):
    app = create_app()
    with app.app_context():
        # 检查用户是否已存在
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, email=email, role='supplier')
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f'用户 {username} 创建成功！')
            return True
        else:
            print(f'用户 {username} 已存在！')
            return False

if __name__ == '__main__':
    # 示例：创建一个新用户
    username = input('请输入用户名：')
    email = input('请输入邮箱：')
    password = input('请输入密码：')
    create_user(username, email, password)