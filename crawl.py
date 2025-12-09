#我想做一个爬虫程序，爬取游泳池网站的实时占用情况，请帮我写一个Python代码示例。
#游泳池的网站是https://www.swm.de/baeder/olympia-schwimmhalle#auslastung

import requests
import json
from datetime import datetime

# 在第一步中找到的真实的 API 地址
AUSLASTUNG_API_URL = "https://counter.ticos-systems.cloud/api/gates/counter?organizationUnitIds=30182"
#"https://www.swm.de/.resources/swmTemplates/themes/swm/css/bath-capacity/bath-capacity-item.css" 

def get_realtime_occupancy():
    """获取并返回泳池的实时占用率"""
    try:
        response = requests.get(AUSLASTUNG_API_URL, timeout=10)
        response.raise_for_status() 
        
        # 1. 解析 JSON 数据，data 现在是一个列表 (List)
        data_list = response.json()
        
        # 2. 检查列表是否非空
        if not data_list:
            print("错误：API 响应列表为空，无法获取数据。")
            return None
        
        # 3. 从列表中取出第一个元素（即我们需要的字典）
        # 这是修复问题的关键步骤！
        occupancy_data = data_list[0] 
        
        # 4. 从字典中使用 .get() 方法安全地提取数据
        current_count = occupancy_data.get("personCount")
        max_capacity = occupancy_data.get("maxPersonCount")
        
        if current_count is not None and max_capacity is not None and max_capacity > 0:
            # 5. 计算占用率百分比
            occupancy_percentage = (current_count / max_capacity) * 100
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("=" * 20)
            print(f"[{timestamp}] Echtzeit-Auslastung:")
            #print(f"  当前人数: {current_count} 人")
            #print(f"  最大容量: {max_capacity} 人")
            print(f"  {100-occupancy_percentage:.2f}% frei")
            print("=" * 20)
            return occupancy_percentage
        else:
            print("错误：API 缺少人数或最大容量数据。")
            return None

    except requests.exceptions.RequestException as e:
        print(f"请求API失败: {e}")
        return None
    except json.JSONDecodeError:
        print("错误：API响应不是有效的JSON格式。")
        return None

if __name__ == "__main__":
    occupancy = get_realtime_occupancy()
    # 可以在这里添加代码，将数据存储到文件或数据库

