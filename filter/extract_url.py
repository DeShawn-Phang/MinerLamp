import json
import os
import csv
import argparse

def main(path, out_name):
    input_dir = path
    output_path = './urllist-' + out_name + '.json'
    # read trace and extract url
    with open(output_path, 'w', newline='') as f:
        file_dict = {}
        length = len(os.listdir(input_dir))
        count = 0
        for file_name in os.listdir(input_dir):
            count = count + 1
            if '.DS' in file_name:
                continue
            print(str(count) + " / " + str(length) + "---" + file_name)
            json_file = input_dir + '/' + file_name + '/' + file_name + "-trace.json"
            url_list = []
            try:
                with open(json_file, 'r', encoding='utf-8') as fj:
                    reader = fj.read()
                    data = json.loads(reader)
                    # 获取当前样本trace中含有的所有url，存入url_list中
                    for i in range(len(data["traceEvents"])):
                        if 'data' in data["traceEvents"][i]["args"]:
                            if 'url' in data["traceEvents"][i]["args"]["data"]:
                                if data["traceEvents"][i]["args"]["data"]["url"] not in url_list and \
                                        data["traceEvents"][i]["args"]["data"]["url"] != '':
                                    url_list.append(data["traceEvents"][i]["args"]["data"]["url"])
                        if 'beginData' in data["traceEvents"][i]["args"]:
                            if 'url' in data["traceEvents"][i]["args"]["beginData"]:
                                if data["traceEvents"][i]["args"]["beginData"]["url"] not in url_list and \
                                        data["traceEvents"][i]["args"]["beginData"]["url"] != '':
                                    url_list.append(data["traceEvents"][i]["args"]["beginData"]["url"])
            except:
                pass
            file_dict[file_name] = url_list
        json.dump(file_dict, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input dir')
    parser.add_argument('-o', '--output', help='output name', default='')
    # example: python extract_url.py -i ./sok -o sok
    input_path = parser.parse_args().input
    name = parser.parse_args().output
    main(input_path, name)
