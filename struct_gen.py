import os
import random
import string
from datetime import datetime

import json

CONFIG_FILE = "/etc/format_tester/generator.json"
def read_config():
    with open(CONFIG_FILE, "r") as c_f:
        return json.loads(c_f.read())

config = read_config()

STRUCT_FOLDER_DIR = config["struct_dir"]
DESC_FOLDER_DIR = config["desc_dir"]

def generate_random_string(struct_desc):
    str_len = random.randint(
                struct_desc["strings"]["min"], 
                struct_desc["strings"]["max"]
            )

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=str_len))

def generate_random_int(struct_desc):
    return random.randint(
                struct_desc["integers"]["min"], 
                struct_desc["integers"]["max"]
            )

def generate_random_float(struct_desc):
    std = struct_desc["floats"]["max"]-struct_desc["floats"]["min"]
    return std*random.random()+struct_desc["floats"]["min"]


LAYERS = config["layers"]
ARRAYS = config["arrays"]
STRING_NUMS = config["string_nums"]
STRING_LENS = config["string_lens"]
INTEGER_NUMS = config["integer_nums"]
FLOATS_NUMS = config["float_nums"]
def generate_struct_desc():
    i = 0
    for layers in LAYERS:
        for arrays in ARRAYS:
            for string_nums in STRING_NUMS:
                for min_string in STRING_LENS:
                    for int_nums in INTEGER_NUMS:
                        for float_nums in FLOATS_NUMS:
                            yield i,{
                                "layers": layers,
                                "arrays": {
                                    "number": arrays,
                                    "item_type":"strings"
                                },
                                "strings":{
                                    "number": string_nums,
                                    "min": min_string,
                                    "max": random.randint(min_string, min_string+5),
                                },
                                "integers":{
                                    "number":int_nums,
                                    "min": -16000,
                                    "max": 16000,
                                },
                                "floats": {
                                    "number":float_nums,
                                    "min": -16000,
                                    "max": 16000,
                                }
                            }
                            i+=1

def generate_struct_csv():
    i = 0
    for layers in LAYERS:
        for arrays in ARRAYS:
            for string_nums in STRING_NUMS:
                for min_string in STRING_LENS:
                    for int_nums in INTEGER_NUMS:
                        for float_nums in FLOATS_NUMS:
                            yield f"{i},{layers},{arrays},{string_nums},{min_string},{int_nums},{float_nums}"

def generate_struct(struct_desc):
    res_struct = {}
    res_data_capacity = 0

    # Генерация вложенных структур
    link = res_struct
    for i in range(struct_desc["layers"]):
        link["layers"] = {
            "a":2
        }
        res_data_capacity +=4+len("1")+len("layers")
        link = link["layers"]

    if struct_desc["arrays"]["number"]!=0:
        res_struct["array"]=[]
        res_data_capacity+=len("array")
        if struct_desc["arrays"]["item_type"]=="integers":
            item_generator = generate_random_int
        elif struct_desc["arrays"]["item_type"]=="strings":
            item_generator = generate_random_string
        elif struct_desc["arrays"]["item_type"]=="floats":
            item_generator = generate_random_float
        for i in range(struct_desc["arrays"]["number"]):
            item_to_add = item_generator(struct_desc)
            res_struct["array"].append(item_to_add)
            res_data_capacity+=len(item_to_add)
    
    for i in range(struct_desc["strings"]["number"]):
        res_struct[f"s{i}"] = generate_random_string(struct_desc)
        res_data_capacity+=len(f"s{i}")+len(res_struct[f"s{i}"])
        
        

    for i in range(struct_desc["integers"]["number"]):
        res_struct[f"i{i}"] = generate_random_int(struct_desc)
        res_data_capacity+=4+len(f"i{i}")
        
    for i in range(struct_desc["floats"]["number"]):
        res_struct[f"f{i}"] = generate_random_float(struct_desc)
        res_data_capacity+=4+len(f"i{i}")

    # print(res_struct, res_data_capacity)
    return res_struct, res_data_capacity

if __name__ == "__main__":
    time_string = datetime.now().strftime("%m_%d_%Y__%H_%M_%S")
    os.makedirs(os.path.join(STRUCT_FOLDER_DIR, time_string))

    with open(os.path.join(DESC_FOLDER_DIR, time_string), "w") as d_f:
        d_f.write(f"id,capacity,layers,arrays,strings_num,strings_min,strings_max,integers_num,integers_min,integers_max,floats_num,floats_min,floats_max\n")
        for i, test_struct_desc in generate_struct_desc():
            struct, capacity = generate_struct(test_struct_desc)
            with open(os.path.join(STRUCT_FOLDER_DIR, time_string, f"{str(i).zfill(5)}_{capacity}.json"), "w") as f:
                f.write(json.dumps(struct))
            
            d_f.write(f"{i},{capacity},{test_struct_desc['layers']},{test_struct_desc['arrays']['number']},{test_struct_desc['strings']['number']},{test_struct_desc['strings']['min']},{test_struct_desc['strings']['max']},{test_struct_desc['integers']['number']},{test_struct_desc['integers']['min']},{test_struct_desc['integers']['max']},{test_struct_desc['floats']['number']},{test_struct_desc['floats']['min']},{test_struct_desc['floats']['max']}\n")