from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Proxy
from app.forms import AddProxyForm

# 创建蓝图
main = Blueprint('main', __name__)


@main.route("/", methods=["GET", "POST"])
def index():
    """主页: 展示代理列表，支持分页、搜索，并包含添加新代理功能的弹窗"""
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)

    # 查询数据
    query = Proxy.query
    if search:
        query = query.filter(
            Proxy.vms_id.like(f"%{search}%") |
            Proxy.internal_ip.like(f"%{search}%") |
            Proxy.external_ip.like(f"%{search}%") |
            Proxy.group_name.like(f"%{search}%")
        )

    pagination = query.paginate(page=page, per_page=13)
    proxies = pagination.items

    # 创建表单实例
    form = AddProxyForm()

    # 处理添加新代理表单提交
    if form.validate_on_submit():
        print("Form validated successfully!")  # 调试信息
        proxy = Proxy(
            vms_id=form.vms_id.data,
            internal_ip=form.internal_ip.data,
            external_ip=form.external_ip.data,
            group_name=form.group_name.data,
            datacenter=form.datacenter.data,
            isp_line=form.isp_line.data,
            specific_line=form.specific_line.data,
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
            remark_3=form.remark_3.data
        )
        db.session.add(proxy)
        db.session.commit()
        flash("Proxy added successfully!", "success")

        return redirect(url_for('main.index'))
    else:
        print("Form validation errors:", form.errors)  # 输出错误信息

    return render_template("index.html", proxies=proxies, pagination=pagination, form=form)