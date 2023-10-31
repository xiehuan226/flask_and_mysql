# pip install mysql-connector-python
# pip install flask
# pip install openpyxl
import plotly
from flask import Flask, request, jsonify, render_template
import mysql.connector
import pandas as pd
import plotly.express as px
import os


app = Flask(__name__)

# MySQL数据库配置
db_config = {
    'host': '10.0.3.20',  # MySQL服务器IP地址
    'user': 'root',        # MySQL用户名
    'password': 'Yunmai.2209',  # MySQL密码
    'database': 'performanceData'  # 数据库名称
}


# 创建数据库和表
def create_database_and_table():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # 创建数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS performanceData")
        cursor.execute("USE performanceData")

        # 创建ethernet表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ethernet (
                id INT AUTO_INCREMENT PRIMARY KEY,
                test_date DATETIME,
                test_team VARCHAR(255),
                test_item VARCHAR(255),
                driver_version VARCHAR(255),
                firmware_version VARCHAR(255),
                protocol_type VARCHAR(255),
                client_ip VARCHAR(255),
                port_mtu INT,
                thread_num INT,
                packet_length VARCHAR(255),
                bandwidth VARCHAR(255),
                gb_average_rx FLOAT,
                gb_average_rx_cropped FLOAT,
                gb_average_tx FLOAT,
                gb_average_tx_cropped FLOAT
            )
        """)

        connection.commit()

    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        connection.close()


# 创建数据库和表
create_database_and_table()


# curl -H "Content-Type: application/json" -X POST -d "{\"test_date\":\"2023.10.23.23:55:14\", \"test_team\":\"QA\",
# \"test_item\":\"ethernet\", \"driver_version\":\"1.1.0.28\", \"firmware_version\":\"100.28.b13.L1ONNADE\",
# \"protocol_type\":\"tcp\", \"client_ip\":\"6.6.6.34\", \"port_mtu\":4200, \"thread_num\":16, \"gb_average_rx\":22.78,
# \"gb_average_rx_cropped\":23.5}" http://127.0.0.1:5000/insert
# API接口：插入数据
@app.route('/insert', methods=['POST'])
def insert_data():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        data = request.get_json()  # 获取POST请求中的JSON数据

        # 插入数据到ethernet表
        query = """
            INSERT INTO ethernet (test_date, test_team, test_item, driver_version,
                                  firmware_version, protocol_type, client_ip,
                                  port_mtu, thread_num, packet_length, bandwidth,
                                  gb_average_rx, gb_average_rx_cropped,
                                  gb_average_tx, gb_average_tx_cropped)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (data['test_date'], data['test_team'], data['test_item'],
                  data['driver_version'], data['firmware_version'], data['protocol_type'],
                  data['client_ip'], data['port_mtu'], data['thread_num'],
                  data['packet_length'], data['bandwidth'], data['gb_average_rx'],
                  data['gb_average_rx_cropped'], data['gb_average_tx'], data['gb_average_tx_cropped'])

        cursor.execute(query, values)
        connection.commit()

        return jsonify({'message': 'Data inserted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# API接口：查询数据
@app.route('/get', methods=['GET'])
def get_data():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # 查询ethernet表中的所有数据
        cursor.execute("SELECT * FROM ethernet")
        data = cursor.fetchall()

        # 将查询结果转换为字典列表
        result = []
        for row in data:
            result.append({
                'id': row[0],
                'test_date': row[1],
                'test_team': row[2],
                'test_item': row[3],
                'driver_version': row[4],
                'firmware_version': row[5],
                'protocol_type': row[6],
                'client_ip': row[7],
                'port_mtu': row[8],
                'thread_num': row[9],
                'packet_length': row[10],
                'bandwidth': row[11],
                'gb_average_rx': row[12],
                'gb_average_rx_cropped': row[13],
                'gb_average_tx': row[14],
                'gb_average_tx_cropped': row[15]
            })

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# API接口：更新数据
@app.route('/update/<int:id>', methods=['PUT'])
def update_data(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        data = request.get_json()  # 获取PUT请求中的JSON数据

        # 更新ethernet表中的数据
        query = """
            UPDATE ethernet
            SET test_date=%s, test_team=%s, test_item=%s, driver_version=%s,
                firmware_version=%s, protocol_type=%s, client_ip=%s,
                port_mtu=%s, thread_num=%s, packet_length=%s, bandwidth=%s, 
                gb_average_rx=%s, gb_average_rx_cropped=%s, gb_average_tx=%s, gb_average_tx_cropped=%s
            WHERE id=%s
        """
        values = (data['test_date'], data['test_team'], data['test_item'],
                  data['driver_version'], data['firmware_version'], data['protocol_type'],
                  data['client_ip'], data['port_mtu'], data['thread_num'], data['packet_length'], data['bandwidth'],
                  data['gb_average_rx'], data['gb_average_rx_cropped'], data['gb_average_tx'],
                  data['gb_average_tx_cropped'], id)

        cursor.execute(query, values)
        connection.commit()

        return jsonify({'message': 'Data updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# API接口：删除数据
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_data(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # 删除ethernet表中指定id的数据
        cursor.execute("DELETE FROM ethernet WHERE id = %s", (id,))
        connection.commit()

        return jsonify({'message': 'Data deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# curl -X DELETE http://localhost:5000/delete_table
# API接口：删除整个表
@app.route('/delete_table', methods=['DELETE'])
def delete_table():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # 删除ethernet表
        cursor.execute("DROP TABLE IF EXISTS ethernet")
        connection.commit()

        return jsonify({'message': 'Table deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# curl -X POST http://localhost:5000/create_table
# API接口：创建表
@app.route('/create_table', methods=['POST'])
def create_table():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # 创建ethernet表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ethernet (
                id INT AUTO_INCREMENT PRIMARY KEY,
                test_date DATETIME,
                test_team VARCHAR(255),
                test_item VARCHAR(255),
                driver_version VARCHAR(255),
                firmware_version VARCHAR(255),
                protocol_type VARCHAR(255),
                client_ip VARCHAR(255),
                port_mtu INT,
                thread_num INT,
                packet_length VARCHAR(255),
                bandwidth VARCHAR(255),
                gb_average_rx FLOAT,
                gb_average_rx_cropped FLOAT,
                gb_average_tx FLOAT,
                gb_average_tx_cropped FLOAT
            )
        """)
        connection.commit()

        return jsonify({'message': 'Table created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/graph', methods=['GET'])
def show_graph():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # 查询ethernet表中的数据
        cursor.execute("SELECT client_ip, test_date, gb_average_rx, gb_average_rx_cropped, gb_average_tx, gb_average_tx_cropped FROM ethernet")
        data = cursor.fetchall()

        # 将查询结果转换为字典列表
        result = []
        for row in data:
            result.append({
                'client_ip': row[0],
                'test_date': row[1],
                'gb_average_rx': row[2],
                'gb_average_rx_cropped': row[3],
                'gb_average_tx': row[4],
                'gb_average_tx_cropped': row[5]
            })

        # 创建数据框
        df = pd.DataFrame(result)

        # 过滤掉值低于5的数据
        filtered_df = df[(df['gb_average_rx'] >= 0) & (df['gb_average_rx_cropped'] >= 0) &
                         (df['gb_average_tx'] >= 0) & (df['gb_average_tx_cropped'] >= 0)]

        # 按照client_ip分组，并为每个组绘制四条折线图
        fig = px.line(filtered_df, x='test_date', y=['gb_average_rx', 'gb_average_rx_cropped', 'gb_average_tx', 'gb_average_tx_cropped'],
                      color='client_ip',
                      title='Performance Data',
                      labels={'value': 'Throughput (GB/s)', 'variable': 'Metric', 'test_date': 'Test Date', 'client_ip': 'Client IP'})

        # 删除已存在的graph.html文件
        graph_html_path = './templates/graph.html'
        if os.path.exists(graph_html_path):
            os.remove(graph_html_path)

        # 保存新的graph.html文件
        fig.write_html(graph_html_path)

        # 返回包含折线图的HTML页面
        return render_template('graph.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# API接口：获取数据并返回折线图页面
@app.route('/graph2', methods=['GET'])
def show_graph2():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # 查询ethernet表中的数据
        cursor.execute("SELECT test_date, gb_average_rx, gb_average_rx_cropped, gb_average_tx, gb_average_tx_cropped FROM ethernet")
        data = cursor.fetchall()

        # 将查询结果转换为字典列表
        result = []
        for row in data:
            result.append({
                'test_date': row[0],
                'gb_average_rx': row[1],
                'gb_average_rx_cropped': row[2],
                'gb_average_tx': row[3],
                'gb_average_tx_cropped': row[4]
            })

        # 创建数据框
        df = pd.DataFrame(result)

        # 将DataFrame中的0替换为NaN
        # df.replace(0, np.nan, inplace=True)
        app.logger.info("Original DataFrame:")
        app.logger.info(df)

        # 过滤掉值低于5的数据
        filtered_df = df[(df['gb_average_rx'] >= 0) & (df['gb_average_rx_cropped'] >= 0) &
                         (df['gb_average_tx'] >= 0) & (df['gb_average_tx_cropped'] >= 0)]
        app.logger.info("Filtered DataFrame:")
        app.logger.info(filtered_df)

        # 绘制折线图
        fig = px.line(filtered_df, x='test_date', y=['gb_average_rx', 'gb_average_rx_cropped', 'gb_average_tx', 'gb_average_tx_cropped'],
                      title='Performance Data',
                      labels={'value': 'Throughput (GB/s)', 'variable': 'Metric', 'test_date': 'Test Date'})


        # 删除已存在的graph.html文件
        graph_html_path = './templates/graph.html'
        if os.path.exists(graph_html_path):
            os.remove(graph_html_path)

        # 保存新的graph.html文件
        fig.write_html(graph_html_path)

        # 返回包含折线图的HTML页面
        return render_template('graph.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# API接口：获取数据并在web表格中显示
@app.route('/display_table', methods=['GET'])
def display_table():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # 查询ethernet表中的数据
        cursor.execute("SELECT * FROM ethernet")
        data = cursor.fetchall()

        # 将查询结果转换为字典列表
        result = []
        for row in data:
            result.append({
                'id': row[0],
                'test_date': row[1],
                'test_team': row[2],
                'test_item': row[3],
                'driver_version': row[4],
                'firmware_version': row[5],
                'protocol_type': row[6],
                'client_ip': row[7],
                'port_mtu': row[8],
                'thread_num': row[9],
                'packet_length': row[10],
                'bandwidth': row[11],
                'gb_average_rx': row[12],
                'gb_average_rx_cropped': row[13],
                'gb_average_tx': row[14],
                'gb_average_tx_cropped': row[15]
            })

        # 返回渲染后的模板，并传递数据给模板
        return render_template('table.html', data=result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# curl -H "Content-Type: application/json" -X POST http://10.0.3.200:5000/replace_values
# API接口：将小于1的值改为0
@app.route('/replace_values', methods=['POST'])
def replace_values():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # 更新ethernet表中的数据，将小于1的值改为0
        cursor.execute("""
            UPDATE ethernet
            SET gb_average_rx = CASE WHEN gb_average_rx < 1 THEN 0 ELSE gb_average_rx END,
                gb_average_rx_cropped = CASE WHEN gb_average_rx_cropped < 1 THEN 0 ELSE gb_average_rx_cropped END,
                gb_average_tx = CASE WHEN gb_average_tx < 1 THEN 0 ELSE gb_average_tx END,
                gb_average_tx_cropped = CASE WHEN gb_average_tx_cropped < 1 THEN 0 ELSE gb_average_tx_cropped END
        """)
        connection.commit()

        return jsonify({'message': 'Values updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()



# 主页路由
@app.route('/')
def index():
    return 'Flask app with MySQL database is running!'


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
