from osgeo import gdal
from GF4_XML import *

def read_rpc(filepath):
    rpc_dict = {}
    with open(filepath) as f:
        text = f.read()
    words = ['errBias', 'errRand', 'lineOffset', 'sampOffset', 'latOffset',
             'longOffset', 'heightOffset', 'lineScale', 'sampScale', 'latScale',
             'longScale', 'heightScale', 'lineNumCoef', 'lineDenCoef','sampNumCoef', 'sampDenCoef',]
    keys = ['ERR_BIAS', 'ERR_RAND', 'LINE_OFF', 'SAMP_OFF', 'LAT_OFF', 'LONG_OFF',
            'HEIGHT_OFF', 'LINE_SCALE', 'SAMP_SCALE', 'LAT_SCALE',
            'LONG_SCALE', 'HEIGHT_SCALE', 'LINE_NUM_COEFF', 'LINE_DEN_COEFF',
            'SAMP_NUM_COEFF', 'SAMP_DEN_COEFF']

    for old, new in zip(words, keys):
        text = text.replace(old, new)
    text_list = text.split(';\n')
    text_list = text_list[3:-2]
    text_list[0] = text_list[0].split('\n')[1]
    text_list = [item.strip('\t').replace('\n', '').replace(' ', '') for item in text_list]

    for item in text_list:
        key, value = item.split('=')
        if '(' in value:
            value = value.replace('(', '').replace(')', '')
        rpc_dict[key] = value

    for key in keys[:12]:
        if not rpc_dict[key].startswith('-'):
            rpc_dict[key] = '+' + rpc_dict[key]
        if key in ['LAT_OFF', 'LONG_OFF', 'LAT_SCALE', 'LONG_SCALE']:
            rpc_dict[key] = rpc_dict[key] + ' degrees'
        if key in ['LINE_OFF', 'SAMP_OFF', 'LINE_SCALE', 'SAMP_SCALE']:
            rpc_dict[key] = rpc_dict[key] + ' pixels'
        if key in ['ERR_BIAS', 'ERR_RAND', 'HEIGHT_OFF', 'HEIGHT_SCALE']:
            rpc_dict[key] = rpc_dict[key] + ' meters'
    for key in keys[-4:]:
        values = []
        for item in rpc_dict[key].split(','):
            #print(item)
            if not item.startswith('-'):
                values.append('+'+item)
            else:
                values.append(item)
            rpc_dict[key] = ' '.join(values)
    return rpc_dict

def write_rpc(file, o_file, rpc_file):
    xmldata = read_xml('GF4_B1_E118.0_N24.0_20230728_L1A0000618715.xml')
    rpcdata = read_rpc(rpc_file)
    dataset = gdal.Open(file,gdal.GA_Update)
    metadata = xmldata | rpcdata
    dataset.SetMetadata(metadata,"RPC")
    del dataset
    
    # Only write Associated RPC Info? needs enhancement