# -*- coding = utf-8 -*-
# @Time : 2022/5/2 9:23
# @Author : WZX
# @File : .py
# @Software : PyCharm


import time
import requests
from bs4 import BeautifulSoup
import re
from lxml import etree
import aiofiles
import subprocess
import pprint
import json
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
# 下载异步
import asyncio
# 访问异步
import aiohttp
# io写入操作异步
import aiofiles


def main():
    baseurl = input("输入网址：")
    # baseurl = "https://www.bilibili.com/video/BV1oD4y1o79h"
    page, headers, proxies = get_page(baseurl)
    amount, urls = find_series(page, baseurl)
    title_all = get_series(urls)
    asyncio.run(task_list(urls))
    download(headers)
    # combine(amount, title_all)
    asyncio.run(combine_list(amount, title_all))


# 1.获取主页面
def get_page(baseurl):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
        # 溯源防盗链：
        "referer": "https://www.bilibili.com/video/BV1G34y1x7Tu?spm_id_from=333.851.b_7265636f6d6d656e64.4"
    }

    proxies = {
        "https": "https://103.80.83.48"
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
    print(urls)
    return amount, urls


# 3.获取所有标题
def get_series(urls):
    title_all = []
    # 获取标题
    resp = requests.session().get(urls[0])
    html_data = re.findall('"pages":(.*?),"subtitle"', resp.text)
    dics_str = html_data[0]
    titles = json.loads(dics_str)
    for j in titles:
        one = j['part']
        title_all.append(one)
    print(title_all)
    return title_all

# 异步二层链接下载
async def down_va(url, urls):
        # resp = aiohttp.ClientSession().get(url)
        resp = requests.session().get(url)
        # with aiohttp.ClientSession() as session:
        #     with session.get(url) as resp:
        # 视频链接获取
        one_v = etree.HTML(resp.text).xpath("/html/head/script[4]/text()")
        str = one_v[0].split("window.__playinfo__=")[1]
        video_link = re.findall(r"baseUrl(.+?)base_url", str)[0]
        video_link = re.sub('["]', '', video_link).strip(':')
        with open(f"series_a.txt", mode="a") as f1:
            f1.write(video_link + "\n")

        # 音频链接获取
        html_data = re.findall('window.__playinfo__=(.*?)</script>', resp.text)[0]
        json_data = json.loads(html_data)
        # pprint.pprint(json_data)
        audio_link = json_data['data']['dash']['audio'][0]['baseUrl']
        with open(f"series_v.txt", mode="a") as f2:
            f2.write(audio_link + "\n")

        print("完成第%d个链接" % (int(urls.index(url)) + 1))


async def task_list(urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(down_va(url, urls), name="第%d个协程对象" % (int(urls.index(url)) + 1))
        tasks.append(task)

    done, pending = await asyncio.wait(tasks, timeout=None)
    print(done)


def download(headers):
    tn = 0
    file = open('series_v.txt')
    series_v = file.readlines()

    file = open('series_a.txt')
    series_a = file.readlines()

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
                with open(rf'video\{num}.mp4', mode="wb") as f:
                    f.write(respv.content)
                    print("写入第%d个视频文件" % num)

                with open(rf'audio\{num}.mp3', mode="wb") as f:
                    f.write(respa.content)
                    print("写入第%d个音频文件" % num)
                break
        except Exception as e:
            print(e)
            print(f'本次请求失败 {l} 次')
            time.sleep(2)


async def combine(i, title_all):
        cmd = f'ffmpeg -i "C:/Users/Wu Zhaoxin/PycharmProjects/Work/video/{i}.mp4" -i "C:/Users/Wu Zhaoxin/PycharmProjects/Work/audio/{i}.mp3" -c:v copy -c:a aac -strict experimental "C:/Users/Wu Zhaoxin/PycharmProjects/Work/combinemp4/{i}.{title_all[i - 1]}.mp4"'
        subprocess.run(cmd, shell=True)
        print(title_all[i-1], "完成合并！")


async def combine_list(amount, title_all):
    tasks = []
    for i in range(1, amount + 1):
        task = asyncio.create_task(combine(i, title_all), name="第%d个协程对象" % i)
        tasks.append(task)

    done, pending = await asyncio.wait(tasks, timeout=None)
    print(done)


if __name__ == "__main__":
    t1 = time.time()
    main()
    t2 = time.time()
    print(t2 - t1)

