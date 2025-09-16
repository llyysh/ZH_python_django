import pandas as pd
import pymysql  # 替换为pymysql库
from pymysql import OperationalError  # pymysql的错误类
import os
import glob2

def get_sql_type(dtype):
    """根据pandas数据类型推断MySQL数据类型"""
    if pd.api.types.is_integer_dtype(dtype):
        return "INT"
    elif pd.api.types.is_float_dtype(dtype):
        return "FLOAT"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "DATETIME"
    elif pd.api.types.is_bool_dtype(dtype):
        return "TINYINT(1)"
    else:
        return "VARCHAR(255)"

def import_xlsx_to_mysql(file_path, cursor, connection):
    """导入单个XLSX文件到MySQL，表名与文件名相同"""
    try:
        # 获取文件名（不含扩展名）作为表名
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        # 清理表名，移除特殊字符
        table_name = file_name.replace(' ', '_').replace('-', '_').replace('.', '_').replace('(', '').replace(')', '')
        
        print(f"开始处理文件: {file_path}，目标表名: {table_name}")
        
        # 读取XLSX文件（默认读取第一个工作表）
        df = pd.read_excel(file_path)
        
        if df.empty:
            print(f"警告: 文件 {file_path} 内容为空，已跳过")
            return
        
        # 清理列名
        clean_columns = [col.replace(' ', '_').replace('-', '_').replace('.', '_').replace('(', '').replace(')', '') 
                        for col in df.columns]
        
        # 创建表（如果不存在）
        create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ("
        for i, col in enumerate(clean_columns):
            col_type = get_sql_type(df.dtypes[i])
            create_table_query += f"`{col}` {col_type}, "
        
        create_table_query = create_table_query[:-2] + ")"
        cursor.execute(create_table_query)
        
        # 准备插入语句
        insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in clean_columns])}) VALUES ({', '.join(['%s'] * len(clean_columns))})"
        
        # 分块插入数据
        chunk_size = 5000
        total_rows = 0
        
        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i:i+chunk_size]
            chunk = chunk.where(pd.notnull(chunk), None)
            data = [tuple(row) for row in chunk.values]
            cursor.executemany(insert_query, data)
            total_rows += len(chunk)
        
        connection.commit()
        print(f"成功导入 {total_rows} 行数据到表 {table_name}")
        
    except OperationalError as e:
        print(f"数据库错误 (文件 {file_path}): {e}")
        connection.rollback()
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")
        connection.rollback()

def batch_import_from_folder(folder_path, db_config):
    """批量导入文件夹中所有XLSX文件"""
    try:
        # 使用pymysql连接MySQL数据库
        connection = pymysql.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
            charset='utf8mb4'  # pymysql建议指定字符集
        )
        
        if connection.open:  # pymysql用open属性判断连接状态
            cursor = connection.cursor()
            
            # 查找所有Excel文件
            xlsx_files = glob2.glob(os.path.join(folder_path, '**', '*.xlsx'))
            xlsx_files += glob2.glob(os.path.join(folder_path, '**', '*.xls'))
            
            if not xlsx_files:
                print("未找到任何Excel文件 (.xlsx 或 .xls)")
                return
            
            print(f"共发现 {len(xlsx_files)} 个Excel文件，开始导入...")
            
            # 逐个处理文件
            for file_path in xlsx_files:
                import_xlsx_to_mysql(file_path, cursor, connection)
            
            print("所有文件处理完成")
            
    except OperationalError as e:
        print(f"数据库连接错误: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()
            print("数据库连接已关闭")


if __name__ == "__main__":
    # 配置数据库连接信息
    db_config = {
        'host': 'localhost',       # 数据库主机地址
        'database': 'zhonghu_test',     # 数据库名称
        'user': 'django_user',   # 数据库用户名
        'password': 'mypassword'# 数据库密码
    }
    
    # 包含XLSX文件的文件夹路径
    folder_path = 'F:\\zh_mysql_test'  # 替换为你的文件夹路径
    
    # 执行批量导入
    batch_import_from_folder(folder_path, db_config)
    