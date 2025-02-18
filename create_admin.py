from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # 检查是否已存在管理员用户
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com')
        admin.set_password('admin')
        db.session.add(admin)
        db.session.commit()
        print('管理员用户创建成功！')
    else:
        print('管理员用户已存在！')