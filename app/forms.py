from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, FieldList, FormField, SelectField, PasswordField
from wtforms.validators import DataRequired, Optional, IPAddress, Length, NumberRange


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')


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
    frps_id = SelectField(
        "关联 FRPS",
        coerce=int,
        validators=[Optional()],
        render_kw={
            "class": "form-select select2",
            "data-placeholder": "搜索并选��� FRPS...",
        }
    )
    frpc_nickname = StringField("FRPC 昵称", validators=[Optional(), Length(max=100)])
    frpc_description = TextAreaField("FRPC 说明", validators=[Optional()])
    frps_ports = StringField("FRPS 占用端口", validators=[Optional(), Length(max=50)])
    supplier = StringField("供应商", validators=[Optional(), Length(max=100)])
    supplier_delivery = TextAreaField("供应商交付内容", validators=[Optional()])
    access_method = StringField("接入方式", validators=[Optional(), Length(max=50)])
    user = StringField("使用方", validators=[Optional(), Length(max=100)])
    gost_address = StringField("Gost 地址", validators=[Optional(), Length(max=255)])
    actual_count = IntegerField("实际数量", validators=[Optional()])
    health_check = SelectField(
        "健康检测方式",
        choices=[('', '请选择...'), ('无', None),('Client', 'Client'), ('FRPS', 'FRPS')],
        validators=[Optional()],
        render_kw={"class": "form-select"}
    )
    remark_1 = TextAreaField("备注 1", validators=[Optional()])
    remark_2 = TextAreaField("备注 2", validators=[Optional()])
    submit = SubmitField("提交")


class EditFrpsForm(FlaskForm):
    vms_id = StringField("VMS ID", validators=[DataRequired(), Length(max=100)])
    internal_ip = StringField("Internal IP", validators=[DataRequired()])
    external_ip = StringField("External IP", validators=[DataRequired()])
    submit = SubmitField("Save changes")


class EditFrpcForm(FlaskForm):
    frps_id = SelectField(
        "关联 FRPS",
        coerce=int,
        validators=[Optional()],
        choices=[]  # 初始为空，由视图动态设置
    )
    frpc_nickname = StringField("昵称", validators=[Length(max=100)])
    frpc_description = TextAreaField("描述", validators=[Optional()])
    frps_ports = StringField("端口占用", validators=[Length(max=50)])
    actual_count = IntegerField("实际数量", validators=[Optional()])
    supplier = StringField("供应商", validators=[Optional(), Length(max=100)])
    supplier_delivery = TextAreaField("供应商交付内容", validators=[Optional()])
    access_method = StringField("接入方式", validators=[Optional(), Length(max=50)])
    user = StringField("使用方", validators=[Optional(), Length(max=100)])
    gost_address = StringField("Gost 地址", validators=[Optional(), Length(max=255)])
    health_check = SelectField(
        "健康检测方式",
        choices=[('', '请选择...'), ('无', None),('Client', 'Client'), ('FRPS', 'FRPS')],
        validators=[Optional()],
        render_kw={"class": "form-select"}
    )
    remark_1 = TextAreaField("备注 1", validators=[Optional()])
    remark_2 = TextAreaField("备注 2", validators=[Optional()])
    submit = SubmitField("保存更改")
