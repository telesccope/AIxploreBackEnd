import os
import base64
from datetime import datetime

def save_image_to_server(image_data, current_user):
    """
    保存Base64编码的图像到服务器，并将其存储到以用户名为目录的路径中。
    
    :param image_data: Base64编码的图像数据
    :param current_user: 当前用户的用户名
    :return: 保存的图像文件路径
    """
    # 定义上传目录的根目录
    base_upload_dir = 'uploads/images'
    
    # 用户专属目录
    user_upload_dir = os.path.join(base_upload_dir, current_user)
    
    # 确保用户目录存在
    if not os.path.exists(user_upload_dir):
        os.makedirs(user_upload_dir)

    # 提取图像类型（例如 png 或 jpeg）
    header, encoded = image_data.split(',', 1)
    file_extension = header.split('/')[1].split(';')[0]  # 提取文件扩展名（png 或 jpeg）
    if file_extension not in ['png', 'jpeg', 'jpg']:
        raise ValueError("Unsupported image format")

    # 生成唯一的文件名
    filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}.{file_extension}"
    file_path = os.path.join(user_upload_dir, filename)

    # 保存图像到服务器
    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(encoded))

    return file_path  # 返回图像路径

import yaml

def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

config = load_yaml('prompts.yaml')

def get_system_message(config=config, **kwargs):
    default_values = {
        "latitude": 51.5074,
        "longitude": -0.1278,
        "nearby_pois": "Example POI 1, Example POI 2",
        "language": "Chinese",
        "food": "Spicy, no peanuts",
        "preference": "Museum, theatre",
        "ai_style": "Detailed"
    }
    default_values.update(kwargs)
    
    system_message_template = config['system_message']
    
    # 直接格式化
    formatted_message = system_message_template.format(**default_values)
    
    return formatted_message

def get_id(nearby_pois,config=config):
    id_template = config.get('getid','')
    formatted_id = id_template.format(nearby_pois=nearby_pois)
    return formatted_id

def get_output(discription,config=config):
    output_template = config.get('getoutput', '')
    formatted_output = output_template.format(discription=discription)
    return formatted_output

def get_sample_discription(config=config):
    return config['getsamplediscription']

def get_title(dialogue, config=config):
    title_template = config.get('title', '')
    if not title_template:
        raise ValueError("Title template not found in configuration.")
    formatted_title = title_template.format(dialogue=dialogue)
    return formatted_title

def get_association(dialogue, config=config):
    association_template = config['association']
    formatted_association = association_template.format(dialogue=dialogue)
    return formatted_association



import requests

tools = [{
  "type": "function",
  "name": "get_item_id",
  "description": "Get historic England list entry ID by , returning the entry description.",
  "parameters": {
    "type": "object",
    "required": [
      "id"
    ],
    "properties": {
      "id": {
        "type": "string",
        "description": "The unique identifier for the historic England list entry"
      }
    },
    "additionalProperties": False
  }
}]

from lxml import html

def fetch_official_list_entry(entry_id: str) -> str:
    url = f"https://historicengland.org.uk/listing/the-list/list-entry/{entry_id}?section=official-list-entry"
    print(f"Fetching: {url}")

    try:
        response = requests.get(url, timeout=10)
        print(response)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"请求失败：{e}"

    try:
        tree = html.fromstring(response.content)
        # 你的 XPath：//*[@id="official-list-entry"]/div/div[4]/div[2]/div
        elements = tree.xpath('//*[@id="official-list-entry"]/div/div[4]/div[2]/div')

        if not elements:
            return "未找到官方清单内容。"

        text_content = elements[0].text_content().strip()
        print(text_content)
        return text_content

    except Exception as e:
        return f"解析失败：{e}"

def fetch_poi(latitude: float, longitude: float, radius: int = 100) -> str:
    """
    Fetch heritage POIs from the local Flask service and return a formatted string.
    
    Args:
        latitude (float): Latitude of the center point.
        longitude (float): Longitude of the center point.
        radius (int): Search radius in meters.

    Returns:
        str: Formatted POI details, or message if none found.
    """
    url = "http://127.0.0.1:5003/heritage"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius,
    }

    response = requests.get(url, params=params)
    data = response.json()

    entries = data.get("entries", [])
    if not entries:
        return "No POI found for the given criteria."

    lines = []
    for item in entries:
        name = item.get("Name", "N/A")
        grade = item.get("Grade", "N/A")
        entry_number = item.get("List entry number", "N/A")
        url = item.get("NHLE link", "N/A")
        lines.append(f"Name: {name}, Grade: {grade}, Entry: {entry_number}, URL: {url}")

    return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    config = load_yaml('prompts.yaml')
    dialogue = "User: What are some spicy food options in London?\nAIxplore: Let me suggest a few places..."
    discription = "War memorial. Erected 1922, after the First World War, to the design of the architects Cheadle and Harding and sculptor Albert Toft. Bronze cast by A B Burton at the Thames Ditton Foundry, London. Further inscriptions added after the Second World War."
    system_message = get_system_message(config)
    get_id = get_id(config,nearby_pois=fetch_poi(51.5074, -0.1278))
    get_output = get_output(discription)
    association = get_association(dialogue)

    print("System Message:\n", system_message)
    print("\nFirst:\n", get_id)
    print("\nTitle:\n", get_output)
    print("\nAssociation:\n", association)