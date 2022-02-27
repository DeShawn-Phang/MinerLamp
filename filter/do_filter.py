import json
import os
import csv
import re
import argparse

def get_result(input_path, output_path):
    with open('./mining_keywords.json', 'r') as mk:
        keywords = json.load(mk)
    csv.field_size_limit(500 * 1024 * 1024)
    with open(output_path, 'w', newline='') as f:
        csv_file = csv.writer(f)
        input_json = json.load(open(input_path, 'r'))
        count = -1
        for key in input_json.keys():
            count += 1
            if count == 0:
                csv_file.writerow(["file_name", "FKMM", "service"])
                continue
            print(count)
            file_name = key
            url_list = input_json[key]
            flag = 0
            kw_result = []
            for url in url_list:
                for keyword in keywords.keys():
                    for v in keywords[keyword]:
                        pattern = re.compile(v.replace("*", ".*"))
                        result = re.match(pattern, url)
                        if str(result) != "None":
                            flag = 1
                            if keyword not in kw_result:
                                kw_result.append(keyword)
            csv_file.writerow([file_name, flag, kw_result])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input path')
    parser.add_argument('-o', '--output', help='output path', default='')
    # example: python do_filter.py -i urllist-sok_known.csv -o sok_known
    input_path = parser.parse_args().input
    output_path = "result-" + parser.parse_args().output + ".csv"
    get_result(input_path, output_path)