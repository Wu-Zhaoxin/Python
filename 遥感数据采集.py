#encoding=utf8
import requests
import json
import pandas as pd
import time
from concurrent.futures import  ThreadPoolExecutor

stadic={}
col= ['卫星'    , '载荷', '采集时间', '左上角纬度', '左上角经度', '右上角纬度', '右上角经度', '景中心纬度', '景中心经度', '右下角纬度', '右下角经度', '左下角纬度', '左下角经度', '接收站',       '轨道圈号',  '景path',  '景row', '星下点path',    '星下点row',   '产品起始行时间', '产品中间行时间', '产品结束行时间', '产品级别', '景序列号', '产品序列号', '生产日期', '产品谱段', '产品谱段数', '产品分辨率（米）', '产品类型', '连续景数', '浮动比例', '产品格式', '产品宽度（像素）', '产品高度（像素）', '原始数据条带号', '云覆盖量', '产品大小', '椭球模型', '重采样方法', '辐射校正方法', 'dem数据来源', '地图投影', '投影带号', '地球模型', '产品波段数', '产品生产时间', '产品分辨率', '景数目', '景漂移', '产品格式', '产品宽度', '产品高度', '原始数据条带号', '云覆盖量', '产品大小', '椭球模型', '重采样方法', '辐射校正方法', '高程模型', '投影方式', '投影带号', '生产方式',  '卫星平台平均航偏角（度）', '卫星平台平均俯仰角（度）', '卫星平台滚动角（度）', '卫星方位角（度）', '卫星高度角（度）', '相机侧视角（度）', '太阳高度角/天顶角（度）', '太阳方位角（度）', '相机前后视角（度）', '增益模式', '积分时间（秒）', '积分级数']
col2=['卫星代号', '载荷', '接收时间', '左上纬度'  , '左上经度'  , '右上纬度'  , '右上经度'  , '中心纬度'  ,  '中心经度' , '右下纬度'  , '右下经度'  , '左下纬度'  , '左下经度' , '接收地面站代号', '轨道圈号', '景Path', '景Row', '卫星星下点Path', '卫星星下点Row', '产品起始时间', '产品中间时间',   '产品终止时间',   '产品级别', '景号', '产品号','生产日期', '产品谱段', '产品谱段数', '产品分辨率（米）', '产品类型', '连续景数', '浮动比例', '产品格式', '产品宽度（像素）', '产品高度（像素）', '原始数据条带号', '云覆盖量', '产品大小', '椭球模型', '重采样方法', '辐射校正方法', 'dem数据来源', '地图投影', '投影带号', '地球模型', '产品波段数', '产品生产时间', '产品分辨率', '景数目', '景漂移', '产品格式', '产品宽度', '产品高度', '原始数据条带号', '云覆盖量', '产品大小', '椭球模型', '重采样方法', '辐射校正方法', '高程模型', '投影方式', '投影带号', '生产方式',                                                       '卫星平台平均航偏角',     '卫星平台平均俯仰角',          '卫星平台滚动角',      '卫星方位角',       '卫星高度角',      '相机侧视角',              '太阳方位角', '太阳高度角/天顶角', '相机前后视角',       '增益模式', '    积分时间', '积分级数']
header={
    'Accept': 'application/json, text/plain, */*',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'access-agent': 'pc-dss',
'Connection': 'keep-alive',
'Content-Type': 'application/json;charset=UTF-8',
'Host': '36.112.130.153:7777',
'ipaddr': '',
'murmur': '298f4d7ef9ace8b08e76c07078242fda',
'Origin': 'http://36.112.130.153:7777',
'Referer': 'http://36.112.130.153:7777/',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}
locations=[

                #---------------------
                #此处按照格式修改坐标
                #---------------------
                "POINT(109.6155 40.8658)",
                "POINT(94.3935 40.09251)",
                "POINT(96.215806 37.32247)",
                "POINT(94.259857 36.430882)",
                "POINT(93.844158 36.606055)",
                "POINT(23.39 28.55)",
                "POINT(13.35 24.42)",
                "POINT(7.66 30.32)",
                "POINT(2.23 31.02)",
                "POINT(-9.3 19.4)",
                "POINT(-8.78 20.85)",
                "POINT(115.69 38.497)",
                "POINT(4.864167 43.558889)",
                "POINT(15.0409 -23.56)",
                "POINT(100 37)",
                "POINT(113.09555 34.5361)",
                "POINT(102.46889 24.21528)"
            ]

def getoneid(item):
    id, location=item
    iddic={}
    url='http://36.112.130.153:7777/manage/meta/api/metadatas/record?id='+id
    while True:
        try:
            dic=requests.get(url,headers=header,timeout=1).json()
            break
        except:
            time.sleep(1)
            print('超时')
    #提取网页内容 然后附加在列表中
    result=dic['result'][0]
    other=result['other']
    base = result['base']
    system = result['system']
    iddic.update(base)
    iddic.update(system)
    iddic.update(other)
    #提取数据
    one = []
    for keyindex in range(len(col)):
        if col[keyindex] in iddic:
            one.append(str(iddic[col[keyindex]]))
        elif col2[keyindex] in iddic:
            one.append(str(iddic[col2[keyindex]]))
        else:
            one.append('')
    print(one)
    stadic[location].append(one)
#填写参数 F12.网络：XHR post标头+payload参数(xhr，全称为XMLHttpRequest，用于与服务器交互数据，是ajax功能实现所依赖的对象，jquery中的ajax就是对
#xhr的封装) F12.网络：Headers：请求头（请求方式+url+Http版本）
def main(location):
    stadic[location] = []
    url='http://36.112.130.153:7777/manage/meta/api/metadatas/records'
    page=0
    while True:
        page+=1
        payload={
            "page": page,
            "size": 3000,
            "geom": [
                location
            ],
            "scenetime": [
                "2018-01-01",
                "2022-01-24"
            ],
            "satelliteSensor": [

                # ---------------------
                # 此处按照格式修改卫星
                # ---------------------
                "GF1B_PMS",
                "GF1C_PMS",
                "GF1D_PMS",
                "GF4_PMS",
                "GF4_PMI",
                "GF4_IRS",
                "GF5_VIMS",
                "GF6_PMS",
                "GF6_WFV",
                "GF7_DLC",
                "CB04A_WPM",
                "CB04A_MUX",
                "CB04A_WFI",
                "ZY02C_PMS",
                "ZY1E_VNIC",
                "ZY3_MUX",
                "ZY302_TMS",
            ],
            "prodlevel": "1",
            "cloudpsd": 100,
            "dwxtype": "gx",
            "userType": 0,
            "userId": "",
            "crossed": 'false',
            "userName": "",
            "name": "",
            "mobile": ""
        }
        #关键：请求返回信息中包含id  html中也包含id 都可以提取详情页内容
        res=requests.post(url,data=json.dumps(payload),headers=header)
        dic=res.json()
        result=dic['result']
        maplist=[]
        for i in result:
            maplist.append([i['id'],location])
        with ThreadPoolExecutor(10) as ex:
            ex.map(getoneid,maplist)
        if len(result)<2000:
            df = pd.DataFrame(stadic[location], columns=col)
            df.to_excel(location+'.xlsx', index=None)
            return
if __name__ == '__main__':
    for location in locations:
        main(location)



