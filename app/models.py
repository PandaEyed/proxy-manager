from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db

# 定义中间表
supplier_frps = db.Table('supplier_frps',
    db.Column('supplier_id', db.Integer, db.ForeignKey('suppliers.id'), primary_key=True),
    db.Column('frps_id', db.Integer, db.ForeignKey('table_frps.id'), primary_key=True),
    db.Column('service_port', db.Integer, nullable=False, default=7000),
    db.Column('port_range', db.String(50), nullable=False, default="7001-7999"),
    db.Column('allocated_count', db.Integer, nullable=False, default=0),
    db.Column('online_count', db.Integer, nullable=False, default=0),
    db.Column('token', db.String(100), nullable=True)
)

class TableFrps(db.Model):
    __tablename__ = 'table_frps'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vms_id = db.Column(db.String(100), nullable=False, comment="VMS ID")
    internal_ip = db.Column(db.String(50), nullable=False, comment="内网 IP")
    external_ip = db.Column(db.String(50), nullable=False, comment="公网 IP")
    group_name = db.Column(db.String(100), nullable=True, comment="Group Name")
    datacenter = db.Column(db.String(100), nullable=True, comment="机房位置")
    isp_line = db.Column(db.String(100), nullable=True, comment="ISP 线路")
    specific_line = db.Column(db.String(100), nullable=True, comment="线路详细信息")
    note = db.Column(db.Text, nullable=True, comment="FRPS备注")

    # Relationship: One FRPS to Many FRPCs
    frpcs = db.relationship('TableFrpc', backref='frps', lazy=True)
    # Relationship: Many FRPS to Many Suppliers
    suppliers = db.relationship('Supplier', secondary=supplier_frps, back_populates='frps_list')
    supplier_associations = db.relationship('Supplier',
        secondary=supplier_frps,
        viewonly=True,
        lazy='dynamic',
        backref=db.backref('frps_associations', lazy='dynamic')
    )

    def __repr__(self):
        return f"<TableFrps(id={self.id}, vms_id={self.vms_id})"

    def get_supplier_info(self, supplier_id):
        """获取特定供应商的关联信息"""
        association = db.session.query(supplier_frps).filter_by(
            supplier_id=supplier_id,
            frps_id=self.id
        ).first()
        return association


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='supplier', comment="用户权限：admin 或 supplier")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    supplier = db.relationship('Supplier', backref=db.backref('user', uselist=False))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<User {self.username}>'


class TableFrpc(db.Model):
    __tablename__ = 'table_frpc'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    frpc_nickname = db.Column(db.String(100), nullable=True, default="无", comment="FRPC 昵称")
    frpc_description = db.Column(db.Text, nullable=True, default="无", comment="FRPC 说明")
    frps_ports = db.Column(db.String(50), nullable=True, default="无", comment="FRPS 占用预留端口")
    supplier = db.Column(db.String(100), nullable=True, default="无", comment="供应商")
    supplier_delivery = db.Column(db.Text, nullable=True, default="无", comment="供应商交付内容")
    access_method = db.Column(db.String(50), nullable=True, default="无", comment="接入方式")
    user = db.Column(db.String(100), nullable=True, default="无", comment="使用方")
    gost_address = db.Column(db.String(255), nullable=True, default="无", comment="Gost 地址")
    actual_count = db.Column(db.Integer, nullable=False, default=0, comment="实际数量")
    health_check = db.Column(db.String(50), nullable=True, default="无", comment="健康检测方式")
    remark_1 = db.Column(db.Text, nullable=True, default="无", comment="备注 1")
    remark_2 = db.Column(db.Text, nullable=True, default="无", comment="备注 2")

    # Foreign Key: Many FRPCs to One FRPS
    frps_id = db.Column(db.Integer, db.ForeignKey('table_frps.id'), nullable=True, default=0, comment="FRPS ID")

    def __repr__(self):
        return f"<TableFrpc(id={self.id}, frpc_nickname={self.frpc_nickname})"


class Supplier(db.Model):
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True, comment="供应商名称")
    contact = db.Column(db.String(100), nullable=True, comment="联系人")
    phone = db.Column(db.String(20), nullable=True, comment="联系电话")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship: Many Suppliers to Many FRPS
    frps_list = db.relationship('TableFrps', secondary=supplier_frps, back_populates='suppliers')

    def __repr__(self):
        return f"<Supplier(id={self.id}, name={self.name})"

