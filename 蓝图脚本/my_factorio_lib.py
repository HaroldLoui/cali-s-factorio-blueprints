import base64
import json
import zlib

'''
异星工厂蓝图格式：
'blueprint' -> dict
				L 'entities' -> [dict]
				|               L 'direction'-> int
				|				L 'entity_number' -> int
				|				L 'name' -> str
				|				L 'position' -> dict
				|					            L 'x' -> float
				|					            L 'y' -> float
				L 'icons' -> [dict]
				|			    L 'index' -> int
				|			    L 'signal' -> dict
				|				    L 'name' -> str
				|				    L 'type' -> str
				L 'item': 'blueprint'
				L 'label' -> str (蓝图的名称)
				L 'version' -> int (不清楚是什么)

带信号的常量运算器实体格式:
'control_behavior'
	L 'sections' -> dict
					L 'sections' -> [dict]
					|	               L 'filters' -> [dict]
					|                                   L 'comparator': '='
					|			                        L 'count' -> int
					|                                   L 'index' -> int
					|                                   L 'name' -> str
					|                                   L 'quality' -> str('normal', 'uncommon', 'rare', 'epic', 'legendary')
					|                                   L 'type' -> str
					L 'index' -> int
'entity_number' -> int
'name': 'constant-combinator'
'position' -> dict
				L 'x' -> float
				L 'y' -> float

'''


def dict_to_blueprint(blueprint_dict: dict) -> str:
	# 将字典加密为蓝图
	
	json_data = json.dumps(blueprint_dict)  # 将蓝图数据转换为 JSON 字符串
	compressed_data = zlib.compress(json_data.encode('utf-8'))  # 压缩 JSON 数据
	base64_data = base64.b64encode(compressed_data).decode('utf-8')  # 编码为 Base64
	blueprint_string = f"0{base64_data}"  # 添加蓝图前缀
	
	return blueprint_string


def blueprint_to_dict(blueprint_string: str) -> dict:
	# 将蓝图代码解码为字典
	
	blueprint_string = blueprint_string[1:] if blueprint_string.startswith("0") else blueprint_string  # 去掉0前缀
	compressed_data = base64.b64decode(blueprint_string)  # Base64 解码
	json_data = zlib.decompress(compressed_data).decode('utf-8')  # 解压缩数据
	blueprint_data = json.loads(json_data)  # 反序列化为 JSON
	
	return blueprint_data
