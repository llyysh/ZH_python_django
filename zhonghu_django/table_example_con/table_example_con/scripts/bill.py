# 开发人员：朱志涛
# 开发时间：
import os
import json
import gzip
import pandas as pd

month = '2502'

folder_api_01_path = 'bill_data/api01/archived' + month + '/'
folder_api_02_path = 'bill_data/api02/archived' + month + '/'
folder_api_local_path = 'bill_data/api_local/archived' + month + '/'
folder_api_bill_path = './bill_data/bill_result/'
UPSTREAM_FLAG = 'xa.account.flog.upstream'
DOWNSTREAM_FLAG = 'xa.account.flog.downstream'

upstream_price_dict = {

}

AlwaysChargeStrategy = [
    'checkMobileNameIdCardAccountNumberV4',
    'checkNameIdCardAccountNumberV4',
    'checkNameAccountNumberV4',
    'getEntLitigationSXBZXROrgInfo',
    'getEntLitigationSXBZXRPersonInfo',
    'getEntLitigationXGBZXROrgInfo',
    'getEntLitigationXGBZXRPersonInfo',
    'getEntLitigationOutOrgInfo',
    'getEntLitigationOutPersonInfo',
    'getPunishInfo',
    'getCopyRightsInfo',
    'getCopyRightProductionInfo',
    'getICPRegInfo',
    'getEntTaxBlackInfo',
    'getEntTaxALevelInfo',
    'getEntPatentFullInfo',
    'getCourtSearchInfo',
    'getEntInvestmentAbroadInfoV2',
    'getEntLawPersonInvestmentInfoV2',
    'getEntLawPersontoOtherInfoV2',
    'queryBlackNumber',
    'queryBlackNumberBatch'
]

downstream_price_dict = {
    'user_bozhongweichuang_idCardUsernameCheck': '0.03500',
    'user_changchengyidong_idCardUsernameCheck': '0.05000',
    'user_fanghuachengzhang_queryEntOperateAddressInfo': '1.00000',
    'user_hangtoubigdata_getFourElementCheckInfo': '0.30000',
    'user_herongchangsheng_getIndividualInfo': '0.02000',
    'user_herongchangsheng_getThreeElementCheckInfoV2': '0.01600',
    'user_herongchangsheng_getTwoElementCheckInfo': '0.01300',
    'user_herongchangsheng_getRegisterInfoV2': '0.02000',
    'user_herongchangsheng_getOrgCombineInfo': '0.05000',
    'user_huadaoNY_queryEntPersonAppointmentInfo': '0.40000',
    'user_huadaoNY_getFourElementCheckInfo': '0.40000',
    'user_huadaoNY_idCardUsernameCheck': '0.05000',
    'user_jinruikeji_idCardUsernameCheck': '0.01300',
    'user_pinansec_generalMatchTwoElementWithISP': '0.20000',
    'user_shenzhouyunhe_getRegisterInfoV2': '0.04000',
    'user_shitongkeji_queryEntPersonAppointmentInfo': '0.28000',
    'user_shitongkeji_getEntLitigationSXBZXRPersonInfo': '0.03000',
    'user_shitongkeji_idCardUsernameCheck': '0.03000',
    'user_shitongkeji_getEntLitigationOutPersonInfo': '0.30000',
    'user_shitongkeji_queryRiskInfoByIdName': '0.22000',
    'user_tiandihexing_idNameImageCheck': '0.10000',
    'user_tiandihexing_idCardUsernameCheck': '0.01500',
    'user_xinshukeji_queryPersonAppointmentInfoMD5': '0.25000',
    'user_xinshukeji_queryPersonAppointmentInfoSHA256': '0.25000',
    'user_xinshukeji_queryEntPersonAppointmentInfo': '0.25000',
    'user_xinshukeji_idCardUsernameCheck': '0.05000',
    'user_yikatong_2_idNameImageCheck': '0.16000',
    'user_youkushengshi_idCardUsernameCheck': '0.10000',
    'user_zhongshengXYGL_getAdministrativePenaltyInfo': '0.30000',
    'user_zhongshengXYGL_getEntLitigationSXBZXRPersonInfo': '0.50000',
    'user_zhongshengXYGL_getEntLitigationSXBZXROrgInfo': '0.50000',
    'user_zhongshengXYGL_getEntLitigationOutPersonInfo': '0.50000',
    'user_zhongshengXYGL_getEntLitigationOutOrgInfo': '0.50000',
    'user_zhongshengXYGL_getEntLitigationXGBZXRPersonInfo': '0.50000',
    'user_zhongshengXYGL_getEntLitigationXGBZXROrgInfo': '0.50000',
    'user_shujubao_idCardUsernameCheck': '0.01750'
}

upstream_data_dict = {
    'date': [],
    'api_user_code': [],
    'interface_code': [],
    'isp_code': [],
    'amount': [],
    'price': [],
    'upstream_code': [],
    'upstream_interface_code': []
}

downstream_data_dict = {
    'date': [],
    'api_user_code': [],
    'interface_code': [],
    'isp_code': [],
    'amount': [],
    'price': []
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
    date = str(date_array[0]) + '-' + str(date_array[1]) + '-' + str(date_array[2])
    api_user_code = data['apiUserCode']
    interface_code = data['interfaceCode']
    if date_type == UPSTREAM_FLAG:
        upstream_code = data['upstreamInfo']['upstreamName']
        upstream_data_dict['date'].append(date)
        upstream_data_dict['api_user_code'].append(api_user_code)
        upstream_data_dict['interface_code'].append(interface_code)
        upstream_data_dict['amount'].append(1)
        upstream_data_dict['upstream_code'].append(data['upstreamInfo']['upstreamName'])
        upstream_data_dict['upstream_interface_code'].append(data['upstreamInfo']['upstreamInterfaceCode'] or '')
        price_key = upstream_code + '_' + interface_code
        if price_key in upstream_price_dict:
            upstream_data_dict['price'].append(upstream_price_dict[price_key])
        else:
            upstream_data_dict['price'].append(0)
        if 'mobile' in data['request']['request']:
            if 'isp' in data['responsePayload']['responsePayload'] and data['responsePayload']['responsePayload']['isp'] is not None:
                upstream_data_dict['isp_code'].append(data['responsePayload']['responsePayload']['isp'])
            else:
                upstream_data_dict['isp_code'].append(get_provider(data['request']['request']['mobile']))
        else:
            upstream_data_dict['isp_code'].append('不适用')
    else:
        downstream_data_dict['date'].append(date)
        downstream_data_dict['api_user_code'].append(data['apiUserCode'])
        downstream_data_dict['interface_code'].append(data['interfaceCode'])
        downstream_data_dict['amount'].append(1)
        price_key = api_user_code + '_' + interface_code
        if price_key in downstream_price_dict:
            downstream_data_dict['price'].append(downstream_price_dict[price_key])
        else:
            downstream_data_dict['price'].append('0')
        if 'mobile' in data['request']['request']:
            if 'isp' in data['response']['payload'] and data['response']['payload']['isp'] is not None:
                downstream_data_dict['isp_code'].append(data['response']['payload']['isp'])
            else:
                downstream_data_dict['isp_code'].append(get_provider(data['request']['request']['mobile']))
        else:
            downstream_data_dict['isp_code'].append('不适用')


def get_data_info(file_path, file_list):
    for api_file in file_list:
        if api_file.endswith('.gz'):
            with gzip.open(file_path + api_file, 'rt',encoding='utf-8') as file:
                for line in file:
                    # print(line.strip())
                    line_json = extract_json(line.strip())
                    is_exception = line_json['exception']
                    interface_code = line_json['interfaceCode']
                    if not is_exception:
                        if line.__contains__(UPSTREAM_FLAG):
                            if line_json['responsePayload']['upstreamChargable']:
                                get_data_frame(line_json, UPSTREAM_FLAG)
                        elif line.__contains__(DOWNSTREAM_FLAG):
                            if line_json['chargable']:
                                get_data_frame(line_json, DOWNSTREAM_FLAG)
                        else:
                            print("错误！！！")


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
downstream_data_frame = pd.DataFrame(downstream_data_dict)
upstream_data_frame.columns = ['日期', '用户', '接口', '运营商', '数量', '单价', '上游', '上游接口']
downstream_data_frame.columns = ['日期', '用户', '接口', '运营商', '数量', '单价']

upstream_result = upstream_data_frame.groupby(['上游', '上游接口', '运营商', '单价'], as_index=True)['数量'].value_counts().reset_index(
    name='count')
downstream_result = downstream_data_frame.groupby(['用户', '接口', '运营商', '单价'], as_index=True)[
    '数量'].value_counts().reset_index(
    name='count')
upstream_result.columns = ['上游', '接口', '运营商', '单价', '数量1', '数量']
downstream_result.columns = ['用户', '接口', '运营商', '单价', '数量1', '数量']

print(upstream_result)
print(downstream_result)
out_Path = './bill_data/bill_result/bill' + month + '.xlsx'

writer = pd.ExcelWriter(out_Path, engine='xlsxwriter')
upstream_result.to_excel(writer, sheet_name='上游', index=False)
downstream_result.to_excel(writer, sheet_name='客户', index=False)
writer.close()
# format_excel(writer, '上游', upstream_result)
# format_excel(writer, '客户', downstream_result)
