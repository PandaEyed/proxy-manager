from app import db

class Proxy(db.Model):
    __tablename__ = 'proxies'

    # 主键 ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="唯一标识")

    # VMS ID
    vms_id = db.Column(db.String(50), nullable=False, comment="机器 VMS 编号")

    # 内网和公网 IP
    internal_ip = db.Column(db.String(50), nullable=False, comment="内网 IP 地址")
    external_ip = db.Column(db.String(50), nullable=False, comment="公网 IP 地址")

    # 基本信息
    group_name = db.Column(db.String(100), nullable=True, comment="分组名称")
    datacenter = db.Column(db.String(100), nullable=True, comment="机房位置")
    isp_line = db.Column(db.String(100), nullable=True, comment="ISP 线路信息")
    specific_line = db.Column(db.String(100), nullable=True, comment="具体线路信息")

    # FRP 配置
    frpc_nickname = db.Column(db.String(100), nullable=True, comment="FRPC 昵称")
    frpc_description = db.Column(db.Text, nullable=True, comment="FRPC 说明")
    frps_ports = db.Column(db.String(50), nullable=True, comment="FRPS 占用或预留端口")

    # 供应商信息
    supplier = db.Column(db.String(100), nullable=True, comment="供应商名称")
    supplier_delivery = db.Column(db.Text, nullable=True, comment="供应商交付内容")

    # 接入与使用方
    access_method = db.Column(db.String(50), nullable=True, comment="接入方式（如 Squid、FRP）")
    user = db.Column(db.String(100), nullable=True, comment="使用方")
    gost_address = db.Column(db.String(255), nullable=True, comment="Gost 地址")

    # 数量与健康监测
    actual_count = db.Column(db.Integer, nullable=True, default=0, comment="实际数量")
    health_check = db.Column(db.String(50), nullable=True, comment="健康检测方式")

    # 备注信息
    remark_1 = db.Column(db.Text, nullable=True, comment="备注 1")
    remark_2 = db.Column(db.Text, nullable=True, comment="备注 2")
    remark_3 = db.Column(db.Text, nullable=True, comment="备注 3")

    # 时间戳
    created_at = db.Column(db.DateTime, server_default=db.func.now(), comment="创建时间")
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), comment="更新时间")

    def __repr__(self):
        return f"<Proxy(id={self.id}, internal_ip={self.internal_ip}, external_ip={self.external_ip})>"