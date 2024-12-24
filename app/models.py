from datetime import datetime

from app import db

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

    # Relationship: One FRPS to Many FRPCs
    frpcs = db.relationship('TableFrpc', backref='frps', lazy=True)

    def __repr__(self):
        return f"<TableFrps(id={self.id}, vms_id={self.vms_id})>"


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
        return f"<TableFrpc(id={self.id}, frpc_nickname={self.frpc_nickname})>"

