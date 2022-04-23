# -*- coding = utf-8 -*-
# @Time : 2022/4/23 9:11
# @Author : WZX
# @File : .py
# @Software : PyCharm

import time
import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
from lxml import etree
import aiofiles
import subprocess
import pprint
import json
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def main():
    baseurl = input("输入网址：")
    page, headers, proxies = get_page(baseurl)
    amount, urls = find_series(page, baseurl)
    series_v, series_a, title_all = get_series(urls)
    download(series_v, series_a, headers)
    combine(amount, title_all)

    # asyncio.run(async_main(series))


# 1.获取主页面
def get_page(baseurl):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
        # 溯源防盗链：
        "referer": "https://www.bilibili.com/video/BV1G34y1x7Tu?spm_id_from=333.851.b_7265636f6d6d656e64.4"
    }

    proxies = {
        "https": "https://代理ip"
    }

    resp = requests.get(baseurl, headers=headers)
    page = BeautifulSoup(resp.text, "html.parser")
    return page, headers, proxies


# 2.获取集数
def find_series(page, baseurl):
    amount = page.find("div", id="multi_page").find("span").text
    amount = re.findall(r"/(.+?)[)]", amount)
    amount = int(amount[0])
    print(amount)

    # sys.exit()
    urls = []
    for i in range(1, int(amount) + 1):
        one_url = baseurl + "?p=" + str(i)
        urls.append(one_url)

    return amount, urls


# 单集解析方法
def get_series(urls):
    title_all = []
    series_v = []
    series_a = []
    i = 0

    # 获取标题
    resp = requests.session().get(urls[0])
    html_data = re.findall('"pages":(.*?),"subtitle"', resp.text)
    dics_str = html_data[0]
    titles = json.loads(dics_str)
    for j in titles:
        one = j['part']
        title_all.append(one)
    print(title_all)

    # sys.exit()

    for url in urls:
        resp = requests.session().get(url)

        # 视频链接获取
        one_v = etree.HTML(resp.text).xpath("/html/head/script[4]/text()")
        str = one_v[0].split("window.__playinfo__=")[1]
        link = re.findall(r"baseUrl(.+?)base_url", str)[0]
        link = re.sub('["]', '', link).strip(':')
        series_v.append(link)
        # 音频链接获取
        html_data = re.findall('window.__playinfo__=(.*?)</script>', resp.text)[0]
        json_data = json.loads(html_data)
        # pprint.pprint(json_data)
        audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
        series_a.append(audio_url)

        i = i + 1
        print("完成第%d个链接" % i)
        # time.sleep(1)
    # print(series_v, series_a)
    return series_v, series_a, title_all


def download(series_v, series_a, headers):
    tn = 0
    with ThreadPoolExecutor(80) as t:
        for one_seriesv, one_seriesa in zip(series_v, series_a):
            tn += 1
            t.submit(download_va, one_seriesv=one_seriesv, one_seriesa=one_seriesa, series_v=series_v, series_a=series_a, headers=headers)
            print("线程：%d" % tn)

    print("Download Finished!")


def download_va(one_seriesv, one_seriesa, series_v, series_a, headers):
    num = int(series_v.index(one_seriesv)) + 1
    trytimes = 6
    for l in range(1, trytimes):
        try:
            respv = requests.get(one_seriesv, headers=headers, timeout=10)
            respa = requests.get(one_seriesa, headers=headers, timeout=10)
            if respv.status_code == 200 and respa.status_code == 200:
                with open(rf'video\{series_v.index(one_seriesv)}.mp4', mode="wb") as f:
                    f.write(respv.content)
                    print("写入第%d个视频文件" % num)

                with open(rf'audio\{series_a.index(one_seriesa)}.mp3', mode="wb") as f:
                    f.write(respa.content)
                    print("写入第%d个音频文件" % num)
                break
        except Exception as e:
            print(e)
            print(f'本次请求失败 {l} 次')
            time.sleep(2)


def combine(amount, title_all):
    # title = os.path.splitext(video)
    for i in range(1, amount + 1):

        # .\ffmpeg.exe -i 输入视频 -i 输入音频 -c:v copy -c:a copy 输出视频
        # 示例：
        # .\ffmpeg.exe -i "AVC FHD 24fps.mp4" -i "AAC 329kbps.m4a" -c:v copy -c:a copy "Output FHD AAC.mp4"

        cmd = f'ffmpeg -i "C:/Users/Wu Zhaoxin/PycharmProjects/Work/video/{i}.mp4" -i "C:/Users/Wu Zhaoxin/PycharmProjects/Work/audio/{i}.mp3" -c:v copy -c:a aac -strict experimental "C:/Users/Wu Zhaoxin/PycharmProjects/Work/combinemp4/{i}.{title_all[i - 1]}.mp4"'
        subprocess.run(cmd, shell=True)
        print(title_all[i-1], "完成合并！")


# async def aio_download(url, i):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as resp:
#             # for i in range(len(series)):
#                 async with aiofiles.open(rf'video\{i}.mp4', mode="wb") as f:
#                     await f.write(await resp.content.read())
#                     print("写入第%s视频文件" % i)
#                     # f.close()


# async def async_main(series):
#     i = 0
#     tasks = []
#     for one_series in series:
#         tasks.append(aio_download(one_series, i))
#         i = i + 1
#
#     await asyncio.wait(tasks)


if __name__ == "__main__":
    t1 = time.time()
    main()
    t2 = time.time()
    print(t2 - t1)
