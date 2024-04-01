# novel-crawler
闲暇无聊写的用python写的小说爬虫程序，现在只有爬取文本，存储的功能
import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
from bs4 import BeautifulSoup
这是依赖的包

使用requests来请求网页数据

使用。select来获取列表的所有元素

遍历所有的li，因为li下有a标签href是详细也的地址

进入详情页面获取包裹小说正文内容的html标签

存储进文件

目前，爬个300张就被中断连接了，分页也不会，就这样了
