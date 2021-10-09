import json
import os

from classes import ParserJSON, ParserXML, ParserYAML, ParserTOML

import pandas as pd

def read_struct(path):
    with open(path, 'r') as f:
        data = json.load(f)
        return data

NUM_OF_ITERATIONS = 10

PARSERS = {
    "json": ParserJSON,
    "xml": ParserXML,
    "yaml": ParserYAML,
    "toml": ParserTOML,
}

# {
#             "id": None,
#             "struct_id":struct_id,
#             "capacity": capacity,
#             "serialize":None,
#             "parse":None,
#             "over":None,
#         }

def write_stat(d_struct):
    return f"{d_struct['id']},{d_struct['struct_id']},{d_struct['capacity']},{d_struct['serialize']},{d_struct['parse']},{d_struct['over']}\n"

def read_conf():
    CONFIG_PATH = "/etc/format_tester/python_conf.json"
    with open(CONFIG_PATH) as f:
        data_conf = json.loads(f.read())
    return data_conf

def run(conf):
    batch = conf["batch"]
    path = conf["struct_dir"]+batch
    stat_path = conf["stat_dir"]
    NUM_OF_ITERATIONS = conf["n_iterations"]
    for format_name in conf["dtypes"]:
        format_parser = PARSERS[format_name]
        n_test = 0
        with open(f"{stat_path}python_{format_name}_{batch}_{NUM_OF_ITERATIONS}.csv", "w") as w_f:
            w_f.write(",struct_id,capacity,serialize,parse,over\n")
            for j,i in enumerate(sorted(os.listdir(path))):
                if j%1000 == 0:
                    print(f"Starting {format_name} file", j, " | filename = ", i)
                data = read_struct(os.path.join(path, i))
                capacity = int(i.strip(".json").split("_")[1])

                parser = format_parser(j, data, capacity)
                for k in range(NUM_OF_ITERATIONS):
                    parser.test(n_test)
                    n_test+=1
                # if j%100 == 0:
                #     print(data_str, "\n")
                # print(parser.archive)
                # print(data, capacity)
                for line in parser.archive:
                    w_f.write(write_stat(line))
                # print(df.describe())
                # break
            print(f"Savind to {format_name} csv")


if __name__ == "__main__":
    conf = read_conf()
    run(conf)