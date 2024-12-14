from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, IPAddress, Length

class AddProxyForm(FlaskForm):
    """添加代理的表单"""
    vms_id = StringField("VMS ID", validators=[DataRequired(),  Length(max=100)])
    internal_ip = StringField("内网 IP", validators=[DataRequired(), IPAddress(message="请输入合法的内网 IP")])
    external_ip = StringField("公网 IP", validators=[DataRequired(), IPAddress(message="请输入合法的公网 IP")])
    group_name = StringField("Group Name", validators=[Optional(), Length(max=100)])
    datacenter = StringField("机房", validators=[Optional(), Length(max=100)])
    isp_line = StringField("ISP 线路", validators=[Optional(), Length(max=100)])
    specific_line = StringField("具体线路", validators=[Optional(), Length(max=100)])
    frpc_nickname = StringField("FRPC 昵称", validators=[Optional(), Length(max=100)])
    frpc_description = TextAreaField("FRPC 说明", validators=[Optional(), Length(max=500)])
    frps_ports = StringField("FRPS 占用端口", validators=[Optional(), Length(max=100)])
    supplier = StringField("供应商", validators=[Optional(), Length(max=100)])
    supplier_delivery = TextAreaField("供应商交付内容", validators=[Optional(), Length(max=500)])
    access_method = StringField("接入方式", validators=[Optional(), Length(max=100)])
    user = StringField("使用方", validators=[Optional(), Length(max=100)])
    gost_address = StringField("GOST 地址", validators=[Optional(), Length(max=100)])
    actual_count = IntegerField("实际数量", validators=[Optional()])
    health_check = StringField("健康检测方式", validators=[Optional(), Length(max=100)])
    remark_1 = TextAreaField("备注 1", validators=[Optional(), Length(max=500)])
    remark_2 = TextAreaField("备注 2", validators=[Optional(), Length(max=500)])
    remark_3 = TextAreaField("备注 3", validators=[Optional(), Length(max=500)])
    submit = SubmitField("提交")
