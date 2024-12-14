from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, IPAddress, Length

class AddFrpsForm(FlaskForm):
    vms_id = StringField("VMS ID", validators=[DataRequired(), Length(max=100)])
    internal_ip = StringField("内网 IP", validators=[DataRequired(), IPAddress()])
    external_ip = StringField("公网 IP", validators=[DataRequired(), IPAddress()])
    group_name = StringField("Group Name", validators=[Optional(), Length(max=100)])
    datacenter = StringField("机房", validators=[Optional(), Length(max=100)])
    isp_line = StringField("ISP 线路", validators=[Optional(), Length(max=100)])
    specific_line = StringField("线路详情", validators=[Optional(), Length(max=100)])
    submit = SubmitField("提交")

class AddFrpcForm(FlaskForm):
    frpc_nickname = StringField("FRPC 昵称", validators=[Optional(), Length(max=100)])
    frpc_description = TextAreaField("FRPC 说明", validators=[Optional()])
    frps_ports = StringField("FRPS 占用端口", validators=[Optional(), Length(max=50)])
    supplier = StringField("供应商", validators=[Optional(), Length(max=100)])
    supplier_delivery = TextAreaField("供应商交付内容", validators=[Optional()])
    access_method = StringField("接入方式", validators=[Optional(), Length(max=50)])
    user = StringField("使用方", validators=[Optional(), Length(max=100)])
    gost_address = StringField("Gost 地址", validators=[Optional(), Length(max=255)])
    actual_count = IntegerField("实际数量", validators=[Optional()])
    health_check = StringField("健康检测方式", validators=[Optional(), Length(max=50)])
    remark_1 = TextAreaField("备注 1", validators=[Optional()])
    remark_2 = TextAreaField("备注 2", validators=[Optional()])
    submit = SubmitField("提交")