# pxy7896@foxmail.com
# 2020/8/1

__doc__ = """
获取中公教育每日一练内容；获取国务院政府工作报告。
"""

import requests
from bs4 import BeautifulSoup
import os


# 服务器反爬虫机制会判断客户端请求头中的User-Agent是否来源于真实浏览器，所以，我们使用Requests经常会指定UA伪装成浏览器发起请求
headers = {'user-agent': 'Mozilla/5.0'}

# 写文件
def writedoc(raw_ss, i, ii):
    # 打开文件
    # 编码为utf-8
    start = raw_ss.find("模拟试题")
    end = raw_ss.find("免责声明")
    ss = raw_ss[start+5: end-5]
    with open("result\\第" + str(ii) + "页.txt", 'a', encoding='utf-8') as f:
        # 写文件
        f.write(ss + "\n\n")
    #print("问题" + str(i) + "文件写入完成" + "\n")

# 根据详细页面url获取目标字符串
def geturl(url):
    # 请求详细页面
    r = requests.get(url, headers=headers)
    # 改编码
    r.encoding = "GB2312"
    soup = BeautifulSoup(r.text, "html.parser")
    # 找出类名为 info-zi mb15 下的所有p标签
    #ans = soup.find_all(["p", ".info-zi mb15"])
    ans = soup.find_all(["p", ".offcn_shocont"])
    # 用来储存最后需要写入文件的字符串
    mlist = ""
    for tag in ans:
        # 获取p标签下的string内容，并进行目标字符串拼接
        mlist = mlist + str(tag.string)
    # 返回目标字符串
    return mlist

# 获取目标网址第几页
def getalldoc(ii):
    #string_ans_li = []
    if ii == 1:
        testurl = "http://www.offcn.com/mianshi/mryl/"
    else:
    # 字符串拼接成目标网址
        testurl = "http://www.offcn.com/mianshi/mryl/" + str(ii) + ".html"
    # 使用request去get目标网址
    res = requests.get(testurl, headers=headers)
    # 更改网页编码--------不改会乱码
    res.encoding = "GB2312"
    # 创建一个BeautifulSoup对象
    soup = BeautifulSoup(res.text, "html.parser")
    # 找出目标网址中所有的small标签
    # 函数返回的是一个list
    ans = soup.find_all("a")
    # 用于标识问题
    cnt = 1
    # 先创建目录
    # 如果需要分页爬取，那么路径只要写到对应就好了
    #mkdir("result\\第" + str(ii) + "页\\")
    for tag in ans:
        # 获取a标签下的href网址
        #string_ans = str(tag.a.get("href"))
        string_ans = str(tag.get("href"))
        if string_ans.find("/mianshi/2020/") == -1 and string_ans.find("/mianshi/2019/") == -1 and string_ans.find("/mianshi/2020/") == -1:
            continue
        #string_ans_li.append(string_ans)
        # 请求详细页面
        # 返回我们需要的字符串数据
        string_write = geturl(string_ans)
        # 写文件到磁盘
        writedoc(string_write, cnt, ii)
        cnt = cnt + 1
    #print("第", ii, "页写入完成")
    #return string_ans_li

"""
def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False
"""

def getall():
    for i in range(1, 10, 1):
        getalldoc(i)
        #print(ss)
        print(str(i) + " end!")
        #break

def get_gov(testurl, file):
    res = requests.get(testurl, headers=headers)
    # 更改网页编码--------不改会乱码
    res.encoding = "utf-8"
    # 创建一个BeautifulSoup对象
    soup = BeautifulSoup(res.text, "html.parser")
    ans = soup.find_all([["p","h5"], "conlun2_box_text"])
    # 用来储存最后需要写入文件的字符串
    mlist = ""
    for tag in ans:
        # 获取p标签下的string内容，并进行目标字符串拼接
        s = str(tag.string)
        if s == 'None': continue
        mlist = mlist + s + "\n"
    # 返回目标字符串
    with open(file, "a+") as file:
        file.write(mlist)

if __name__ == "__main__":
    #getall()
    get_gov("http://www.gov.cn/guowuyuan/zfgzbg.htm","gov-2020.txt")
    get_gov("http://www.gov.cn/guowuyuan/2019zfgzbg.htm","gov-2019.txt")
