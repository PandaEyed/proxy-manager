from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app import db
from app.models import TableFrps, TableFrpc, User, Supplier, supplier_frps
from app.forms import AddFrpsForm, AddFrpcForm, EditFrpsForm, EditFrpcForm, LoginForm
from app.services.statistics import StatisticsService
from app.decorators import admin_required, supplier_required

login_manager = LoginManager()
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

main = Blueprint('main', __name__)
def flash_and_redirect(message, category, endpoint):
    """抽象 flash 消息和重定向逻辑"""
    flash(message, category)
    return redirect(url_for(endpoint))
@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'supplier':
            return redirect(url_for('main.supplier_my_frps'))
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            if user.role == 'supplier':
                return redirect(url_for('main.supplier_my_frps'))
            return redirect(url_for('main.index'))
        flash('用户名或密码错误', 'error')
    return render_template('auth/login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route("/", methods=["GET"])
@login_required
@admin_required
def index():
    frps_list = TableFrps.query.all()
    # 使用StatisticsService获取统计数据
    filtered_count = StatisticsService.get_datacenter_statistics(frps_list)
    supplier_counts = StatisticsService.get_supplier_statistics(frps_list)
    isp_counts = StatisticsService.get_isp_statistics(frps_list)
    capacity_data = StatisticsService.get_capacity_statistics(frps_list)
    return render_template(
        "index.html", 
        frps_list=frps_list, 
        datacenter_counts=filtered_count,
        supplier_counts=supplier_counts,
        isp_counts=isp_counts,
        capacity_data=capacity_data
    )

@main.route("/overview", methods=["GET"])
@login_required
@admin_required
def overview():
    frps_list = TableFrps.query.all()
    form = AddFrpcForm()
    return render_template(
        "overview.html",
        frps_list=frps_list,
        form=form
    )

# FRPS 列表页面
@main.route("/frps", methods=["GET", "POST"])
@login_required
@admin_required
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
@login_required
@admin_required
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
@login_required
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
@login_required
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
        flash("代理���加成功！", "success")
        return redirect(url_for("main.frpc"))
    
    return render_template(
        "add_frpc.html", 
        form=form, 
        frps_list=frps_list  # 确保传递 frps_list 到模板
    )

@main.route("/edit_frps/<int:frps_id>", methods=["POST"])
@login_required
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
@login_required
def delete_frps(frps_id):
    frps = TableFrps.query.get_or_404(frps_id)
    db.session.delete(frps)
    db.session.commit()
    flash("FRPS deleted successfully!", "success")
    return redirect(url_for("main.frps"))


@main.route('/edit_frpc/<int:frpc_id>', methods=['POST'])
@login_required
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
@login_required
def delete_frpc(frpc_id):
    """删除 FRPC 数据"""
    frpc = TableFrpc.query.get_or_404(frpc_id)
    db.session.delete(frpc)
    db.session.commit()
    flash("FRPC deleted successfully!", "success")
    return redirect(url_for("main.frpc"))

@main.route("/supplier", methods=["GET"])
@login_required
@admin_required
def supplier():
    suppliers = Supplier.query.all()
    frps_list = TableFrps.query.all()
    return render_template(
        "supplier.html",
        suppliers=suppliers,
        frps_list=frps_list
    )

@main.route("/supplier/<int:supplier_id>", methods=["GET"])
@login_required
def supplier_detail(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    # 获取所有未分配给当前供应商的FRPS列表
    available_frps_list = TableFrps.query.filter(~TableFrps.suppliers.contains(supplier)).all()
    return render_template("supplier_detail.html", supplier=supplier, available_frps_list=available_frps_list)

@main.route("/add_supplier", methods=["POST"])
@login_required
def add_supplier():
    try:
        supplier = Supplier(
            name=request.form.get('name'),
            contact=request.form.get('contact'),
            phone=request.form.get('phone')
        )
        
        # 处理FRPS分配
        frps_ids = request.form.getlist('frps_ids')
        if frps_ids:
            frps_list = TableFrps.query.filter(TableFrps.id.in_(frps_ids)).all()
            supplier.frps_list.extend(frps_list)
        
        db.session.add(supplier)
        db.session.commit()
        flash("供应商添加成功！", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"添加失败：{str(e)}", "error")
    
    return redirect(url_for("main.supplier"))

@main.route("/assign_frps_to_supplier/<int:supplier_id>", methods=["POST"])
@login_required
def assign_frps_to_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    
    try:
        frps_ids = request.form.getlist('frps_ids')
        if frps_ids:
            frps_list = TableFrps.query.filter(TableFrps.id.in_(frps_ids)).all()
            for frps in frps_list:
                if frps not in supplier.frps_list:
                    supplier.frps_list.append(frps)
            
            db.session.commit()
            flash("FRPS分配成功！", "success")
        else:
            flash("请选择要分配的FRPS", "warning")
    except Exception as e:
        db.session.rollback()
        flash(f"分配失败：{str(e)}", "error")
    
    return redirect(url_for("main.supplier_detail", supplier_id=supplier_id))

@main.route("/remove_frps_from_supplier/<int:supplier_id>/<int:frps_id>", methods=["POST"])
@login_required
def remove_frps_from_supplier(supplier_id, frps_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    frps = TableFrps.query.get_or_404(frps_id)
    
    try:
        supplier.frps_list.remove(frps)
        db.session.commit()
        flash("已成功解除FRPS分配！", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"解除分配失败：{str(e)}", "error")
    
    return redirect(url_for("main.supplier_detail", supplier_id=supplier_id))

@main.route("/delete_supplier/<int:supplier_id>", methods=["POST"])
@login_required
def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    try:
        db.session.delete(supplier)
        db.session.commit()
        flash("供应商删除成功！", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"删除失败：{str(e)}", "error")
    return redirect(url_for("main.supplier"))

@main.route("/supplier/<int:supplier_id>/frps/<int:frps_id>/update_note", methods=["POST"])
@login_required
def update_frps_note(supplier_id, frps_id):
    """更新供应商关联的FRPS备注"""
    supplier = Supplier.query.get_or_404(supplier_id)
    frps = TableFrps.query.get_or_404(frps_id)
    
    if frps not in supplier.frps_list:
        flash("该FRPS不属于此供应商", "error")
        return redirect(url_for("main.supplier_detail", supplier_id=supplier_id))
    
    note = request.form.get("note", "")
    # 添加note字段到TableFrps模型中
    frps.note = note
    db.session.commit()
    
    flash("FRPS备注已更新", "success")
    return redirect(url_for("main.supplier_detail", supplier_id=supplier_id))

@main.route("/supplier/my-frps", methods=["GET"])
@login_required
@supplier_required
def supplier_my_frps():
    """供应商查看自己的FRPS资产"""
    if not current_user.supplier:
        flash("您还未关联到任何供应商账户", "error")
        return redirect(url_for("main.login"))
    
    # 获取当前供应商的FRPS列表，包括关联表中的数据
    supplier_id = current_user.supplier.id
    frps_list = TableFrps.query.join(
        supplier_frps,
        supplier_frps.c.frps_id == TableFrps.id
    ).filter(
        supplier_frps.c.supplier_id == supplier_id
    ).all()

    # 为每个FRPS获取关联表数据
    for frps in frps_list:
        # 使用get_supplier_info方法获取关联信息
        association = frps.get_supplier_info(supplier_id)
        if association:
            # 将关联信息存储为属性
            frps.service_port = association.service_port
            frps.port_range = association.port_range
            frps.allocated_count = association.allocated_count
            frps.online_count = association.online_count
            frps.token = association.token
    
    return render_template("supplier/my_frps.html", frps_list=frps_list)

@main.route("/supplier/my-contract", methods=["GET"])
@login_required
@supplier_required
def supplier_my_contract():
    """供应商查看自己的合同"""
    if not current_user.supplier:
        flash("您还未关联到任何供应商账户", "error")
        return redirect(url_for("main.login"))
    
    return render_template("supplier/my_contract.html")

@main.route("/supplier/help", methods=["GET"])
@login_required
@supplier_required
def supplier_help():
    """供应商帮助文档"""
    return render_template("supplier/help.html")

@main.route("/supplier/<int:supplier_id>/update", methods=["POST"])
@login_required
def update_supplier(supplier_id):
    """更新供应商信息"""
    supplier = Supplier.query.get_or_404(supplier_id)
    try:
        supplier.name = request.form.get('name')
        supplier.contact = request.form.get('contact')
        supplier.phone = request.form.get('phone')
        
        db.session.commit()
        flash("供应商信息更新成功！", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"更新失败：{str(e)}", "error")
    
    return redirect(url_for("main.supplier_detail", supplier_id=supplier_id))
