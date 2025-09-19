# 开发人员：朱志涛
# 开发时间：
import os
import json
import gzip
import pandas as pd

month = '09'

folder_api_01_path = 'bill_data/api01/archived' + month + '/'
folder_api_02_path = 'bill_data/api02/archived' + month + '/'
folder_api_local_path = 'bill_data/api_local/archived' + month + '/'
api_user = 'xinyisou'

folder_api_bill_path = './bill_data/bill_result/'
UPSTREAM_FLAG = 'xa.account.flog.upstream'
DOWNSTREAM_FLAG = 'xa.account.flog.downstream'

upstream_data_dict = {
    'date': [],
    'interface_code': [],
    'request': [],
    'response': []
}

downstream_data_dict = {
    'date': [],
    'api_user_code': [],
    'interface_code': [],
    'msg': [],
    'uuid': []
}


# 根据号段获取运营商
def get_provider(phone_number):
    providers = {
        '1340': '中国移动',
        '1341': '中国移动',
        '1342': '中国移动',
        '1343': '中国移动',
        '1344': '中国移动',
        '1345': '中国移动',
        '1346': '中国移动',
        '1347': '中国移动',
        '1348': '中国移动',
        '135': '中国移动',
        '136': '中国移动',
        '137': '中国移动',
        '138': '中国移动',
        '139': '中国移动',
        '147': '中国移动',
        '148': '中国移动',
        '150': '中国移动',
        '151': '中国移动',
        '152': '中国移动',
        '157': '中国移动',
        '158': '中国移动',
        '159': '中国移动',
        '165': '中国移动',
        '1703': '中国移动',
        '1705': '中国移动',
        '1706': '中国移动',
        '172': '中国移动',
        '178': '中国移动',
        '182': '中国移动',
        '183': '中国移动',
        '184': '中国移动',
        '187': '中国移动',
        '188': '中国移动',
        '195': '中国移动',
        '197': '中国移动',
        '198': '中国移动',
        '130': '中国联通',
        '131': '中国联通',
        '132': '中国联通',
        '145': '中国联通',
        '146': '中国联通',
        '155': '中国联通',
        '156': '中国联通',
        '166': '中国联通',
        '167': '中国联通',
        '1704': '中国联通',
        '1707': '中国联通',
        '1708': '中国联通',
        '1709': '中国联通',
        '171': '中国联通',
        '175': '中国联通',
        '176': '中国联通',
        '185': '中国联通',
        '186': '中国联通',
        '196': '中国联通',
        '133': '中国电信',
        '1349': '中国电信',
        '149': '中国电信',
        '153': '中国电信',
        '162': '中国电信',
        '1700': '中国电信',
        '1702': '中国电信',
        '173': '中国电信',
        '1740': '中国电信',
        '177': '中国电信',
        '180': '中国电信',
        '181': '中国电信',
        '189': '中国电信',
        '190': '中国电信',
        '191': '中国电信',
        '193': '中国电信',
        '199': '中国电信',
    }
    if phone_number is None or isinstance(phone_number, list):
        return '不适用'
    for pattern in providers:
        if phone_number.startswith(pattern):
            return providers[pattern]
    print(phone_number)
    return '未知运营商'


# 获取指定文件夹内所有文件和文件夹的名称
def get_filenames(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


# 获取日志中的json数据
def extract_json(text):
    try:
        # 假设JSON以花括号开始和结束
        start_index = text.index('{')
        end_index = text.rindex('}')
        json_str = text[start_index:end_index + 1]
        json_data = json.loads(json_str)
        return json_data
    except (ValueError, json.JSONDecodeError):
        return None


def get_data_frame(data, date_type):
    date_array = data['invocationTime']
    if len(date_array) > 5:
        date = str(date_array[0]) + '-' + str(date_array[1]) + '-' + str(date_array[2]) + ' ' + str(
            date_array[3]) + ':' + str(date_array[4]) + ':' + str(date_array[5])
    else:
        date = str(date_array[0]) + '-' + str(date_array[1]) + '-' + str(date_array[2]) + ' ' + str(
            date_array[3]) + ':' + str(date_array[4]) + ':00'
    interface_code = data['interfaceCode']
    if date_type == UPSTREAM_FLAG:
        upstream_data_dict['date'].append(date)
        upstream_data_dict['interface_code'].append(interface_code)
        upstream_data_dict['request'].append(data['request']['request'])
        upstream_data_dict['response'].append(data['responsePayload'])


def get_data_info(file_path, file_list):
    for api_file in file_list:
        if api_file.endswith('.gz'):
            with gzip.open(file_path + api_file, 'rt', encoding='utf-8') as file:
                for line in file:
                    # print(line.strip())
                    line_json = extract_json(line.strip())
                    is_exception = line_json['exception']
                    interface_code = line_json['interfaceCode']
                    if not is_exception:
                        if line.__contains__(UPSTREAM_FLAG):
                            upstream_name = line_json['upstreamInfo']['upstreamName']
                            if upstream_name == api_user:
                                get_data_frame(line_json, UPSTREAM_FLAG)


file_01_names = get_filenames(folder_api_01_path)
file_01_names.sort()
file_02_names = get_filenames(folder_api_02_path)
file_02_names.sort()
file_local_names = get_filenames(folder_api_local_path)
file_local_names.sort()

get_data_info(folder_api_01_path, file_01_names)

get_data_info(folder_api_02_path, file_02_names)

get_data_info(folder_api_local_path, file_local_names)

upstream_data_frame = pd.DataFrame(upstream_data_dict)

upstream_data_frame.columns = ['时间', '接口', '入参', '出参']

out_Path = './bill_data/bill_result/bill_detail_' + api_user + '_' + month + '.xlsx'

writer = pd.ExcelWriter(out_Path, engine='xlsxwriter')

upstream_data_frame.to_excel(writer, sheet_name='上游', index=False)
writer.close()

