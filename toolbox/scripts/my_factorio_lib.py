import base64
import json
import zlib
import pyperclip

from pprint import pprint

from my_factorio_consts import DirectionType

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
	"""将字典加密为蓝图"""
	
	json_data = json.dumps(blueprint_dict)  # 将蓝图数据转换为 JSON 字符串
	compressed_data = zlib.compress(json_data.encode('utf-8'))  # 压缩 JSON 数据
	base64_data = base64.b64encode(compressed_data).decode('utf-8')  # 编码为 Base64
	blueprint_string = f"0{base64_data}"  # 添加蓝图前缀
	
	return blueprint_string


def blueprint_to_dict(blueprint_string: str) -> dict:
	"""将蓝图代码解码为字典"""
	
	blueprint_string = blueprint_string[1:] if blueprint_string.startswith("0") else blueprint_string  # 去掉0前缀
	compressed_data = base64.b64decode(blueprint_string)  # Base64 解码
	json_data = zlib.decompress(compressed_data).decode('utf-8')  # 解压缩数据
	blueprint_data = json.loads(json_data)  # 反序列化为 JSON
	
	return blueprint_data


class Entity:
	"""实体对象"""
	
	def __init__(self, entity: dict) -> None:
		self.entity_number = entity.get('entity_number')  # 实体序号
		self.name = entity.get('name')  # 名称
		self.type = entity.get('type')  # 类型
		self.position = entity.get('position')  # 位置
		self.direction = entity.get('direction')  # 朝向
		self.control_behavior = entity.get('control_behavior')  # 控制行为
	
	def get_dict(self) -> dict:
		"""获得该实体对象的字典格式"""
		_ = {}
		
		if self.entity_number:
			_['entity_number'] = self.entity_number
		if self.name:
			_['name'] = self.name
		if self.type:
			_['type'] = self.type
		if self.position:
			_['position'] = self.position
		if self.direction:
			_['direction'] = self.direction
		if self.control_behavior:
			_['control_behavior'] = self.control_behavior
		
		return _
	
	def replace(self, name: str = None, type: str = None) -> None:
		"""用新的name或type来置换当前实体"""
		if name:
			self.name = name
		if type:
			self.type = type
	
	def rotate(self, direction: int) -> None:
		"""旋转实体"""
		self.direction = direction


class Blueprint:
	"""蓝图对象"""
	
	def __init__(self, blueprint_dict: dict) -> None:
		blueprint = blueprint_dict['blueprint']
		
		self.entities = [Entity(x) for x in blueprint['entities']]  # 实体列表
		self.icons = blueprint.get('icons')  # 图标列表
		self.label = blueprint.get('label')  # 名称
		self.version = blueprint.get('version')  # 版本号
	
	def get_dict(self) -> dict:
		"""获得该蓝图对象的字典形式"""
		_ = {}
		
		if self.entities:
			_['entities'] = [x.get_dict() for x in self.entities]
		if self.icons:
			_['icons'] = self.icons
		if self.label:
			_['label'] = self.label
		if self.version:
			_['version'] = self.version
		
		return {'blueprint': _}
	
	def get_entities_number(self) -> int:
		"""获取实体总数"""
		return len(self.entities)


if __name__ == '__main__':
	with open('blueprint_cache.txt', 'r', encoding='utf-8') as f:
		bp = f.read()
	
	bp_dict = blueprint_to_dict(bp)
	pprint(bp_dict)
	
	bp_object = Blueprint(bp_dict)  # 对象化
	
	for entity in bp_object.entities:
		entity.rotate(DirectionType.SOUTH_EAST.value)
	
	pyperclip.copy(dict_to_blueprint(bp_object.get_dict()))
