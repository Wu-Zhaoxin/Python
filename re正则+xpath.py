# -*- coding = utf-8 -*-
# @Time : 2022/4/7 17:53
# @Author : WZX
# @File : .py
# @Software : PyCharm

from lxml import etree
# import re


# lst = re.findall(r"\d+", "difsh分的高分gdgre非官方大哥忽1122然感觉很容易奴家1245哈密瓜计划")
# print(lst)
#
# # 主要
# it = re.finditer(r"\d+", "difsh分的高分gdgre非官方大哥1122忽然感觉很容易奴家1245哈密瓜计划")
# for i in it:
#     print(i)
#     print(i.group())
#
# s = re.search(r"\d+", "difsh分的高分gdgre非官1122方大哥忽然感觉很容易奴家1245哈密瓜计划")
# print(s)
# print(s.group())
#
# # 匹配开头
# k = re.match(r"\d+", "999difsh分的高分gdgre非官1122方大哥忽然感觉很容易奴家1245哈密瓜计划")
# print(k)
# print(k.group())
#
# # 预加载正则（提高效率）：
#
# obj = re.compile(r"\d+")  # compile编译
# ret = obj.finditer("dfdghueri非但不会跟你你nets56发给你回复354")
# for it in ret:
#     print(it.group())

# Xpath:
xml = '''
<grandfather>爷爷
    <father>父亲
        <son>儿子
            <baby>宝贝</baby>
            <baby_1>宝贝1</baby_1>
        </son>
    </father>
</grandfather>
'''
tree = etree.XML(xml)
result = tree.xpath("/grandfather/father/son/baby/text()")
print(result)