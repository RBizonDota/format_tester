from time import time
from copy import deepcopy

import json

from dicttoxml import dicttoxml
import xmltodict

import yaml

import toml

class ParserABS:
    def __init__(self, struct_id, data, capacity, save=False, dtype='unknown'):
        self.data = data
        self.capacity = capacity
        self.stat = {
            "id": None,
            "struct_id":struct_id,
            "capacity": capacity,
            "serialize":None,
            "parse":None,
            "over":None,
        }
        self.archive = [
        ]
        self.save = save
        self.dtype = dtype

    def parse(self,data_str):
        data, timestamp = self._parse(data_str)
        self.stat["parse"] = timestamp/self.capacity
        self.stat["over"] = len(data_str)/self.capacity
        return data
    
    def serialize(self):
        data, timestamp = self._serialize(self.data)
        self.stat["serialize"] = timestamp/self.capacity
        # self.stat["over"].append(len(data_str)/self.capacity)
        return data

    def save_stat(self):
        self.archive.append(deepcopy(self.stat))

    def test(self, test_id):
        data_str = self.serialize()
        # print(data_str)
        # print("    ", self.capacity, len(data_str))
        data = self.parse(data_str)
        self.stat["id"] = test_id
        self.save_stat()
        return data, data_str

# ----------------------- JSON ---------------------------------
def json_parse(str_data):
    start = time()
    data = json.loads(str_data)
    stop = time()-start
    return data, stop

def json_serialize(data):
    start = time()
    str_data = json.dumps(data)
    stop = time()-start
    return str_data, stop


class ParserJSON(ParserABS):
    def  __init__(self, struct_id, data, capacity):
        super().__init__(struct_id, data, capacity)
        self._parse = json_parse
        self._serialize = json_serialize

# ----------------------- XML ---------------------------------

def xml_serialize(data):
    start = time()
    xml_str = dicttoxml(data, attr_type=False, root=False)
    stop = time()-start
    # print(xml_str)
    return "<root>"+xml_str.decode("utf-8")+"</root>", stop

def xml_parse(data_str):
    start = time()
    data = xmltodict.parse(data_str)
    stop = time()-start
    return data, stop

class ParserXML(ParserABS):
    def  __init__(self, struct_id, data, capacity):
        super().__init__(struct_id, data, capacity, save=False, dtype="xml")
        self._parse = xml_parse
        self._serialize = xml_serialize

# ----------------------- YAML --------------------------------

def yaml_serialize(data):
    start = time()
    yaml_str = yaml.dump(data)
    stop = time()-start
    return yaml_str, stop

def yaml_parse(data_str):
    start = time()
    data = yaml.load(data_str, Loader=yaml.BaseLoader)
    stop = time()-start
    return data, stop

class ParserYAML(ParserABS):
    def  __init__(self, struct_id, data, capacity):
        super().__init__(struct_id, data, capacity, save=False, dtype="yaml")
        self._parse = yaml_parse
        self._serialize = yaml_serialize

# ----------------------- TOML --------------------------------

def toml_serialize(data):
    start = time()
    yaml_str = toml.dumps(data)
    stop = time()-start
    return yaml_str, stop

def toml_parse(data_str):
    start = time()
    data = toml.loads(data_str)
    stop = time()-start
    return data, stop

class ParserTOML(ParserABS):
    def  __init__(self, struct_id, data, capacity):
        super().__init__(struct_id, data, capacity, save=False, dtype="toml")
        self._parse = toml_parse
        self._serialize = toml_serialize
