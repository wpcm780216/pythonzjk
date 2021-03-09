
import urllib.request
import base64
import socket
import urllib.parse,json,requests,time,threading,socketserver
from http.server import HTTPServer, BaseHTTPRequestHandler




data = {'result': 'this is a test'}
host = ('10.0.0.8', 888)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

## v2ray订阅地址
subscribe_url = ''
hostname = ''
servername = ''
vmesscode = ''
class MyThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    pass
class Resquest(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        vmess(self)
        self.wfile.write(vmesscode)  # 返回内容



def vmess(self):
        global vmesscode
        subscribe_url = self.path.split("&&")[1]
        hostname = self.path.split("&&")[2]
        servername = urllib.parse.unquote(self.path.split("&&")[3])
        print("subscribe_url:",subscribe_url)
        print("hostname:",hostname)
        print("servername:", servername)

        socket.setdefaulttimeout(5)  #请求超时设置为5s
        req = urllib.request.Request(url=subscribe_url, headers=headers)

        return_content = urllib.request.urlopen(req).read()
        print("请求到的内容为：", return_content)
        base64Str = base64.urlsafe_b64decode(return_content)  # 进行base64解码
        print("解码后内容：", base64Str)
        print("开始处理...\r")
        share_links = base64Str.splitlines()  # \r\n进行分行
        add = ""

        for share_link in share_links:
            dict = {}
            share_link = bytes.decode(share_link)  # 转换类型
            if share_link.find("vmess://") == -1:
                # print("")
               # vmesscode = "抱歉，您的订阅链接不是vmess链接。"
                pass
            else:
                # print("服务器参数：", share_link)
                shar = share_link.split("ss://")
                jj = base64.urlsafe_b64decode(shar[1]).decode('UTF-8')  # 解析VMESS参数得到josn字符串 后面解析unicode
                # jj = base64.urlsafe_b64decode(shar[1]) # 解析VMESS参数得到josn字符串 后面解析unicode
                print("vmess参数解析得到josn内容：",jj)

                par = json.loads(jj)  # 转换成字典
                if (self.path.count("&&") == 4):
                    for index in range(len(self.path.split("&&")[4].split('.'))):
                        if(str(par["port"] )== str(self.path.split("&&")[4].split('.')[index])):
                           
                            add = add + vm(par,self)
                elif (self.path.count("&&") == 4 and str(par["port"]) == str(self.path.split("&&")[4])):
                    add = add + vm(par,self)
                elif self.path.count("&&") == 3 :
                    add = add + vm(par,self)
                else:
                    pass


            #   if (self.path.count("&&") == 4 and str(par["port"] )== str(self.path.split("&&")[4].split('.')[0]) ):
            #       add = add + vm(par)
            #   elif self.path.count("&&") == 3 :
            #       add = add + vm(par)
            #   else:
            #       pass
                # 添加混淆完成
                # print("转换后所有vmess参数\r",add)
        dic3 = base64.b64encode(add.encode('UTF-8'))
        vmesscode = dic3
        print("订阅内容：")
        print(dic3)



def vm(par,self):
    hostname = self.path.split("&&")[2]
    servername = urllib.parse.unquote(self.path.split("&&")[3])
    #print("转换为字典后内容:", par)
    par["ps"] = servername + par["ps"]
    par["host"] = hostname
    # par["path"] = pathname
    dic = json.dumps(par)  # 转换成json
    print("添加混淆参数后json内容：", dic)

    # dic1 = base64.b64encode(dic)  # 转换成base64字符串
    dic1 = base64.b64encode(dic.encode('UTF-8'))  # 转换成base64字符串
    dic2 = 'vmess://' + bytes.decode(dic1) + "\r\n"  # 拼接vmess头
    return dic2




if __name__ == '__main__':
    server = MyThreadingHTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
