import multiprocessing

# 绑定的IP和端口
bind = '0.0.0.0:8080'

# worker数量：CPU + 1
workers = multiprocessing.cpu_count() + 1

# worker类型：gevent
worker_class = 'gevent'

# 日志配置
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# 预加载应用
preload_app = True

# 超时设置
timeout = 30

# 重启worker的最大请求数
max_requests = 2000
max_requests_jitter = 400