from flask import flash, redirect, url_for

def flash_and_redirect(message, category, endpoint):
    """抽象 flash 消息和重定向逻辑
    
    Args:
        message (str): 要显示的消息
        category (str): 消息类别（success, error等）
        endpoint (str): 重定向的端点
    
    Returns:
        Response: Flask重定向响应
    """
    flash(message, category)
    return redirect(url_for(endpoint))

def format_datacenter_name(datacenter):
    """格式化数据中心名称
    
    Args:
        datacenter (str): 原始数据中心名称
    
    Returns:
        str: 格式化后的数据中心名称
    """
    return datacenter.strip().upper() if datacenter else "未知"

def calculate_usage_percent(total_count, max_capacity=1000):
    """计算使用百分比
    
    Args:
        total_count (int): 当前使用量
        max_capacity (int): 最大容量
    
    Returns:
        float: 使用百分比，最大为100
    """
    return min(round((total_count / max_capacity) * 100, 1), 100)