import requests
import http.cookiejar
import time
# pip3 install beautifulsoup4
# pip3 install html5lib
from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.parse



session = requests.session()
session.cookies = http.cookiejar.LWPCookieJar(filename="cookies.txt")

def get_headers():
    url = "http://elec.xmu.edu.cn/PdmlWebSetup/Pages/SMSMain.aspx"
    response = session.get(url)
    s_id = response.cookies["ASP.NET_SessionId"]
    cookies = {'ASP.NET_SessionId':s_id}
    header = {
        "HOST":"elec.xmu.edu.cn",
        "Origin":"http://elec.xmu.edu.cn",
        "Referer": "http://elec.xmu.edu.cn/PdmlWebSetup/Pages/SMSMain.aspx",
        "Upgrade-Insecure-Requests":"1",
        "Content-Type":"application/x-www-form-urlencoded",
        'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Cookie": "ASP.NET_SessionId=" + s_id
    }
    return cookies,header

# 获取header和cookie
cookies,headers = get_headers()


# 获取viewstate和eventargument
def get_hiddenvalue(drxiaoqu):
    url = "http://elec.xmu.edu.cn/PdmlWebSetup/Pages/SMSMain.aspx"

    # 设置截止时间，具体说明见下个函数
    date_now = time.strftime("%Y-%m-%d") + " 08:00:00"
    date_array = time.strptime(date_now, "%Y-%m-%d %H:%M:%S")
    date_end_stamp = int(time.mktime(date_array)) * 1000

    post_data = {
        "__EVENTTARGET": "drxiaoqu",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__VIEWSTATE":"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aWRWaWV3RGF0YVRleHRDb2x1bW4sIERldkV4cHJlc3MuV2ViLkFTUHhHcmlkVmlldy52MTEuMSwgVmVyc2lvbj0xMS4xLjcuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iODhkMTc1NGQ3MDBlNDlhZAISDzwrABYCAA8WAh8GaGQGDxYCHwdnDxQrAAYUKwALFgwfCAUM5oi/6Ze057yW5Y+3HwkFCFJvb21Db2RlHwpmHwsbAAAAAAAALkAHAAAAHwwFB1RleHRCb3gfDWc8KwAMAQAWAh8OCysEAjwrAAwBABYCHw4LKwQCZGRkZGRkZGQUKwALFgwfCAUG5pel5pyfHwkFCEVsZWNEYXRlHwoCAR8LGwAAAAAAAC5ABwAAAB8MBQdUZXh0Qm94Hw1nPCsADAEAFgIfDgsrBAI8KwAMAQAWAh8OCysEAmRkZGRkZGRkFCsACxYMHwgFDOaIv+mXtOWQjeensB8JBQhmYW5namlhbh8KAgEfCxsAAAAAAAA0QAcAAAAfDAUHVGV4dEJveB8NZzwrAAwBABYCHw4LKwQCPCsADAEAFgIfDgsrBAJkZGRkZGRkZBQrAAsWDB8IBQvnlKjph48o5YWDKR8JBQhVc2VkRWxlYx8KAgEfCxsAAAAAAAAuQAcAAAAfDAUHVGV4dEJveB8NZzwrAAwBABYCHw4LKwQCPCsADAEAFgIfDgsrBAJkZGRkZGRkZBQrAAsWDB8IBQ7nlKjnlLXph48o5bqmKR8JBQpBbGxVc2VFbGVjHwoCAR8LGwAAAAAAAC5ABwAAAB8MBQdUZXh0Qm94Hw1nPCsADAEAFgIfDgsrBAI8KwAMAQAWAh8OCysEAmRkZGRkZGRkFCsACxYMHwgFEeWJqeS9meeUtemHjyjluqYpHwkFBm15ZWxlYx8KAgIfCxsAAAAAAAA0QAcAAAAfDAUHVGV4dEJveB8NZzwrAAwBABYCHw4LKwQCPCsADAEAFgIfDgsrBAJkZGRkZGRkZA8UKwEGAgECAQIBAgECAQIBFgEFmQFEZXZFeHByZXNzLldlYi5BU1B4R3JpZFZpZXcuR3JpZFZpZXdEYXRhVGV4dENvbHVtbiwgRGV2RXhwcmVzcy5XZWIuQVNQeEdyaWRWaWV3LnYxMS4xLCBWZXJzaW9uPTExLjEuNy4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI4OGQxNzU0ZDcwMGU0OWFkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYHBQ9keGRhdGVTdGFydCREREQFFWR4ZGF0ZVN0YXJ0JERERCRDJEZOUAUNZHhkYXRlRW5kJERERAUTZHhkYXRlRW5kJERERCRDJEZOUAUKZHhidG5RdWVyeQULZHhndlN1YkluZm8FCGR4Z3ZFbGVjh0eWG9QfV05LaHf8j8zhXnguMsc=",
        "__EVENTVALIDATION":"/wEWJwLD84UkAsz5lloCzPmWWgLclvC3DALclvS3DALclsi3DALclsy3DALclsC3DALclsS3DALclti3DALClsS3DALclpy0DALclpC0DALClvC3DALClvS3DALClsi3DALClsy3DALClsC3DALClti3DALClpy0DALClpC0DALBlvy3DALBlvC3DALBlvS3DALBlsi3DALBlsy3DALBlsC3DALAlvS3DALAlvC3DALAlvy3DALDlvy3DALDlvC3DALDlvS3DALHlvy3DALHlvC3DAKDweWBBgLE4IbRAwKXqKQUApunmcIIFKxzVx4fqtQw/XsFLhp3AQj8H8s=",
        "drxiaoqu": drxiaoqu,
        "drlou":"",
        "txtRoomid":"",
        "dxdateStart_Raw": "1491004800000",
        "dxdateStart": "",
        "dxdateStart_DDDWS": "0:0:-1:-10000:-10000:0:-10000:-10000:1",
        "dxdateStart_DDD_C_FNPWS": "0:0:-1:-10000:-10000:0:0px:-10000:1",
        "dxdateStart$DDD$C": "",
        "dxdateEnd_Raw": date_end_stamp,
        "dxdateEnd": "",
        "dxdateEnd_DDDWS": "0:0:-1:-10000:-10000:0:-10000:-10000:1",
        "dxdateEnd_DDD_C_FNPWS": "0:0:-1:-10000:-10000:0:0px:-10000:1",
        "dxdateEnd$DDD$C": "",
        "dxgvSubInfo$DXSelInput": "",
        "dxgvSubInfo$CallbackState": "/wEWBB4ERGF0YQUsQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBSEFBY0EeBVN0YXRlBVRCd1VIQUFJQkJ3RUNBUWNCQWdFSEFRSUJCd0lDQVFjQUJ3QUhBQWNBQlFBQUFJQUpBZ0FKQWdBQ0FBTUhCQUlBQndBQ0FRY0FCd0FDQVFjQUJ3QT0=",
        "dxgvElec$CallbackState": "/wEWBB4ERGF0YQUsQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBSEFBY0EeBVN0YXRlBVhCd1lIQUFJQkJ3RUNBUWNCQWdFSEFRSUJCd0VDQVFjQ0FnRUhBQWNBQndBSEFBVUFBQUNBQ1FJQUNRSUFBZ0FEQndRQ0FBY0FBZ0VIQUFjQUFnRUhBQWNB",
        "DXScript": "1_42,1_74,2_22,2_29,1_46,1_54,2_21,1_67,1_64,2_16,2_15,1_52,1_65,3_7"
    }
    post_data = urllib.parse.urlencode(post_data)
    response = requests.post(url, data=post_data, headers=headers)

    # 采用正则表达式取出VIEWSTATE和EVENTVALIDATION
    VIEWSTATE =re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*?)" />', response.text)
    EVENTVALIDATION =re.findall(r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*?)" />', response.text)
    return VIEWSTATE[0],EVENTVALIDATION[0]



def get_info(drxiaoqu,drlou,txtRoomid):
    # 调用上面的函数取出drxiaoqu对应的的VIEWSTATE, EVENTVALIDATION
    drxiaoqu = drxiaoqu
    VIEWSTATE, EVENTVALIDATION= get_hiddenvalue(drxiaoqu)
    # 查询开始和截止时间是将时间转为时间戳再乘1000，dxdateEnd_Raw必填
    post_url = "http://elec.xmu.edu.cn/PdmlWebSetup/Pages/SMSMain.aspx"
    date_now = time.strftime("%Y-%m-%d") + " 08:00:00"
    date_array = time.strptime(date_now, "%Y-%m-%d %H:%M:%S")
    date_end_stamp = int(time.mktime(date_array)) * 1000

    post_data = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__VIEWSTATE":VIEWSTATE,
        "__EVENTVALIDATION":EVENTVALIDATION,
        "drxiaoqu":drxiaoqu,
        "drlou":drlou.encode("utf-8"),
        "txtRoomid":txtRoomid,
        "dxdateStart_Raw":"1491004800000",
        "dxdateStart":"",
        "dxdateStart_DDDWS":"0:0:-1:-10000:-10000:0:-10000:-10000:1",
        "dxdateStart_DDD_C_FNPWS":"0:0:-1:-10000:-10000:0:0px:-10000:1",
        "dxdateStart$DDD$C":"",
        "dxdateEnd_Raw":date_end_stamp,
        "dxdateEnd":"",
        "dxdateEnd_DDDWS":"0:0:-1:-10000:-10000:0:-10000:-10000:1",
        "dxdateEnd_DDD_C_FNPWS":"0:0:-1:-10000:-10000:0:0px:-10000:1",
        "dxdateEnd$DDD$C":"",
        "dxgvSubInfo$DXSelInput":"",
        "dxgvSubInfo$CallbackState":"/wEWBB4ERGF0YQUsQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBSEFBY0EeBVN0YXRlBVRCd1VIQUFJQkJ3RUNBUWNCQWdFSEFRSUJCd0lDQVFjQUJ3QUhBQWNBQlFBQUFJQUpBZ0FKQWdBQ0FBTUhCQUlBQndBQ0FRY0FCd0FDQVFjQUJ3QT0=",
        "dxgvElec$CallbackState":"/wEWBB4ERGF0YQUsQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBSEFBY0EeBVN0YXRlBVhCd1lIQUFJQkJ3RUNBUWNCQWdFSEFRSUJCd0VDQVFjQ0FnRUhBQWNBQndBSEFBVUFBQUNBQ1FJQUNRSUFBZ0FEQndRQ0FBY0FBZ0VIQUFjQUFnRUhBQWNB",
        "DXScript":"1_42,1_74,2_22,2_29,1_46,1_54,2_21,1_67,1_64,2_16,2_15,1_52,1_65,3_7"
    }

    #将post_data转换格式
    post_data = urllib.parse.urlencode(post_data)
    # 发送请求，得到response
    response = requests.post(post_url, data=post_data, headers=headers,cookies=cookies)
    return response.text




def query_info():
    for room in range(000, 511):
        room = room + 1
        roomid = "0"+str(room)
        buildName = "丰庭"
        buildCode = "10"
        build = buildName + buildCode
        resp = get_info("29", build, roomid)

        # 使用beautifulsoup实例化网页,resp是请求得到的HTML内容
        soup = BeautifulSoup(resp,'html5lib')
        # 根据id找余额那个标签
        try:
            money_info = soup.find_all(id='lableft')[0].string
        except:
            print(build + "-" + roomid + ":error")
            continue

        if money_info:
            #采用正则表达式，分别取出余额和剩余电量
            money_obj = re.findall(".\d.\d+",money_info)
            money_left = money_obj[0]
            enery_left = money_obj[1]
            print(build + "-房间号码：" + roomid + "，账户余额为"+ money_left +"元,剩余电量为"+ enery_left +"度" )


query_info()




