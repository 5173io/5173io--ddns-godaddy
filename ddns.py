# -*- coding: utf-8 -*-  
#python39
#导入需要的模块
import urllib.request
import json

domain = str('yourdomain.com') # 这里修改成你的域名
ip_file = str('ip.txt')
#ip_api = str('http://ip.42.pl/raw')
ip_api = str('http://ip.5173.io/text.php')
#定义请求地址
api_url = 'https://api.godaddy.com/v1/domains/' + domain + '/records'
api_key = 'xxxx'
api_secret = 'xxxx'

#直接做一个函数，传入API地址和更改的IP
def update_NS(api_url,ip_addr):
    #定义http请求头
    head = {}
    #定义服务器返回json数据给我们
    head['Accept'] = 'application/json'
    #定义我们发送的数据为json
    head['Content-Type'] = 'application/json'
    #定义身份认证信息
    head['Authorization'] = 'sso-key ' + api_key + ':' + api_secret

    #定义解析记录
    records_a = {
    "data" : ip_addr,
    "name" : "@",
    "ttl" : 600,
    "type" : 'A',
    }
    records_b = {
    "data" : domain,
    "name" : "www",
    "ttl" : 600,
    "type" : 'A',
    }
    #下面这两个必须包含，不可更改
    #ns47.domaincontrol.com
    records_NS01 = {
    "data" : "ns47.domaincontrol.com",
    "name" : "@",
    "ttl" : 3600,
    "type" : "NS",
    }

    #ns48.domaincontrol.com
    records_NS02 = {
    "data" : "ns48.domaincontrol.com",
    "name" : "@",
    "ttl" : 3600,
    "type" : "NS",
    }
    #定义需要发送给服务器的数据为put_data这个列表，包含上面的解析记录
    put_data = [records_a,records_b,records_NS01,records_NS02]

    rsp = ""
    #错误处理
    try:
        #定义请求，包含请求地址，请求头，请求方式，并把put_data从json转换为字符串格式，再转换成bytes
        req = urllib.request.Request(api_url,headers = head,data = json.dumps(put_data).encode(),method = "PUT")
        rsp = urllib.request.urlopen(req)
        #根据官方文档我们只需要知道服务器返回码即可，200为成功，这里获取服务器的返回码
        code = rsp.getcode()
        #判断是否成功
        if code == 200:
            print('成功更改域名解析：'+ip_addr)
            return True
        else:
            print('更改失败！')
    #原谅我偷懒。官方有400/401/422等错误，这里统一处理了
    except Exception as e:
        print('update错误2！')
        print(e)
    return False


def fetch_myip(ip_api):
    try:
        #定义请求，包含请求地址，请求头，请求方式，并把put_data从json转换为字符串格式，再转换成bytes
        req = urllib.request.Request(ip_api,method = "GET")
        rsp = urllib.request.urlopen(req)
        #根据官方文档我们只需要知道服务器返回码即可，200为成功，这里获取服务器的返回码
        code = rsp.getcode()
        ip = rsp.read().decode('utf-8')
        #判断是否成功
        if code == 200:
            print('成功获取IP：'+ip)
            return ip
        else:
            print('获取IP失败！')
            return ""
    #原谅我偷懒。官方有400/401/422等错误，这里统一处理了
    except:
        print('myip错误1！')
        return ""

def file_get_content(file):
    with open(file, 'r') as f:
        txt = f.read()
        print(txt)
        return txt
        
def file_put_content(file, txt):
    with open(file, 'w') as f:
        txt = f.write(txt)

ip_addr1 = file_get_content(ip_file).strip()
ip_addr2 = fetch_myip(ip_api).strip()
print(ip_addr2)
if ip_addr2 != "" and ip_addr1 != ip_addr2:
    #执行一下函数，并传入请求地址和我们输入的IP
    ret = update_NS(api_url,ip_addr2)
    if ret:
        file_put_content(ip_file, ip_addr2)
        print("成功写入IP: " + ip_addr2)
else:
    print("IP没有变化")
