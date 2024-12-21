from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import TableFrps, TableFrpc,ScaleRequest,  ScaleItem
from app.forms import AddFrpsForm, AddFrpcForm, EditFrpsForm, EditFrpcForm,ScaleItemForm, ScaleRequestForm

main = Blueprint('main', __name__)
def flash_and_redirect(message, category, endpoint):
    """抽象 flash 消息和重定向逻辑"""
    flash(message, category)
    return redirect(url_for(endpoint))
@main.route("/", methods=["GET"])
def index():
    frps_list = TableFrps.query.all()
    # 数据统计逻辑
    datacenter_counts = {"SHAXY": 0, "SHARB": 0}  # 数据中心占比统计
    supplier_counts = {}  # 供应商占比统计
    for frps in frps_list:
        datacenter = frps.datacenter.strip().upper() if frps.datacenter else "未知"
        datacenter_counts[datacenter] = datacenter_counts.get(datacenter, 0) + 1
        for frpc in frps.frpcs:
            supplier = frpc.supplier or "未知供应商"
            supplier_counts[supplier] = supplier_counts.get(supplier, 0) + (frpc.actual_count or 0)

    return render_template(
        "index.html", frps_list=frps_list, datacenter_counts=datacenter_counts,
        supplier_counts=supplier_counts
    )

@main.route("/overview", methods=["GET"])
def overview():
    frps_list = TableFrps.query.all()
    return render_template(
        "overview.html",
        frps_list=frps_list
    )

# FRPS 列表页面
@main.route("/frps", methods=["GET", "POST"])
def frps():
    frps_list = TableFrps.query.all()
    form = EditFrpsForm()

    if form.validate_on_submit():
        frps = TableFrps.query.get_or_404(form.id.data)
        frps.vms_id = form.vms_id.data
        frps.internal_ip = form.internal_ip.data
        frps.external_ip = form.external_ip.data
        db.session.commit()
        return flash_and_redirect("FRPS updated successfully!", "success", "main.frps")

    return render_template("frps.html", frps_list=frps_list, form=form)


# FRPC 列表页面
@main.route("/frpc", methods=["GET", "POST"])
def frpc():
    frpc_list = TableFrpc.query.join(TableFrps).all()
    form = EditFrpcForm()
    # 获取所有的 FRPS 数据供下拉框选择
    frps_list = TableFrps.query.all()
    # 更新下拉框选项，使用 datacenter 替换 location



    if request.method == "POST" and form.validate_on_submit():
        frpc = TableFrpc.query.get_or_404(form.id.data)
        frpc.frpc_nickname = form.frpc_nickname.data
        frpc.frps_ports = form.frps_ports.data
        frpc.frps_id = form.frps_id.data if form.frps_id.data else None
        db.session.commit()
        return flash_and_redirect("FRPC updated successfully!", "success", "main.frpc")


    return render_template("frpc.html", frpc_list=frpc_list, frps_list=frps_list,form=form)

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


@main.route('/edit_frpc/<int:frpc_id>', methods=['GET', 'POST'])
def edit_frpc(frpc_id):
    print(f"Editing FRPC with ID: {frpc_id}")  # Debug: 确认进入路由
    print("Request method:", request.method)
    print("Form data:", request.form)

    # 获取当前要编辑的 FRPC 实例
    frpc = TableFrpc.query.get_or_404(frpc_id)
    form = EditFrpcForm()

    # 获取所有的 FRPS 数据供下拉框选择
    frps_list = TableFrps.query.all()

    # 更新下拉框选项，使用 datacenter 替换 location
    form.frps_id.choices = [(0, "未关联")] + [
        (frps.id, f"{frps.vms_id} (机房: {frps.datacenter})") for frps in frps_list
    ]


    if request.method == 'POST' and form.validate_on_submit():
        print("Form Submitted")  # Debug: 表单提交检测
        # 更新 FRPC 数据
        frpc.frpc_nickname = form.frpc_nickname.data
        frpc.frps_ports = form.frps_ports.data
        frpc.frps_id =  TableFrps.query.filter(TableFrps.vms_id == request.form["frpc_vm"]).first().id if request.form.get("frpc_vm", None) else None# 处理未关联情况
        # frpc.request.form.get("frpc_vm", None)
        db.session.commit()
        flash('FRPC updated successfully!', 'success')
        return redirect(url_for('main.frpc'))

    # 如果是 GET 请求，设置表单默认值
    form.frpc_nickname.data = frpc.frpc_nickname
    form.frps_ports.data = frpc.frps_ports
    form.frps_id.data = frpc.frps_id or 0  # 默认值为未关联

    # Debug 输出表单数据
    print("Form Default Data:", {
        "frpc_nickname": form.frpc_nickname.data,
        "frps_ports": form.frps_ports.data,
        "frps_id": form.frps_id.data
    })

    return render_template('edit_frpc.html', frpc=frpc)

@main.route("/delete_frpc/<int:frpc_id>", methods=["POST"])
def delete_frpc(frpc_id):
    """删除 FRPC 数据"""
    frpc = TableFrpc.query.get_or_404(frpc_id)
    db.session.delete(frpc)
    db.session.commit()
    flash("FRPC deleted successfully!", "success")
    return redirect(url_for("main.frpc"))


""" 扩容单 """

@main.route('/scale_requests', methods=['GET'])
def scale_requests():
    scale_requests = ScaleRequest.query.order_by(ScaleRequest.created_at.desc()).all()
    return render_template('scale_requests.html', scale_requests=scale_requests)

@main.route('/scale_request/<int:request_id>')
def scale_request_detail(request_id):
    scale_request = ScaleRequest.query.get_or_404(request_id)
    return render_template('scale_request_detail.html', scale_request=scale_request)


@main.route('/create_scale_request', methods=['GET', 'POST'])
def create_scale_request():
    form = ScaleRequestForm()
    form.frps_allocation.choices = [(frps.id, frps.vms_id) for frps in TableFrps.query.all()]
    if request.method == "GET":
        return render_template('create_scale_request.html', form=form)

    # if form.validate_on_submit():
    scale_request = ScaleRequest(
        subject=form.subject.data,
        description=form.description.data,
        request_type="扩容单",
        status="Pending",
        created_at=datetime.utcnow(),
    )
    db.session.add(scale_request)
    db.session.commit()

    for item_data in form.items.data:
        scale_item = ScaleItem(
            nickname=item_data['nickname'],
            progress=item_data['progress'],
            frps_id=form.frps_allocation.data,
            scale_request_id=scale_request.id,
        )
        db.session.add(scale_item)
    db.session.commit()

    flash('扩容单已成功创建！', 'success')
    return redirect(url_for('main.scale_requests'))


@main.route('/update_scale_request_status/<int:request_id>', methods=['POST'])
def update_scale_request_status(request_id):
    scale_request = ScaleRequest.query.get_or_404(request_id)
    scale_request.status = "Completed"
    db.session.commit()
    flash('工单已标记为完成！', 'success')
    return redirect(url_for('main.scale_request_detail', request_id=request_id))