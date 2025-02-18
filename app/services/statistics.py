from app.models import TableFrps

class StatisticsService:
    @staticmethod
    def get_datacenter_statistics(frps_list):
        """获取数据中心统计信息"""
        datacenter_counts = {"SHAXY": 0, "SHARB": 0}
        for frps in frps_list:
            datacenter = frps.datacenter.strip().upper() if frps.datacenter else "未知"
            datacenter_counts[datacenter] = datacenter_counts.get(datacenter, 0) + 1
        return {key: value for key, value in datacenter_counts.items() if key != '无'}
    
    @staticmethod
    def get_supplier_statistics(frps_list):
        """获取供应商统计信息"""
        supplier_counts = {}
        for frps in frps_list:
            for frpc in frps.frpcs:
                supplier = frpc.supplier or "未知供应商"
                supplier_counts[supplier] = supplier_counts.get(supplier, 0) + (frpc.actual_count or 0)
        return supplier_counts
    
    @staticmethod
    def get_isp_statistics(frps_list):
        """获取ISP线路统计信息"""
        isp_counts = {}
        for frps in frps_list:
            if frps.isp_line:
                isp_line = frps.isp_line.strip()
                isp_counts[isp_line] = isp_counts.get(isp_line, 0) + 1
        return {key: value for key, value in isp_counts.items() if key != '无'}
    
    @staticmethod
    def get_capacity_statistics(frps_list):
        """获取FRPS容量统计信息"""
        capacity_data = []
        for frps in frps_list:
            total_count = sum(frpc.actual_count or 0 for frpc in frps.frpcs)
            capacity_data.append({
                'vms_id': frps.vms_id,
                'total_count': total_count,
                'usage_percent': min(round((total_count / 1000) * 100, 1), 100)
            })
        return capacity_data