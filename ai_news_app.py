import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
from bs4 import BeautifulSoup
import webbrowser
import json
import os
from datetime import datetime
import re
from urllib.parse import quote
import logging
import ttkthemes
from concurrent.futures import ThreadPoolExecutor, as_completed

class AINewsApp:
    def __init__(self, root):
        # 配置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('AINewsApp')
        
        self.root = root
        self.root.title("AI新闻聚合器")
        
        # 初始化代理设置
        self.proxy_var = tk.StringVar(value="")
        
        # 使用主题
        self.style = ttkthemes.ThemedStyle(self.root)
        self.style.set_theme("arc")  # 使用arc主题
        
        # 设置窗口大小和位置
        window_width = 1000
        window_height = 700
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 创建主框架
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 创建顶部框架
        top_frame = ttk.Frame(self.main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 创建标题
        title_label = ttk.Label(top_frame, text="AI新闻聚合器", font=("微软雅黑", 20))
        title_label.pack(side=tk.LEFT, pady=10)
        
        # 创建设置按钮
        settings_btn = ttk.Button(top_frame, text="设置", command=self.show_settings)
        settings_btn.pack(side=tk.RIGHT, pady=10)
        
        # 创建新闻源选择框架
        source_frame = ttk.LabelFrame(self.main_frame, text="新闻源", padding=10)
        source_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 创建新闻源选择按钮
        self.source_var = tk.StringVar(value="all")
        sources = [
            ("全部", "all"),
            ("必应", "bing"),
            ("谷歌", "google"),
            ("新浪科技", "sina"),
            ("36氪", "36kr"),
            ("量子位", "qbit")
        ]
        
        # 使用网格布局排列新闻源按钮
        for i, (text, value) in enumerate(sources):
            ttk.Radiobutton(source_frame, text=text, value=value, 
                          variable=self.source_var).grid(row=0, column=i, padx=10)
        
        # 创建工具栏
        toolbar = ttk.Frame(self.main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # 创建刷新按钮
        refresh_btn = ttk.Button(toolbar, text="刷新", command=self.fetch_news, style="Accent.TButton")
        refresh_btn.pack(side=tk.LEFT)
        
        # 创建加载指示器
        self.loading_label = ttk.Label(toolbar, text="")
        self.loading_label.pack(side=tk.LEFT, padx=10)
        
        # 创建新闻显示区域
        self.news_frame = ttk.Frame(self.main_frame)
        self.news_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建新闻列表
        self.news_canvas = tk.Canvas(self.news_frame)
        scrollbar = ttk.Scrollbar(self.news_frame, orient=tk.VERTICAL, command=self.news_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.news_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.news_canvas.configure(scrollregion=self.news_canvas.bbox("all"))
        )
        
        self.news_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.news_canvas.configure(yscrollcommand=scrollbar.set)
        
        # 布局新闻区域
        self.news_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 初始化新闻数据
        self.news_data = []
        
        # 创建状态栏
        self.status_bar = ttk.Label(self.main_frame, text="就绪", anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(5, 0))
        
        # 首次加载新闻
        self.fetch_news()
        
    def show_settings(self):
        """显示设置对话框"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("400x300")
        
        # 代理设置
        proxy_frame = ttk.LabelFrame(settings_window, text="代理设置", padding=10)
        proxy_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(proxy_frame, text="HTTP代理:").grid(row=0, column=0, padx=5, pady=5)
        proxy_entry = ttk.Entry(proxy_frame, textvariable=self.proxy_var, width=30)
        proxy_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(proxy_frame, text="格式: http://ip:port").grid(row=1, column=0, columnspan=2, pady=5)
        
    def create_news_card(self, news):
        """创建新闻卡片"""
        card = ttk.Frame(self.scrollable_frame, style="Card.TFrame")
        card.pack(fill=tk.X, padx=10, pady=5)
        
        # 新闻标题
        title = ttk.Label(card, text=news["title"], font=("微软雅黑", 12, "bold"), wraplength=900)
        title.pack(anchor=tk.W, pady=(5, 0))
        
        # 新闻摘要
        if news.get("snippet"):
            snippet = ttk.Label(card, text=news["snippet"], wraplength=900)
            snippet.pack(anchor=tk.W, pady=(5, 0))
        
        # 来源和时间
        info_frame = ttk.Frame(card)
        info_frame.pack(fill=tk.X, pady=5)
        
        source_label = ttk.Label(info_frame, text=f"来源: {news['source']}")
        source_label.pack(side=tk.LEFT, padx=(0, 10))
        
        time_label = ttk.Label(info_frame, text=f"时间: {news['time']}")
        time_label.pack(side=tk.LEFT)
        
        # 链接按钮
        link_btn = ttk.Button(card, text="阅读全文", 
                            command=lambda url=news["link"]: webbrowser.open(url))
        link_btn.pack(anchor=tk.E, pady=(0, 5))
        
    def fetch_bing_news(self):
        """获取Bing新闻"""
        try:
            self.logger.info("开始获取Bing新闻...")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
            }
            
            url = "https://www.bing.com/news/search?q=人工智能+AI&setlang=zh-CN"
            response = requests.get(url, headers=headers)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            news_cards = soup.find_all('div', class_='news-card newsitem cardcommon')
            
            results = []
            for card in news_cards[:10]:
                try:
                    title_elem = card.find('a', class_='title')
                    if not title_elem:
                        continue
                        
                    title = title_elem.get_text(strip=True)
                    link = title_elem['href']
                    source = card.find('div', class_='source').get_text(strip=True) if card.find('div', class_='source') else "未知来源"
                    time = card.find('span', class_='time').get_text(strip=True) if card.find('span', class_='time') else ""
                    snippet = card.find('div', class_='snippet').get_text(strip=True) if card.find('div', class_='snippet') else ""
                    
                    results.append({
                        "title": title,
                        "link": link,
                        "time": time,
                        "source": source,
                        "snippet": snippet
                    })
                except Exception as e:
                    self.logger.error(f"解析新闻卡片时出错: {str(e)}")
                    continue
                    
            return results
        except Exception as e:
            self.logger.error(f"获取Bing新闻失败: {str(e)}")
            return []
            
    def fetch_google_news(self):
        """获取Google新闻"""
        try:
            self.logger.info("开始获取Google新闻...")
            if not self.proxy_var.get():
                self.logger.warning("未设置代理地址")
                return []
                
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
            }
            
            proxies = {
                "http": self.proxy_var.get(),
                "https": self.proxy_var.get()
            }
            
            url = "https://news.google.com/search?q=AI+人工智能&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('article')
            
            results = []
            for article in articles[:10]:
                try:
                    title_elem = article.find('h3')
                    if not title_elem:
                        continue
                        
                    title = title_elem.get_text(strip=True)
                    link = "https://news.google.com" + title_elem.find('a')['href'][1:]
                    time_elem = article.find('time')
                    time = time_elem['datetime'] if time_elem else ""
                    source = article.find('a', {'data-n-tid': '9'}).text if article.find('a', {'data-n-tid': '9'}) else "未知来源"
                    
                    results.append({
                        "title": title,
                        "link": link,
                        "time": time,
                        "source": source,
                        "snippet": ""
                    })
                except Exception as e:
                    self.logger.error(f"解析文章时出错: {str(e)}")
                    continue
            
            return results
        except Exception as e:
            self.logger.error(f"获取Google新闻失败: {str(e)}")
            return []
            
    def fetch_sina_news(self):
        """获取新浪科技AI新闻"""
        try:
            self.logger.info("开始获取新浪科技新闻...")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            url = "https://tech.sina.com.cn/keywords/a/ai.html"
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = soup.find_all('div', class_='news-item')
            
            results = []
            for item in news_items[:10]:
                try:
                    title_elem = item.find('h2').find('a')
                    title = title_elem.text.strip()
                    link = title_elem['href']
                    time = item.find('div', class_='time').text.strip()
                    snippet = item.find('p', class_='summary').text.strip()
                    
                    results.append({
                        "title": title,
                        "link": link,
                        "time": time,
                        "source": "新浪科技",
                        "snippet": snippet
                    })
                except Exception as e:
                    self.logger.error(f"解析新浪新闻项时出错: {str(e)}")
                    continue
                    
            return results
        except Exception as e:
            self.logger.error(f"获取新浪科技新闻失败: {str(e)}")
            return []
            
    def fetch_36kr_news(self):
        """获取36氪AI新闻"""
        try:
            self.logger.info("开始获取36氪新闻...")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            url = "https://36kr.com/search/articles/ai"
            response = requests.get(url, headers=headers)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = soup.find_all('div', class_='article-item')
            
            results = []
            for item in news_items[:10]:
                try:
                    title_elem = item.find('a', class_='article-title')
                    title = title_elem.text.strip()
                    link = "https://36kr.com" + title_elem['href']
                    time = item.find('span', class_='time').text.strip()
                    snippet = item.find('p', class_='summary').text.strip()
                    
                    results.append({
                        "title": title,
                        "link": link,
                        "time": time,
                        "source": "36氪",
                        "snippet": snippet
                    })
                except Exception as e:
                    self.logger.error(f"解析36氪新闻项时出错: {str(e)}")
                    continue
                    
            return results
        except Exception as e:
            self.logger.error(f"获取36氪新闻失败: {str(e)}")
            return []
            
    def fetch_qbit_news(self):
        """获取量子位AI新闻"""
        try:
            self.logger.info("开始获取量子位新闻...")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            url = "https://www.qbitai.com/"
            response = requests.get(url, headers=headers)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = soup.find_all('div', class_='article-item')
            
            results = []
            for item in news_items[:10]:
                try:
                    title_elem = item.find('h2', class_='title')
                    title = title_elem.text.strip()
                    link = title_elem.find('a')['href']
                    time = item.find('span', class_='time').text.strip()
                    snippet = item.find('div', class_='summary').text.strip()
                    
                    results.append({
                        "title": title,
                        "link": link,
                        "time": time,
                        "source": "量子位",
                        "snippet": snippet
                    })
                except Exception as e:
                    self.logger.error(f"解析量子位新闻项时出错: {str(e)}")
                    continue
                    
            return results
        except Exception as e:
            self.logger.error(f"获取量子位新闻失败: {str(e)}")
            return []
    
    def fetch_news(self):
        """获取新闻"""
        try:
            self.logger.info("开始获取新闻...")
            self.loading_label.config(text="正在获取新闻...")
            self.status_bar.config(text="正在获取新闻...")
            self.root.update()
            
            # 清空现有新闻
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            
            # 创建线程池
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                source = self.source_var.get()
                
                if source in ["all", "bing"]:
                    futures.append(executor.submit(self.fetch_bing_news))
                if source in ["all", "google"]:
                    futures.append(executor.submit(self.fetch_google_news))
                if source in ["all", "sina"]:
                    futures.append(executor.submit(self.fetch_sina_news))
                if source in ["all", "36kr"]:
                    futures.append(executor.submit(self.fetch_36kr_news))
                if source in ["all", "qbit"]:
                    futures.append(executor.submit(self.fetch_qbit_news))
                
                all_news = []
                for future in as_completed(futures):
                    try:
                        news_items = future.result()
                        all_news.extend(news_items)
                    except Exception as e:
                        self.logger.error(f"获取新闻源失败: {str(e)}")
            
            if not all_news:
                ttk.Label(self.scrollable_frame, 
                         text="未找到新闻，请检查网络连接或切换新闻源",
                         font=("微软雅黑", 12)).pack(pady=20)
                return
            
            # 按时间排序（如果有）
            all_news.sort(key=lambda x: x.get("time", ""), reverse=True)
            
            # 显示新闻
            for news in all_news:
                self.create_news_card(news)
            
            self.loading_label.config(text=f"找到 {len(all_news)} 条新闻")
            self.status_bar.config(text="就绪")
            
        except Exception as e:
            self.logger.error(f"获取新闻时出错: {str(e)}")
            self.loading_label.config(text="获取新闻失败")
            self.status_bar.config(text=f"错误: {str(e)}")
            messagebox.showerror("错误", f"获取新闻时出错: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AINewsApp(root)
    root.mainloop() 