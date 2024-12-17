from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import TableFrps, TableFrpc
from app.forms import AddFrpsForm, AddFrpcForm, EditFrpsForm, EditFrpcForm

main = Blueprint('main', __name__)

@main.route("/", methods=["GET"])
def index():
    frps_list = TableFrps.query.all()
    return render_template("index.html", frps_list=frps_list, active_tab="dashboard")


@main.route("/frps", methods=["GET"])
def frps():
    frps_list = TableFrps.query.all()
    form = EditFrpsForm()  # 创建表单实例
    return render_template("frps.html", frps_list=frps_list, form=form,active_tab="frps")


@main.route("/frpc", methods=["GET"])
def frpc():
    frpc_list = TableFrpc.query.all()
    form = EditFrpcForm()  # 创建表单实例
    return render_template("frpc.html", frpc_list=frpc_list, form=form,active_tab="frpc")

@main.route("/add_frps", methods=["GET", "POST"])
def add_frps():
    """添加 FRPS 数据"""
    form = AddFrpsForm()
    if form.validate_on_submit():
        frps = TableFrps(
            vms_id=form.vms_id.data,
            internal_ip=form.internal_ip.data,
            external_ip=form.external_ip.data,
            group_name=form.group_name.data,
            datacenter=form.datacenter.data,
            isp_line=form.isp_line.data,
            specific_line=form.specific_line.data
        )
        db.session.add(frps)
        db.session.commit()
        flash("FRPS added successfully!", "success")
        return redirect(url_for("main.index"))
    return render_template("add_frps.html", form=form)


@main.route("/add_frpc/<int:frps_id>", methods=["GET", "POST"])
@main.route("/add_frpc", defaults={"frps_id": None}, methods=["GET", "POST"])
def add_frpc(frps_id):

    # 初始化表单
    form = AddFrpcForm()

    # 动态生成 FRPS 选项，添加未关联选项 (0 表示未关联)
    form.frps_id.choices = [(0, "未关联")] + [
        (frps.id, f"{frps.internal_ip} - {frps.vms_id}") for frps in TableFrps.query.all()
    ]

    # 如果表单提交并验证通过
    if form.validate_on_submit():
        frps_id_selected = form.frps_id.data if form.frps_id.data != 0 else None
        frpc = TableFrpc(
            frpc_nickname=form.frpc_nickname.data,
            frpc_description=form.frpc_description.data,
            frps_ports=form.frps_ports.data,
            supplier=form.supplier.data,
            supplier_delivery=form.supplier_delivery.data,
            access_method=form.access_method.data,
            user=form.user.data,
            gost_address=form.gost_address.data,
            actual_count=form.actual_count.data,
            health_check=form.health_check.data,
            remark_1=form.remark_1.data,
            remark_2=form.remark_2.data,
            frps_id=frps_id_selected  # 设置关联的 FRPS ID 或 None
        )
        db.session.add(frpc)
        db.session.commit()
        flash("FRPC added successfully!", "success")
        return redirect(url_for("main.frpc"))

    # 渲染模板
    return render_template("add_frpc.html", form=form, frps_id=frps_id)

@main.route("/edit_frps/<int:frps_id>", methods=["POST"])
def edit_frps(frps_id):
    form = EditFrpsForm()
    frps = TableFrps.query.get_or_404(frps_id)
    if form.validate_on_submit():
        frps.vms_id = form.vms_id.data
        frps.internal_ip = form.internal_ip.data
        frps.external_ip = form.external_ip.data
        db.session.commit()
        flash("FRPS updated successfully!", "success")
    return redirect(url_for("main.frps"))


@main.route("/delete_frps/<int:frps_id>", methods=["POST"])
def delete_frps(frps_id):
    frps = TableFrps.query.get_or_404(frps_id)
    db.session.delete(frps)
    db.session.commit()
    flash("FRPS deleted successfully!", "success")
    return redirect(url_for("main.frps"))


@main.route("/edit_frpc/<int:frpc_id>", methods=["POST"])
def edit_frpc(frpc_id):
    form = EditFrpcForm()
    frpc = TableFrpc.query.get_or_404(frpc_id)
    if form.validate_on_submit():
        frpc.frpc_nickname = form.frpc_nickname.data
        frpc.frps_ports = form.frps_ports.data
        db.session.commit()
        flash("FRPC updated successfully!", "success")
    return redirect(url_for("main.frpc"))



@main.route("/delete_frpc/<int:frpc_id>", methods=["POST"])
def delete_frpc(frpc_id):
    """删除 FRPC 数据"""
    frpc = TableFrpc.query.get_or_404(frpc_id)
    db.session.delete(frpc)
    db.session.commit()
    flash("FRPC deleted successfully!", "success")
    return redirect(url_for("main.frpc"))