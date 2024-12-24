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
    # 去掉未使用的 frps
    filtered_count = {key: value for key, value in datacenter_counts.items() if key != '无'}
    return render_template(
        "index.html", frps_list=frps_list, datacenter_counts=filtered_count,
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
    form = AddFrpsForm()  # 改用 AddFrpsForm 而不是 EditFrpsForm
    datacenter_colors = {
        'shaxy': '#1E90FF',
        'sharb': '#ADFF2F'
    }

    if form.validate_on_submit():
        # 处理新增 FRPS 的表单提交
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
        flash("FRPS 添加成功！", "success")
        return redirect(url_for("main.frps"))

    return render_template(
        "frps.html", 
        frps_list=frps_list, 
        form=form, 
        datacenter_colors=datacenter_colors
    )


# FRPC 列表页面
@main.route("/frpc", methods=["GET", "POST"])
def frpc():
    frpc_list = TableFrpc.query.join(TableFrps).all()
    form = EditFrpcForm()
    # 获��� FRPS 数据供下拉框选择
    frps_list = TableFrps.query.all()
    
    # 添加数据中心颜色映射
    datacenter_colors = {
        'shaxy': '#1E90FF',  # 上海新园
        'sharb': '#ADFF2F'   # 上海如邦
    }

    if request.method == "POST" and form.validate_on_submit():
        frpc = TableFrpc.query.get_or_404(form.id.data)
        frpc.frpc_nickname = form.frpc_nickname.data
        frpc.frps_ports = form.frps_ports.data
        frpc.frps_id = form.frps_id.data if form.frps_id.data else None
        db.session.commit()
        return flash_and_redirect("FRPC 更新成功！", "success", "main.frpc")

    return render_template(
        "frpc.html", 
        frpc_list=frpc_list, 
        form=form, 
        frps_list=frps_list,
        datacenter_colors=datacenter_colors  # 添加颜色映射到模板变量
    )

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


@main.route("/add_frpc", methods=["GET", "POST"])
def add_frpc():
    form = AddFrpcForm()
    # 获取所有 FRPS 数据
    frps_list = TableFrps.query.all()
    
    # 设置 form 的选项
    form.frps_id.choices = [(0, '未分配')] + [
        (frps.id, f'{frps.vms_id} ({frps.datacenter})') 
        for frps in frps_list
    ]
    
    if form.validate_on_submit():
        frpc = TableFrpc(
            frpc_nickname=form.frpc_nickname.data,
            frpc_description=form.frpc_description.data,
            frps_ports=form.frps_ports.data,
            frps_id=form.frps_id.data if form.frps_id.data else None,
            actual_count=form.actual_count.data or 0,
            supplier=form.supplier.data,
            supplier_delivery=form.supplier_delivery.data,
            access_method=form.access_method.data,
            user=form.user.data,
            gost_address=form.gost_address.data,
            health_check=form.health_check.data,
            remark_1=form.remark_1.data,
            remark_2=form.remark_2.data
        )
        db.session.add(frpc)
        db.session.commit()
        flash("代理添加成功！", "success")
        return redirect(url_for("main.frpc"))
    
    return render_template(
        "add_frpc.html", 
        form=form, 
        frps_list=frps_list  # 确保传递 frps_list 到模板
    )

@main.route("/edit_frps/<int:frps_id>", methods=["POST"])
def edit_frps(frps_id):
    frps = TableFrps.query.get_or_404(frps_id)
    try:
        # 更新所有字段
        frps.vms_id = request.form.get('vms_id')
        frps.internal_ip = request.form.get('internal_ip')
        frps.external_ip = request.form.get('external_ip')
        frps.group_name = request.form.get('group_name')
        frps.datacenter = request.form.get('datacenter')
        frps.isp_line = request.form.get('isp_line')
        frps.specific_line = request.form.get('specific_line')
        
        db.session.commit()
        flash("FRPS 更新成功！", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"更新失败：{str(e)}", "error")
    
    return redirect(url_for("main.frps"))


@main.route("/delete_frps/<int:frps_id>", methods=["POST"])
def delete_frps(frps_id):
    frps = TableFrps.query.get_or_404(frps_id)
    db.session.delete(frps)
    db.session.commit()
    flash("FRPS deleted successfully!", "success")
    return redirect(url_for("main.frps"))


@main.route('/edit_frpc/<int:frpc_id>', methods=['POST'])
def edit_frpc(frpc_id):
    frpc = TableFrpc.query.get_or_404(frpc_id)
    
    try:
        # 直接从表单数据获取值
        frpc.frpc_nickname = request.form.get('frpc_nickname')
        frpc.frpc_description = request.form.get('frpc_description')
        frpc.frps_ports = request.form.get('frps_ports')
        frpc.actual_count = int(request.form.get('actual_count', 0))
        frpc.supplier = request.form.get('supplier')
        frpc.supplier_delivery = request.form.get('supplier_delivery')
        frpc.access_method = request.form.get('access_method')
        frpc.user = request.form.get('user')
        frpc.gost_address = request.form.get('gost_address')
        frpc.health_check = request.form.get('health_check')
        frpc.remark_1 = request.form.get('remark_1')
        frpc.remark_2 = request.form.get('remark_2')
        
        # 处理 frps_id
        frps_id = int(request.form.get('frps_id', 0))
        frpc.frps_id = None if frps_id == 0 else frps_id
        
        db.session.commit()
        flash('FRPC 更新成功！', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'更新失败：{str(e)}', 'error')
    
    return redirect(url_for('main.frpc'))

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