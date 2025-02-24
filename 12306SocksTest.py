import requests


def send_request_via_socks5_proxy():
    # 请求 URL
    url = "https://mobile.12306.cn/otsmobile/app/mgs/mgw.htm"

    # 请求参数
    params = {
        "operationType": "com.cars.otsmobile.queryLeftTicketG",
        "requestData": '[{"train_date":"20250103","purpose_codes":"00","from_station":"BJP","to_station":"SHH","station_train_code":"","start_time_begin":"0000","start_time_end":"2400","train_headers":"QB#","train_flag":"","seat_type":"0","seatBack_Type":"","ticket_num":"","dfpStr":"","baseDTO":{"check_code":"b1773885886094fea7ed46adde7795c5","device_no":"TEMP-Z26aOLHZBGsDACo1sXN55vos","h5_app_id":"60000001","h5_app_version":"5.9.0.42","hwv":"2107119DC","mobile_no":"","os_type":"a","time_str":"20250103102850","user_name":"pinpoy","version_no":"5.9.0.8"}}]',
        "ts": "1735871330041",
        "sign": "2b3028a73e251c76eec9d83122d95c0a5f618079146769233d4f9dd4b20823a8"
    }

    # 请求头
    headers = {
        "pagets": "",
        "nbappid": "60000001",
        "nbversion": "5.9.0.42",
        "x-mpaas-apdidtoken": "kmG+mNAINRcoZMVjc3qJzghvLc0iGa/mezKppTpfbpJTNf0plAEAAA==",
        "x-mpaas-timestamp": "PGf/dRu",
        "x-mpaas-uid": "Android",
        "appv": "5.9.0.8",
        "tk": "UKHK3f4EAmeAEF031DOIoDjRUWcPRvQsbcp2p0",
        "bbid": "c1605850-c65a-3403-a9ee-04d3bee7e30f",
        "fo": "whfltfp32tx09e09mFCI0Q9AEcb3MbQxgE42HcurkW97X1p8ZMj7-rhcZRQcNN4imEBGsPaEa1tbfvDK3dDKx7He5Pe7N2djeoVQj0JroG2GFVtGRC8L_YvvqyWf03asQy_DdHlFXnbqxx9R5txi3AC9ROY_zb-nt7aK_g",
        "dfpstr": "",
        "user-agent": "Dalvik/2.1.0 (Linux; U; Android 13; 2107119DC Build/TKQ1.220829.002)",
        "osm": "a",
        "blueapdidtoken": "kmG+mNAINRcoZMVjc3qJzghvLc0iGa/mezKppTpfbpJTNf0plAEAAA==",
        "Platform": "ANDROID",
        "AppId": "9101430221728",
        "WorkspaceId": "product",
        "productVersion": "1.8.5.241219194812",
        "productId": "9101430221728_ANDROID",
        "did": "TEMP-Z26aOLHZBGsDACo1sXN55vos",
        "clientId": "241227201442593|241227201442592",
        "TRACKERID": "",
        "signType": "sm3",
        "x-app-sys-Id": "com.MobileTicket",
        "Cookie": "JSESSIONID=C0558A9F5CE6CB25C629FCE4CA882DE8; AlteonMobile=FVsgET/UAQqIWpB0yVQvUw$$; BIGipServernginxformobile=351601162.50215.0000; altmobile=AaF6JhzlAgphMGoz+WCRNA$$; otsBusiness=B4yoGBzlAgp0kxpZmjRvNg$$",
        "RpcId": "17",
        "TRACEID": "TEMP-Z26aOLHZBGsDACo1sXN55vosnull_17",
        "Retryable2": "0",
        "Accept-Language": "zh-Hans",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive",
        "Host": "mobile.12306.cn"
    }

    # Socks5 代理配置
    proxy_host = "xccx2025.vpsnb.net"  # 代理 IP
    proxy_port = 38002  # 代理端口
    username = "20231211"  # 代理用户名
    password = "u6pdxtud89"  # 代理密码

    proxy = f"socks5://{username}:{password}@{proxy_host}:{proxy_port}"
    proxies = {
        "http": proxy,
        "https": proxy
    }

    try:
        # 发送请求
        response = requests.get(url, headers=headers, params=params,timeout=10)
        #response = requests.get(url, headers=headers, params=params, proxies=proxies, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")


if __name__ == "__main__":
    send_request_via_socks5_proxy()