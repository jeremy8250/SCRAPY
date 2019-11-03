from bs4 import BeautifulSoup
import requests, sys

class downloader(object):

    """
    初始化参数
    """
    def __init__(self):
        self.server = 'http://www.biqukan.com'                  #域名
        self.target = 'http://www.biqukan.com/1_1094/'          #需要爬取的目标起始地址
        self.names = []                                         #用来存放章节名
        self.urls = []                                          #用来存放章节链接
        self.nums = 0                                           #用来存放章节数数量

    """
    【爬取章节名+链接】
    这个方法首选获取当前页面的所有章节内容，
    然后爬取章节名(str)和对应的链接(href)，
    最后将章节名放在names[]列表中，
    章节链接以域名(server)+爬取到的地址(href)拼接起来，
    放到urls[]列表中。
    """
    def get_download_url(self):
        req = requests.get(url = self.target)                   #发出GET请求，获取页面信息
        req.encoding = 'gbk'                                    #网页编码为gbk，需要转化，否则会乱码
        html = req.text                                         #获取页面的返回内容
        div_bf = BeautifulSoup(html, 'lxml')                    #实例化一个BeautifulSoup，并使用lxml解析器解析
        div = div_bf.find_all('div', class_ = 'listmain')       #获取所有tag=div，class=listmain的内容
        a_bf = BeautifulSoup(str(div[0]), 'lxml')               #返回的div类型为ResultSet，数据存储在第一个索引位置，因此用div[0]，获取后需要将内容转成str，再实例化，通过lxml解析
        a = a_bf.find_all('a')                                  #获取div标签下所有a的标签
        self.nums = len(a[16:])                                 #剔除前面的16章无关内容，计算从第17章开始到最后，共有多少章节
        for each in a[16:]:                                     #遍历所有章节
            self.names.append(each.string)                      #提取标签的文本内容，放入章节名(names)列表
            self.urls.append(self.server + each.get('href'))    #提取标签的href属性，与域名拼接后形成新的地址，放入章节链接(urls)列表

    """
    【爬取正文内容】
    这个方法首先获取当前页面的所有内容，
    然后查找div标签下class=showtxt的标签，
    再剔除文本中多余的空格和换行符后输出。
    """
    def get_contents(self,target):
        req = requests.get(url=target)                          #发出GET请求，获取页面信息
        req.encoding = 'gbk'                                    #网页编码为gbk，需要转化，否则会乱码
        html = req.text                                         #获取页面的返回内容
        bf = BeautifulSoup(html, 'lxml')                        #实例化一个BeautifulSoup，并使用lxml解析器解析
        texts = bf.find_all('div', class_='showtxt')            #获取div标签下class=showtxt的内容
        texts = texts[0].text.replace('\xa0'*7, '\n\n')         #返回的texts类型为ResultSet,数据存储在第一个索引位置，因此用texts[0]，.text为获取文本内容，再将页面上的空格替换为回车
        return texts                                            #输出清洗后的数据

    """
    【将爬取的内容写入文件】
    这个方法
    """
    def writer(self, name, path, text):
        write_flag = True                                       #写标签设置为true
        with open(path, 'a', encoding='utf-8') as f:            #在<path>路径下，以追加的方式('a')创建一个文件编码为utf-8的文件
            f.write(name + '\n')                                #写入章节名
            f.writelines(text)                                  #写入正文内容
            f.write('\n\n')                                     #换行结束

"""
【主函数】
"""
if __name__ == "__main__":
    dl = downloader()                                                           #实例化类对象(downloader)
    dl.get_download_url()                                                       #调用爬取章节名方法
    print('《一念永恒》开始下载：')                                                 #打印提示信息
    for i in range(dl.nums):                                                    #遍历章节数
        dl.writer(dl.names[i], '一念永恒.txt', dl.get_contents(dl.urls[i]))      #调用writer方法，将章节名、文件保存路径、正文内容写入项目目录下的一念永恒.txt文件
        sys.stdout.write("已下载: %.3f%%" % float(i/dl.nums) + '\r')             #调用标准输出，在控制台打印下载进度（进度=当前遍历的章节数/总章节数）
        sys.stdout.flush()                                                      #刷新内存
    print('《一念永恒》下载完毕！')                                                 #打印提示信息