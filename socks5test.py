import time
import requests
from requests.exceptions import ProxyError, ConnectTimeout


def test_socks5_proxy(proxy_host, proxy_port, username=None, password=None,
                      test_url="http://speedtest.tele2.net/10MB.zip"):
    if username and password:
        proxy = f"socks5://{username}:{password}@{proxy_host}:{proxy_port}"
    else:
        proxy = f"socks5://{proxy_host}:{proxy_port}"

    proxies = {
        "http": proxy,
        "https": proxy
    }

    try:
        # 测试连接
        print("🌐 测试代理连接...")
        start_time = time.time()
        response = requests.get(test_url, proxies=proxies, stream=True, timeout=10)
        response_time = time.time() - start_time

        if response.status_code == 200:
            print(f"✅ 代理 {proxy_host}:{proxy_port} 可用")
            print(f"✅ 代理 IP : {response.text}")
            print(f"⏱️ 响应时间: {response_time:.2f} 秒")
        else:
            print(f"❌ 代理 {proxy_host}:{proxy_port} 返回错误状态码: {response.status_code}")
            return

        # 测试下载速度
        print("📡 测试下载速度...")
        start_time = time.time()
        total_data = 0
        for chunk in response.iter_content(1024 * 1024):  # 每次读取 1MB
            total_data += len(chunk)
        elapsed_time = time.time() - start_time

        download_speed = (total_data / 1024 / 1024) / elapsed_time  # MB/s
        print(f"📥 下载速度: {download_speed:.2f} MB/s")

    except ProxyError:
        print(f"❌ 代理 {proxy_host}:{proxy_port} 不可用")
    except ConnectTimeout:
        print(f"❌ 代理 {proxy_host}:{proxy_port} 连接超时")
    except Exception as e:
        print(f"❌ 测试代理 {proxy_host}:{proxy_port} 时发生错误: {e}")


if __name__ == "__main__":
    # 修改为你的 Socks5 代理信息
    proxy_host = "xccx2025.vpsnb.net"  # 代理 IP
    proxy_port = 38002  # 代理端口
    username = "20231211"  # 代理用户名
    password = "u6pdxtud89"  # 代理密码
    test_url = "http://47.110.135.238:8081/getip"  # 测试用的目标 URL

    test_socks5_proxy(proxy_host, proxy_port, username, password, test_url)