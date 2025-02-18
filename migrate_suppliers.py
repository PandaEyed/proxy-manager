from app import create_app, db
from app.models import TableFrpc, Supplier, TableFrps

def migrate_suppliers():
    # 创建应用上下文
    app = create_app()
    with app.app_context():
        # 1. 从 table_frpc 中获取所有不重复的供应商名称
        unique_suppliers = db.session.query(TableFrpc.supplier).distinct().filter(
            TableFrpc.supplier != '无',
            TableFrpc.supplier.isnot(None)
        ).all()

        # 2. 为每个供应商创建记录
        supplier_map = {}
        for (supplier_name,) in unique_suppliers:
            # 检查供应商是否已存在
            existing_supplier = Supplier.query.filter_by(name=supplier_name).first()
            if not existing_supplier:
                new_supplier = Supplier(name=supplier_name)
                db.session.add(new_supplier)
                db.session.flush()  # 获取新创建的供应商ID
                supplier_map[supplier_name] = new_supplier
            else:
                supplier_map[supplier_name] = existing_supplier

        # 3. 建立供应商和FRPS的关联关系
        frpc_records = TableFrpc.query.filter(
            TableFrpc.supplier != '无',
            TableFrpc.supplier.isnot(None),
            TableFrpc.frps_id.isnot(None)
        ).all()

        for frpc in frpc_records:
            if frpc.supplier in supplier_map and frpc.frps:
                supplier = supplier_map[frpc.supplier]
                frps = frpc.frps
                
                # 检查关联关系是否已存在
                if frps not in supplier.frps_list:
                    supplier.frps_list.append(frps)

        # 4. 提交所有更改
        try:
            db.session.commit()
            print("数据迁移成功完成！")
        except Exception as e:
            db.session.rollback()
            print(f"数据迁移失败：{str(e)}")

if __name__ == '__main__':
    migrate_suppliers()