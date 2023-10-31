import requests
import json
import mysql.connector

# MySQL数据库配置
db_config = {
    'host': '10.0.3.20',  # MySQL服务器IP地址
    'user': 'root',        # MySQL用户名
    'password': 'Yunmai.2209',  # MySQL密码
    'database': 'performanceData'  # 数据库名称
}

# API接口地址
api_url = 'http://10.0.3.20:5000/insert'

# 连接数据库
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# 从文件中读取数据并插入到数据库
with open('data.txt', 'r') as file:
    # 逐行读取文件中的数据
    for line in file:
        # 移除两端空格和换行符，并将数据分割成字段
        parts = line.strip().split()

        # 解析数据
        test_date = parts[0]  # 日期和时间字段
        test_team = parts[1]
        test_item = parts[2]
        driver_version = parts[3]
        firmware_version = parts[4]
        protocol_type = parts[5]
        client_ip = parts[6]
        port_mtu = int(parts[7])
        thread_num = int(parts[8])
        gb_average_rx = float(parts[9])
        gb_average_rx_cropped = float(parts[10])

        # 查询数据库，检查test_date是否存在
        query = "SELECT id FROM ethernet WHERE test_date = %s"
        cursor.execute(query, (test_date,))
        result = cursor.fetchone()

        # 如果test_date不存在，则插入数据
        if not result:
            # 构造数据
            data = {
                'test_date': test_date,
                'test_team': test_team,
                'test_item': test_item,
                'driver_version': driver_version,
                'firmware_version': firmware_version,
                'protocol_type': protocol_type,
                'client_ip': client_ip,
                'port_mtu': port_mtu,
                'thread_num': thread_num,
                'gb_average_rx': gb_average_rx,
                'gb_average_rx_cropped': gb_average_rx_cropped
            }

            # 发送POST请求插入数据
            response = requests.post(api_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
            print(response.status_code)  # 打印HTTP状态码
            print(response.json())  # 打印API返回的JSON数据
        else:
            print(f"Data for test_date {test_date} already exists in the database.")

# 关闭数据库连接
cursor.close()
connection.close()
