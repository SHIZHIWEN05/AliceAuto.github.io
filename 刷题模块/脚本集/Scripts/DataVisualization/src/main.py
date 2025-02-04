
import os
import re
import json
import sys
import time
import argparse
from collections import defaultdict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import matplotlib
matplotlib.use('Agg')  # 使用非 GUI 后端
import matplotlib.pyplot as plt
from matplotlib import font_manager
from threading import Timer  # 导入定时器




# ------------------------------ 配置文件处理 ------------------------------
def resource_path(relative_path):
    """ 获取资源文件的路径 """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def load_config():
    """ 读取 JSON 配置文件 """
    json_path = resource_path("../../../data/config.json")

    if not os.path.exists(json_path):
        print(f"错误: 找不到配置文件 {json_path}")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    return config
import os
import re

import os
import re

def generate_catalog_md(root_directory, catalog_md_path):
    """生成带有题目 div 的目录 md 文件"""
    catalog_md = []
    
    # 添加目录的标题
    catalog_md.append("# 题目目录\n")
    catalog_md.append("以下是所有题目的目录，点击链接可跳转到对应题目。\n\n")

    # 定义文件名匹配的正则模式
    pattern = r"^(?P<difficulty>.*?)_(?P<types>\{.*?\})_(?P<title>.*?)\.md$"  # 文件名的匹配模式
    
    # 遍历文件目录
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith(".md"):
                # 解析文件名，获取题目标题
                match = re.match(pattern, file)
                if match:
                    title = match.group("title")
                    difficulty = match.group("difficulty")
                    types = match.group("types")
                    
                    # 生成相对路径链接
                    relative_path = os.path.relpath(os.path.join(root, file), root_directory)
                    
                    # 构建目录项，并用 div 标签包裹
                    catalog_md.append(f"<div class=\"problem-item\">\n")
                    catalog_md.append(f"  - ### [{title}]({relative_path.replace(os.sep, '/')}) **`{difficulty}`**\n")
                    catalog_md.append(f"</div>\n")
                    
    # 将目录内容写入 md 文件
    with open(catalog_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(catalog_md))

    print(f"目录文件已生成: {catalog_md_path}")

# ------------------------------ 中文字体设置 ------------------------------
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager

import os
import matplotlib.pyplot as plt
from matplotlib import font_manager

def set_chinese_font(config=None):
    """ 设置中文字体 """
    font_found = False

    # 如果 config 为 None，则设置为空字典
    if config is None:
        config = {}

    # 获取配置文件中指定的字体目录
    font_dir = config.get("font_path", "")
    if font_dir:
        print(f"配置文件指定的字体目录：{font_dir}")
    else:




        print("未指定字体目录，将尝试从系统中查找字体...")

    # 如果配置文件中指定了字体目录，查找该目录下的字体文件
    if font_dir and not font_found:
    
        print("正在查找系统中的中文字体...")
        font_paths = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')  # 仅查找 ttf 格式的字体
        for font_path in font_paths:
            try:
                # 打印出找到的字体文件路径，方便调试
                print(f"找到字体文件路径：{os.path.abspath(font_path)}")
                font_prop = font_manager.FontProperties(fname=font_path)
                font_name = font_prop.get_name()
                # 判断是否包含常见中文字体
                if any(font in font_name for font in ['Microsoft YaHei']):
                    plt.rcParams['font.family'] = font_name
                    plt.rcParams['axes.unicode_minus'] = False
                    font_found = True
                    print(f"已找到并加载字体：{font_name}")
                    break  # 找到第一个合适的字体后即停止
            except Exception as e:
                print(f"加载字体 {font_path} 时出错: {e}")
    
    # 如果没有找到字体文件，则查找系统中的字体
    if not font_found:
        print(f"正在查找目录 {font_dir} 中的字体文件...")
        if os.path.isdir(font_dir):
            # 查找该目录下的所有 ttf 文件
            font_paths = [os.path.join(font_dir, f) for f in os.listdir(font_dir) if f.endswith('.ttf')]
            for font_path in font_paths:
                try:
                    font_prop = font_manager.FontProperties(fname=font_path)
                    font_name = font_prop.get_name()
                    # 判断是否是中文字体
                    if any(font in font_name for font in ['Microsoft YaHei']):
                        plt.rcParams['font.sans-serif'] =font_name
                        plt.rcParams['font.family'] = font_name
                        plt.rcParams['axes.unicode_minus'] = False
                        font_found = True
                        print(f"{font_path}:已找到并加载字体：{font_name}")
                        break  # 找到第一个合适的字体后即停止
                except Exception as e:
                    print(f"加载字体 {font_path} 时出错: {e}")
        else:
            print(f"指定的字体目录 {font_dir} 不存在，继续搜索系统字体")
    # 如果依然没有找到中文字体，则使用默认字体
    if not font_found:
        print("未能加载中文字体，使用默认字体 Arial")
        plt.rcParams['font.sans-serif'] =plt.rcParams['font.family'] = 'Arial'






# ------------------------------ 文件分析 ------------------------------
# 用于解析文件名的正则表达式
pattern = r"^(?P<difficulty>.*?)_(?P<types>\{.*?\})_(?P<title>.*?)\.md$"


import re

# 用于解析文件名的正则表达式
pattern = r"^(?P<difficulty>.*?)_(?P<types>\{.*?\})_(?P<title>.*?)\.md$"
author_pattern = r"\[(.*?)\]"  # 用于匹配 [作者1;作者2] 格式

import re
from collections import defaultdict

# 用于解析文件名的正则表达式
pattern = r"^(?P<difficulty>.*?)_(?P<types>\{.*?\})_(?P<title>.*?)\.md$"
author_pattern = r"\[(.*?)\]"  # 用于匹配 [作者1;作者2...作者n] 格式

import re
from collections import defaultdict

# 用于解析文件名的正则表达式
pattern = r"^(?P<difficulty>.*?)_(?P<types>\{.*?\})_(?P<title>.*?)\.md$"
author_pattern = r"\[(.*?)\]"  # 用于匹配 [作者1;作者2...作者n] 格式

import re
from collections import defaultdict

# 用于解析文件名的正则表达式
pattern = r"^(?P<difficulty>.*?)_(?P<types>\{.*?\})_(?P<title>.*?)\.md$"
author_pattern = r"\[(.*?)\]"  # 用于匹配 [作者1;作者2...作者n] 格式

def analyze_filename(filename, directory):
    """解析文件名并返回 div 和类型信息，同时读取文件第一行以确定作者"""
    match = re.match(pattern, filename)
    if match:
        types = match.group("types")[1:-1].split(";")  # 去除花括号并分割类型
        div_match = re.findall(r'div[1-5]', filename)
        authors = None
        try:
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                first_line = file.readline().strip()  # 读取第一行并去除前后空白字符
                if first_line:
                    # 尝试匹配 [作者1;作者2...作者n] 格式
                    author_match = re.match(author_pattern, first_line)
                    if author_match:
                        authors = author_match.group(1).split(';')  # 分割作者
                        authors = [a.strip() for a in authors if a.strip()]  # 去除空白字符和空字符串
                    else:
                        # 如果不符合 [作者1;作者2...作者n] 格式，尝试其他格式
                        author_match = re.match(r'\s*作者?\s*:\s*(.*)', first_line)
                        if author_match:
                            authors = [author_match.group(1).strip()]  # 提取作者名并去除空白字符
                        else:
                            authors = [first_line]  # 如果不符合格式，直接使用第一行内容作为作者名
        except Exception as e:
            print(f"读取文件 {filename} 出错: {e}")
        return div_match, types, authors
    return None, None, None

def count_author_contributions(file_info):
    """统计每个作者的创作量"""
    author_counts = defaultdict(int)
    for _, _, authors in file_info:
        if authors:
            for author in authors:
                if author:  # 确保作者名不为空
                    author_counts[author] += 1
    return author_counts

# 其他函数保持不变...
def plot_author_ranking(author_counts, save_path):
    """可视化作者创作量排名，并保存为 PNG 图片"""
    # 根据创作量对作者进行排序，创作量多的在前
    sorted_author_counts = sorted(author_counts.items(), key=lambda item: item[1], reverse=False)
    
    labels = [author for author, count in sorted_author_counts]
    sizes = [count for author, count in sorted_author_counts]
    
    plt.figure(figsize=(10, 8), dpi=150)
    plt.barh(labels, sizes, color='skyblue')
    plt.xlabel("创作量")
    plt.ylabel("作者")
    plt.title("Ranking")
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"作者排名榜图表已保存到：{save_path}")
    plt.close()
   
def scan_directory(directory, mode):
    """ 扫描目录及子目录中的所有文件并提取信息 """
    print(f"扫描的根目录的绝对路径：{os.path.abspath(directory)}")  # 打印根目录的绝对路径
    file_info = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".md"):
                div_match, types, author = analyze_filename(filename, root)
                if div_match:
                    file_info.append((div_match, types, author))
                print(f"扫描文件: {filename}")
    return file_info

# ------------------------------ 绘图和输出 ------------------------------
# ------------------------------ 绘图和输出 ------------------------------
def plot_div_distribution(div_counts, save_path):
    """ 可视化 div1 到 div5 的分布，并保存为 PNG 图片 """
    
    # 创建图像并设置大小和分辨率
    fig_width = 10
    fig_height = 6
    dpi = 150
    font_size = 12

    plt.figure(figsize=(fig_width, fig_height), dpi=dpi)
    
    # 指定 div 的排序顺序
    div_order = ['div1', 'div2', 'div3', 'div4', 'div5']
    # 按照指定顺序绘制 div 的条形图
    ordered_div_counts = {div: div_counts[div] for div in div_order if div in div_counts}
    if(len(ordered_div_counts)==0):
        print("数据异常")
        return
    # 绘制 div1-div5 分布的条形图
    plt.bar(ordered_div_counts.keys(), ordered_div_counts.values(), color='lightblue')
    plt.title("div1到div5分布", fontsize=font_size)
    plt.xlabel("div类别", fontsize=font_size)
    plt.ylabel("数量", fontsize=font_size)
    
    # 动态调整字体大小
    xticks_fontsize = max(font_size, fig_width // len(ordered_div_counts))
    plt.xticks(rotation=45, ha='right', fontsize=xticks_fontsize)
    
    # 优化布局，避免标签重叠
    plt.tight_layout()
    
    # 保存图片
    plt.savefig(save_path)
    print(f"div统计图表已保存到：{save_path}")
    plt.close()

def plot_type_distribution(type_counts, save_path):
    """ 可视化类型分布，并保存为 PNG 图片 """
    if(len(type_counts)==0):
        print("数据异常")
        return
    # 创建图像并设置大小和分辨率
    fig_width = 10
    fig_height = 6
    dpi = 150
    font_size = 12

    plt.figure(figsize=(fig_width, fig_height), dpi=dpi)
    
    # 绘制类型分布的条形图
    plt.bar(type_counts.keys(), type_counts.values(), color='lightgreen')
    plt.title("类型分布", fontsize=font_size)
    plt.xlabel("类型", fontsize=font_size)
    plt.ylabel("数量", fontsize=font_size)
    
    # 动态调整字体大小
    xticks_fontsize = max(font_size, fig_width // len(type_counts))
    plt.xticks(rotation=45, ha='right', fontsize=xticks_fontsize)
    
    # 优化布局，避免标签重叠
    plt.tight_layout()
    
    # 保存图片
    plt.savefig(save_path)
    print(f"类型统计图表已保存到：{save_path}")
    plt.close()

from collections import defaultdict

def print_statistics(file_info, save_directory):
    """打印统计信息并调用可视化输出"""
    div_counts = defaultdict(int)
    type_counts = defaultdict(int)
    author_counts = defaultdict(int)

    # 统计 div1-div5 分布、类型分布和作者创作量
    for div_match, types, authors in file_info:
        for div in div_match:
            div_counts[div] += 1
        for t in types:
            type_counts[t] += 1
        if authors:  # 确保 authors 不为空
            for author in authors:  # 遍历 authors 列表
                if author:  # 确保作者名不为空
                    author_counts[author] += 1

    # 输出文本统计
    print("div1到div5分布:")
    for div, count in div_counts.items():
        print(f"{div}: {count} 个")

    print("\n类型分布:")
    for t, count in type_counts.items():
        print(f"{t}: {count} 个")

    print("\n作者创作量排名榜:")
    for author, count in author_counts.items():
        print(f"{author}: {count} 个")

    # 确定保存路径
    div_save_path = os.path.join(save_directory, "div_distribution.png")
    type_save_path = os.path.join(save_directory, "type_distribution.png")
    author_save_path = os.path.join(save_directory, "author_ranking.png")
    
    os.makedirs(save_directory, exist_ok=True)

    # 分别保存 div、type 和 author 的统计图表
    plot_div_distribution(div_counts, div_save_path)
    plot_type_distribution(type_counts, type_save_path)
    plot_author_ranking(author_counts, author_save_path)
# ------------------------------ 文件夹监听 ------------------------------
class DirectoryHandler(FileSystemEventHandler):
    """ 文件夹变化事件处理 """

    def __init__(self, directory, save_directory, mode, interval):
        self.directory = directory
        self.save_directory = save_directory
        self.mode = mode
        self.interval = interval
        self.timer = None  # 定时器，用于延迟执行

    def on_any_event(self, event):
        """ 当任何文件发生变化时，重新扫描并更新统计 """
        if event.event_type != 'modified':  # 仅处理文件修改事件
            return

        # 如果变化的文件在输出目录（例如 PNG 文件）中，则忽略
        if event.src_path.endswith(".png"):
            print(f"忽略变化文件: {event.src_path} (PNG 文件)")
            return
        if event.src_path.endswith("README.md"):
            print(f"忽略变化文件: {event.src_path} (README 文件)")
            return

        # 如果已有定时任务正在等待，先取消它
        if self.timer is not None:
            self.timer.cancel()

        # 打印文件变化日志
        print(f"检测到变化: {event.src_path}")

        # 设置定时任务：等待一段时间后更新
        self.timer = Timer(self.interval, self.update_statistics)
        self.timer.start()

    def update_statistics(self):
        """ 更新统计并执行操作 """
        print("开始更新统计...")
        file_info = scan_directory(self.directory, self.mode)
        print_statistics(file_info, self.save_directory)
        generate_catalog_md(self.directory, "OJ/README.md")



def start_watching(directory, save_directory, interval, mode):
    """ 启动目录监听 """
    event_handler = DirectoryHandler(directory, save_directory, mode, interval)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    print(f"开始监听目录: {directory}，每 {interval} 秒检查一次")

    try:
        while True:
            time.sleep(interval)  # 使用监听间隔时间
    except KeyboardInterrupt:
        observer.stop()
        print("监听停止")
    observer.join()


# ------------------------------ 主程序入口 ------------------------------
import os

import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="文件夹统计工具")
    parser.add_argument(
        "-m", "--mode", type=int, choices=[0, 1], default=1,
        help="运行模式：1 为手动扫描模式，0 为实时监听模式（默认: 1）"
    )
    parser.add_argument(
        "-i", "--interval", type=float, default=2.0,
        help="监听间隔时间，仅在 0 模式下有效（单位：秒，默认: 2.0）"
    )
    args = parser.parse_args()

    # 读取 JSON 配置文件
    config = load_config()
    root_directory = config.get("root_directory", "")
    save_directory = config.get("png_save_directory", "")
    
    if not root_directory:
        # 如果为空，使用当前脚本目录作为根目录
        root_directory = os.path.dirname(os.path.abspath(__file__))

    # 拼接根目录路径，将配置中的相对路径与脚本目录拼接
    root_directory = os.path.join( os.getcwd(), root_directory)

    set_chinese_font(config)  # 设置中文字体

    if args.mode == 1:
        print("手动扫描模式")
        file_info = scan_directory(root_directory, args.mode)
        print_statistics(file_info, save_directory)

       
        generate_catalog_md(".", "OJ/README.md")

    else:
        print("实时监听模式")
        start_watching(root_directory, save_directory, args.interval, args.mode)
