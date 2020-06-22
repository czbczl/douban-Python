# -*- codeing =utf-8 -*-
#@Time: 2020/6/20 8:33
#@Author :cz
#@File : testCloud.py
#@Software: PyCharm

import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import sqlite3

# 准备词云所需的文字（词）
con = sqlite3.connect('movie.db')
cur = con.cursor()
sql = 'select instroduction from movie250'
data = cur.execute(sql)
text = ""
for item in data:
    text = text +item[0]
# print(text)
cur.close()
con.close()

#分词
cut = jieba.cut(text)
string = ' '.join(cut)
# print(len(string))

img = Image.open(r'.\static\assets\img\tree.jpg') #打开遮罩图片
img_array = np.array(img) #将图片转换为数组
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path="msyh.ttc"
)
wc.generate_from_text(string)


#绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')

#plt.show()  #显示生成的词云图片

#输出词云图片到文件
plt.savefig(r'.\static\assets\img\word.jpg',dpi=500)
