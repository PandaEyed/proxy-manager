from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import TableFrps, TableFrpc
from app.forms import AddFrpsForm, AddFrpcForm

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    """主页: 展示 table_frps 和 table_frpc 的数据"""
    frps_list = TableFrps.query.all()
    frpc_list = TableFrpc.query.all()
    return render_template("index.html", frps_list=frps_list, frpc_list=frpc_list)

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
def add_frpc(frps_id):
    """添加 FRPC 数据，并关联到指定的 FRPS"""
    form = AddFrpcForm()
    if form.validate_on_submit():
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
            frps_id=frps_id
        )
        db.session.add(frpc)
        db.session.commit()
        flash("FRPC added successfully!", "success")
        return redirect(url_for("main.index"))
    return render_template("add_frpc.html", form=form, frps_id=frps_id)