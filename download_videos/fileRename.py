import os
import sys
import time


class file_rename(object):

    def __init__(self):
        self.ts = []
        self.mp4 = []
        self.path = os.getcwd() + '/av/'
        self.count = 0

    def fileRe(self):
        # with open('index.m3u8','r') as g:
        #     for line in g.readlines():
        #         if ".ts" in line:
        #             #去掉每个ts文件名后面的回车符号
        #             ts_line = line.replace('\n','') + '.mp4'
        #             #将ts文件写入self.ts列表
        #             self.ts.append(ts_line)
        #     # print(self.ts)


        # self.mp4 = os.listdir(self.path)
        # # print(self.mp4)

        # self.count = len(self.ts)
        # # print(self.count)

        os.chdir(self.path)
        # for i in range(len(self.ts)):
        #     ts_name = self.ts[i]
        #     for j in range(len(self.mp4)):
        #         mp4_name = self.mp4[j]
        #         currenttime1 = int(time.time())
        #         if ts_name == mp4_name:
        #             new_name = currenttime1
        #             os.rename(mp4_name, str(new_name) + '.ts.mp4')
        #             time.sleep(1)
                    
            # sys.stdout.write("已完成: %.3f%%" % float(i/len(self.ts)) + '\r')
        # print('mission complete!')


        cmd_merge = "cat *.mp4 > av.mp4"
        os.system(cmd_merge)

        print('merge complete!')

if __name__ == "__main__":
    fr = file_rename()
    fr.fileRe()