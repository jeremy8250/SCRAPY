from bs4 import BeautifulSoup
import requests
import json
import time
import sys
from contextlib import closing
i
class get_pictures(object):

    def __init__(self):
        #初始化空的图片ID列表
        self.ids = []
        #图片下载的url,XXX就是具体的图片ID
        self.download_url = "https://unsplash.com/photos/XXX/download?force=true"
        #图片列表，控制每页显示多少张图片
        self.id_url = "https://unsplash.com/napi/photos?page=1&per_page=YYY"

    """
    这个方法主要获取每张图片的ID，再把这些ID拼接到下载地址中返回，
    首先定义好需要下载多少张图片，perPage参数代表每页先死多少张，
    从返回的list中获取ID字段，再写入self.ids列表，
    遍历所有的id，把他们拼接到图片下载的url中，
    最后返回所有图片的下载地址
    """
    def get_img_url(self,perPage):
        #将带有图片id的url赋值给target
        target = self.id_url
        #图片张数替换YYY
        target = target.replace('YYY', perPage)
        #GET方法调用url,获取返回信息
        req = requests.get(url = target)
        #将返回的信息转换成json
        html = json.loads(req.text)
        for pics in html:
            #遍历所有的返回内容，获取key = id的值
            pic_id = pics['id']
            #将所有id值写入ids列表
            self.ids.append(pic_id)
        for id in self.ids:
            #遍历ids里面所有的id，再替换download_url中的XXX
            download_urls = self.download_url.replace("XXX", id)
        #返回每张图片的下载地址
        return download_urls

    """
    这个方法主要是用来下载图片，
    with closing表示下载完了需要关闭连接，不能一直开着，避免资源浪费，
    stream = true表示在下载的过程中需要链接一直保持，避免中断，
    chunk用于分段处理大文件
    """
    def writter(self,filename,perPage):
        #将图片下载地址赋值给变量download_urls
        download_urls = get_pictures.get_img_url(self,perPage)
        #调用GET方法，打开下载链接
        with closing(requests.get(url=download_urls, stream=True)) as r:
            #将下载的文件以二进制的形式保存为jpg文件
            with open('%d.jpg' % filename, 'ab+') as f:
                #文件太大，需要切合下载
                for chunk in r.iter_content():
                    if chunk:
                        f.write(chunk)
                        f.flush()

if __name__ == "__main__":
    #类实例化
    gp = get_pictures()
    print('图片获取中...')
    #调用获取图片下载链接方法，参数'2'表示需要下载2张图片
    gp.get_img_url('2')
    print('图片下载中...')
    #获取图片id的总数，遍历下载
    for i in range(len(gp.ids)):
        print('正在下载第%d张图片' % (i+1))
        gp.writter(i+1,'2')
    #下载完成后通知一下
    print('图片下载完成！')