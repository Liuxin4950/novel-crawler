import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
from bs4 import BeautifulSoup


def scrape_novel():
    # 获取用户输入的参数
    list_url = catalog_url_entry.get()
    baseurl = chapter_url_prefix_entry.get()
    novel_list_selector = novel_list_entry.get()
    novel_body_selector = novel_body_entry.get()
    novel_title = ''
    # 检查用户输入是否为空
    if not list_url.strip() or not baseurl.strip():
        messagebox.showerror("Error", "小说地址URL和目录URL不能为空！")
        return

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.222 Safari/537.36'
    }

    try:
        # 获取小说目录页面内容
        catalog_response = requests.get(url=baseurl + list_url, headers=headers)
        catalog_response.raise_for_status()  # 检查请求是否成功
        catalog_response.encoding = catalog_response.apparent_encoding
        catalog_soup = BeautifulSoup(catalog_response.text, "lxml")

        #解析小说标题
        for cover_div in catalog_soup.select('div.cover'):
            img_alt = cover_div.img.get('alt')
            novel_title = img_alt


        # 解析小说目录并逐一爬取章节内容
        chapters = catalog_soup.select(novel_list_selector)
        for chapter in chapters:
            if chapter.a['href'] != 'javascript:dd_show()':
                chapter_url = baseurl + chapter.a['href']
                chapter_response = requests.get(url=chapter_url, headers=headers)
                chapter_response.raise_for_status()  # 检查请求是否成功
                chapter_response.encoding = chapter_response.apparent_encoding
                chapter_soup = BeautifulSoup(chapter_response.text, 'lxml')
                chapter_content = chapter_soup.select_one(novel_body_selector).get_text()

                # 将章节内容写入文件
                with open('./'+novel_title+'.txt', 'a', encoding='utf-8') as fp:
                    fp.write(chapter.string + "\n" + chapter_content + '\n')

                # 在结果文本框中显示爬取成功信息
                result_text.config(state=tk.NORMAL)
                result_text.insert(tk.END, chapter.string + "获取成功!\n")
                root.update()  # 更新界面

        result_text.config(state=tk.DISABLED)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"请求错误: {e}")
        result_text.config(state=tk.NORMAL)
        result_text.insert(tk.END, f"请求错误: {e}\n")
        result_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"爬取小说失败: {e}")
        result_text.config(state=tk.NORMAL)
        result_text.insert(tk.END, f"爬取小说失败: {e}\n")
        result_text.config(state=tk.DISABLED)


def stop_scraping():
    # 在这里添加停止爬取的逻辑
    pass


# 创建页面ui
root = tk.Tk()
root.title("Novel Liuxin")

# 添加标签和输入框
chapter_url_prefix_label = tk.Label(root, text="小说网站地址:")
chapter_url_prefix_label.grid(row=0, column=0, sticky="e")
chapter_url_prefix_entry = tk.Entry(root, width=50)
chapter_url_prefix_entry.grid(row=0, column=1, padx=5, pady=5)
chapter_url_prefix_entry.insert(tk.END, "https://www.biqg.cc")

catalog_url_label = tk.Label(root, text="小说目录路径:")
catalog_url_label.grid(row=1, column=0, sticky="e")
catalog_url_entry = tk.Entry(root, width=50)
catalog_url_entry.grid(row=1, column=1, padx=5, pady=5)
catalog_url_entry.insert(tk.END, "/book/2061/")

novel_list_label = tk.Label(root, text="小说目录规则:")
novel_list_label.grid(row=2, column=0, sticky="e")
novel_list_entry = tk.Entry(root, width=50)
novel_list_entry.grid(row=2, column=1, padx=5, pady=5)
novel_list_entry.insert(tk.END, '.listmain > dl dd')

novel_body_label = tk.Label(root, text="小说内容规则:")
novel_body_label.grid(row=3, column=0, sticky="e")
novel_body_entry = tk.Entry(root, width=50)
novel_body_entry.grid(row=3, column=1, padx=5, pady=5)
novel_body_entry.insert(tk.END, '#chaptercontent')

scrape_button = tk.Button(root, text="运行程序", command=scrape_novel)
scrape_button.grid(row=4, column=0, padx=5, pady=10)

stop_button = tk.Button(root, text="结束爬取", command=stop_scraping)
stop_button.grid(row=4, column=1, padx=5, pady=10)

result_text = scrolledtext.ScrolledText(root, width=60, height=10)
result_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
result_text.config(state=tk.DISABLED)

root.mainloop()
