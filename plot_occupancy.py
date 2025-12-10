import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

DATA_FILE = "pool_occupancy_log.csv"

def plot_daily_occupancy():
    """读取 CSV 文件并绘制占用率随时间变化的曲线图"""
    try:
        # 1. 读取数据
        df = pd.read_csv(DATA_FILE)
        
        # 2. 数据预处理
        # 确保 Timestamp 列是 datetime 类型，以便正确绘图
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        
        # 提取日期，只绘制最近一天的记录（假设文件中有几天的记录）
        latest_date = df['Timestamp'].dt.date.max()
        df_today = df[df['Timestamp'].dt.date == latest_date]
        
        if df_today.empty:
            print("错误：数据集中没有足够的当日记录来绘图。")
            return
            
        # 3. 绘图设置
        plt.figure(figsize=(12, 6))
        
        # 绘制占用率曲线
        plt.plot(df_today['Timestamp'], df_today['OccupancyPercentage'], 
                 marker='o', linestyle='-', color='skyblue', label='Occupancy Rate')
        
        # 4. 优化图表显示
        plt.title(f"Olympia Schwimmhalle real-time utilization figure ({latest_date})")
        plt.xlabel("Time")
        plt.ylabel("Utilization (%)")
        plt.grid(True, linestyle='--', alpha=0.7)
        # x轴时间控制在当天范围内
        plt.xlim(datetime.combine(latest_date, datetime.min.time()), 
                 datetime.combine(latest_date, datetime.max.time()))
        plt.yticks(range(0, 101, 10)) # Y轴显示 0% 到 100%
        plt.tight_layout() # 自动调整布局，避免标签重叠
        
        # 5. 保存图像
        image_filename = f"occupancy_plot_{latest_date}.png"
        plt.savefig(image_filename)
        print(f"\n绘图完成！图像已保存为 {image_filename}")
        
    except FileNotFoundError:
        print(f"错误：找不到数据文件 {DATA_FILE}。请先运行监控脚本收集数据。")
    except Exception as e:
        print(f"绘图过程中发生错误: {e}")

if __name__ == "__main__":
    plot_daily_occupancy()