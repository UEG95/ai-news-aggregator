import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
from bs4 import BeautifulSoup
import webbrowser
import logging
import json
import time
from datetime import datetime
import threading
from ttkthemes import ThemedTk
import os
from PIL import Image, ImageTk

# 图标数据 - 简约设计的新闻聚合器图标
ICON_DATA = '''
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
'''

class NewsAggregator:
    def __init__(self, root):
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='news_aggregator.log'
        )
        self.logger = logging.getLogger('NewsAggregator')
        
        self.root = root
        self.root.title("AI新闻聚合器 - UEG95")
        
        # 设置窗口图标
        try:
            if os.path.exists("icon.png"):
                icon_image = Image.open("icon.png")
                icon_photo = ImageTk.PhotoImage(icon_image)
                self.root.iconphoto(True, icon_photo)
        except Exception as e:
            self.logger.warning(f"加载图标失败: {str(e)}")
        
        # 使用主题
        self.root.set_theme("arc")
        
        # 设置窗口大小和位置
        window_width = 1200
        window_height = 800
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 初始化代理设置
        self.proxy = None
        
        # 新闻源配置
        self.news_sources = {
            "新浪科技": self.get_sina_tech_news,
            "36氪": self.get_36kr_news
        }
        
        # 创建主框架
        self.create_main_frame()
        
        # 存储新闻链接
        self.news_links = []
        
        # 获取新闻
        self.get_news()
    
    def create_main_frame(self):
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建顶部控制区域
        control_frame = ttk.Frame(self.main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 左侧控制区
        left_control = ttk.Frame(control_frame)
        left_control.pack(side=tk.LEFT)
        
        # 新闻源选择
        ttk.Label(left_control, text="新闻源:").pack(side=tk.LEFT, padx=5)
        self.source_var = tk.StringVar(value="新浪科技")
        source_menu = ttk.OptionMenu(left_control, self.source_var, "新浪科技", *self.news_sources.keys())
        source_menu.pack(side=tk.LEFT, padx=5)
        
        # 代理设置按钮
        self.proxy_button = ttk.Button(left_control, text="设置代理", command=self.show_proxy_settings)
        self.proxy_button.pack(side=tk.LEFT, padx=5)
        
        # 刷新按钮
        self.refresh_button = ttk.Button(left_control, text="刷新新闻", command=self.get_news)
        self.refresh_button.pack(side=tk.LEFT, padx=5)
        
        # 右侧控制区
        right_control = ttk.Frame(control_frame)
        right_control.pack(side=tk.RIGHT)
        
        # 搜索框
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_news)
        ttk.Label(right_control, text="搜索:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(right_control, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        # 创建新闻显示区域
        self.news_area = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, height=30, font=("微软雅黑", 10))
        self.news_area.pack(fill=tk.BOTH, expand=True, pady=5)
        self.news_area.tag_configure("title", font=("微软雅黑", 12, "bold"))
        self.news_area.tag_configure("link", foreground="blue", underline=1)
        self.news_area.tag_configure("source", font=("微软雅黑", 9))
        self.news_area.tag_configure("time", font=("微软雅黑", 9))
        
        # 绑定点击事件
        self.news_area.tag_bind("link", "<Button-1>", self.open_link)
        self.news_area.tag_bind("link", "<Enter>", lambda e: self.news_area.config(cursor="hand2"))
        self.news_area.tag_bind("link", "<Leave>", lambda e: self.news_area.config(cursor=""))
        
        # 状态栏
        status_frame = ttk.Frame(self.main_frame)
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_bar.pack(side=tk.LEFT)
        
        # 版权信息
        ttk.Label(status_frame, text="© 2024 UEG95，保留所有权利").pack(side=tk.RIGHT)
    
    def filter_news(self, *args):
        search_text = self.search_var.get().lower()
        self.news_area.delete(1.0, tk.END)
        
        for title, link, source, time_str in self.news_links:
            if search_text in title.lower() or search_text in source.lower():
                self.display_news_item(title, link, source, time_str)
    
    def display_news_item(self, title, link, source="", time_str=""):
        # 插入标题
        self.news_area.insert(tk.END, f"{title}\n", "title")
        
        # 插入来源和时间
        if source or time_str:
            source_text = f"来源: {source}" if source else ""
            time_text = f" | 时间: {time_str}" if time_str else ""
            self.news_area.insert(tk.END, f"{source_text}{time_text}\n", "source")
        
        # 插入链接
        self.news_area.insert(tk.END, f"{link}\n", "link")
        self.news_area.insert(tk.END, "-" * 80 + "\n\n")
    
    def open_link(self, event):
        # 获取点击位置的索引
        index = self.news_area.index(f"@{event.x},{event.y}")
        # 获取该行的文本
        line = self.news_area.get(f"{index} linestart", f"{index} lineend")
        # 如果是链接（以http开头），则打开
        if line.startswith("http"):
            webbrowser.open(line)
    
    def show_proxy_settings(self):
        proxy_window = tk.Toplevel(self.root)
        proxy_window.title("代理设置")
        proxy_window.geometry("400x200")
        proxy_window.transient(self.root)  # 设置为主窗口的子窗口
        
        # 使用ttk风格
        main_frame = ttk.Frame(proxy_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="代理地址:").pack(pady=5)
        proxy_entry = ttk.Entry(main_frame, width=40)
        proxy_entry.pack(pady=5)
        if self.proxy:
            proxy_entry.insert(0, self.proxy)
        
        ttk.Label(main_frame, text="格式: http://host:port 或 socks5://host:port").pack(pady=5)
        
        def save_proxy():
            proxy = proxy_entry.get().strip()
            if proxy:
                self.proxy = proxy
                self.logger.info(f"设置代理: {proxy}")
                messagebox.showinfo("成功", "代理设置已保存")
            else:
                self.proxy = None
                self.logger.info("清除代理设置")
                messagebox.showinfo("成功", "代理设置已清除")
            proxy_window.destroy()
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="保存", command=save_proxy).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="取消", command=proxy_window.destroy).pack(side=tk.LEFT, padx=10)
    
    def get_news(self):
        self.status_var.set("正在获取新闻...")
        self.refresh_button.state(['disabled'])
        self.news_area.delete(1.0, tk.END)
        self.news_links.clear()
        
        def fetch_news():
            try:
                source_name = self.source_var.get()
                source_func = self.news_sources.get(source_name)
                if source_func:
                    source_func()
                else:
                    self.root.after(0, lambda: self.status_var.set("未知的新闻源"))
            except Exception as e:
                error_msg = str(e)
                self.logger.error(f"获取新闻失败: {error_msg}")
                self.root.after(0, lambda: self.status_var.set(f"获取新闻失败: {error_msg}"))
            finally:
                self.root.after(0, lambda: self.refresh_button.state(['!disabled']))
        
        threading.Thread(target=fetch_news, daemon=True).start()
    
    def get_sina_tech_news(self):
        try:
            url = "https://tech.sina.com.cn/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
            }
            proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else None
            
            self.logger.info(f"正在获取新浪科技新闻，URL: {url}")
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            response.encoding = 'utf-8'
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找所有新闻链接，特别是AI相关的
            news_items = []
            for link in soup.find_all("a", href=True):
                text = link.text.strip()
                href = link["href"]
                if ("AI" in text.upper() or "智能" in text or "机器人" in text) and href.startswith("http"):
                    news_items.append((text, href, "新浪科技", time.strftime("%Y-%m-%d")))
            
            self.logger.info(f"找到 {len(news_items)} 条新浪科技新闻")
            
            if not news_items:
                raise Exception("未找到新闻")
            
            # 更新新闻列表
            self.news_links = news_items
            
            # 显示新闻
            for title, link, source, time_str in news_items:
                try:
                    if title and link and len(title) > 5:  # 确保标题有意义
                        self.root.after(0, lambda t=title, l=link, s=source, ts=time_str: 
                                      self.display_news_item(t, l, s, ts))
                except Exception as e:
                    self.logger.warning(f"处理新闻项时出错: {str(e)}")
                    continue
            
            self.root.after(0, lambda: self.status_var.set(f"成功获取 {len(news_items)} 条新闻"))
            
        except Exception as e:
            self.logger.error(f"获取新浪科技新闻失败: {str(e)}")
            raise Exception(f"获取新浪科技新闻失败: {str(e)}")
    
    def get_36kr_news(self):
        try:
            url = "https://36kr.com/feed"  # 使用RSS源
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/rss+xml,application/xml;q=0.9",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
            }
            proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else None
            
            self.logger.info(f"正在获取36氪新闻，URL: {url}")
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'xml')  # 使用xml解析器
            
            # 查找所有新闻条目
            news_items = []
            for item in soup.find_all('item'):
                title = item.title.text.strip() if item.title else ""
                link = item.link.text.strip() if item.link else ""
                pub_date = item.pubDate.text.strip() if item.pubDate else ""
                
                # 转换发布时间格式
                try:
                    if pub_date:
                        dt = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
                        pub_date = dt.strftime("%Y-%m-%d")
                except Exception:
                    pub_date = time.strftime("%Y-%m-%d")
                
                # 只添加包含AI相关关键词的新闻
                if any(keyword in title for keyword in ["AI", "人工智能", "机器学习", "深度学习", "智能"]):
                    news_items.append((title, link, "36氪", pub_date))
            
            self.logger.info(f"找到 {len(news_items)} 条36氪新闻")
            
            if not news_items:
                raise Exception("未找到新闻")
            
            # 更新新闻列表
            self.news_links = news_items
            
            # 显示新闻
            for title, link, source, time_str in news_items:
                try:
                    self.root.after(0, lambda t=title, l=link, s=source, ts=time_str: 
                                  self.display_news_item(t, l, s, ts))
                except Exception as e:
                    self.logger.warning(f"处理新闻项时出错: {str(e)}")
                    continue
            
            self.root.after(0, lambda: self.status_var.set(f"成功获取 {len(news_items)} 条新闻"))
            
        except Exception as e:
            self.logger.error(f"获取36氪新闻失败: {str(e)}")
            raise Exception(f"获取36氪新闻失败: {str(e)}")

if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # 使用主题化的Tk
    app = NewsAggregator(root)
    root.mainloop() 