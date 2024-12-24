from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired, Optional, IPAddress, Length, NumberRange
from wtforms import SelectField


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
            "data-placeholder": "搜索并选择 FRPS...",
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
    health_check = StringField("健康检测方式", validators=[Optional(), Length(max=50)])
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
    health_check = StringField("健康检测方式", validators=[Optional(), Length(max=50)])
    remark_1 = TextAreaField("备注 1", validators=[Optional()])
    remark_2 = TextAreaField("备注 2", validators=[Optional()])
    submit = SubmitField("保存更改")

class ScaleItemForm(FlaskForm):
    nickname = StringField('FRPC Nickname', validators=[DataRequired(), Length(max=100)])
    progress = IntegerField('扩展量', validators=[DataRequired(), NumberRange(min=1, max=750)])


class ScaleRequestForm(FlaskForm):
    subject = StringField('主题', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('描述需求', validators=[DataRequired()])
    frps_allocation = SelectField('选择 FRPS', choices=[], coerce=int)
    items = FieldList(FormField(ScaleItemForm), min_entries=1, max_entries=10)
    submit = SubmitField('提交扩容单')