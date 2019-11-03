import sys, os
import requests,json
from bs4 import BeautifulSoup
from contextlib import closing

class signleDownloader(object):

    def __init__(self):
        self.list_url = "http://unsplash.com/napi/collections/1065976/photos?page=1&per_page=20&order_by=latest"
        self.download_url = "http://unsplash.com/photos/photo_id/download?force=true"
        self.ids = []

    
    def get_img(self):
        req = requests.get(url=self.list_url)
        list_api = json.loads(req.text)
        for pics in list_api:
            pic_id = pics['id']
            self.ids.append(pic_id)
        for id in self.ids:
            download_url = self.download_url.replace("photo_id", id)
        
        return download_url

    def downloader(self):
        with closing (requests.get(url=signleDownloader.get_img(self), stream=True)) as r:
            for i in range(len(self.ids)):
                fname = 'pic_' + str(i)
                with open('%s.jpg' % fname, 'ab+') as f:
                    for chunk in r.iter_content():
                        if chunk:
                            f.write(chunk)
                            f.flush()
                    sys.stdout.write("已完成: %.3f%%" % float(i/len(self.ids)) + '\r')

        print('下载完成！')




if __name__ == "__main__":
    sd = signleDownloader()
    sd.downloader()