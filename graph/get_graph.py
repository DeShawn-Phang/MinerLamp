import argparse
import os
import sys
import random
import jsonlines
from graph_constructor import GraphConstructor

def get_graphs(dir, out):
    if not os.path.exists(dir):
        print("Error!!! Can not find the input dir!", dir)
        exit()
    gc = GraphConstructor()
    count = 0
    if not os.path.exists(out):
        os.mkdir(out)
    # TODO: multi-thread for accelerating
    for root, dirs, files in os.walk(dir, topdown=True):
        for file_name in files:
            if ".json" in file_name:
                count += 1
                trace_path = os.path.join(root, file_name)
                print(count, "Construct graph for", file_name)
                try:
                    # construct and print graph
                    graph, websocket, mining = gc.construct(trace_path)
                    gc.print_graph()
                    # some scripts may fail to insert, so we mark them as 0
                    if '-none' in file_name:
                        label = 0.0
                    else:
                        if websocket==False or len(graph['adjacency_lists'][1])==0 or mining==False:
                            print("no-websocket or no-worker or no-mining")
                            label = 0.0
                        else:
                            label = 1.0
                    # add graph data to jsonl file
                    with jsonlines.open(os.path.join(out, "graphs.jsonl"), mode='a') as jl:
                        item = {"Property": label, "filename": os.path.split(trace_path)[-1], "graph": graph}
                        jl.write(item)
                except Exception:
                    print("ERROR!")
                    with open("error.log", 'a') as f:
                        f.write(trace_path+'\n')
                        f.write(str(sys.exc_info())+'\n')
                print()

def generate_dataset(out, mode):
    jsonl_path = os.path.join(out, 'graphs.jsonl')
    if mode == 'train':
        train_rate = 0.8
        valid_rate = 0.1
    else:
        train_rate = 0
        valid_rate = 0
    with open(jsonl_path, 'r') as f:
        if not os.path.exists(out):
            os.mkdir(out)
        graph_list = [g for g in jsonlines.Reader(f).iter()]
        random.shuffle(graph_list)
        size = len(graph_list)
        print("size of dataset:", size)
        train_num = int(size * train_rate)
        valid_num = size * valid_rate
        count = 0
        for row in graph_list:
            if count < train_num:
                jsonl_out_path = os.path.join(out, 'train.jsonl')
            elif count < train_num + valid_num:
                jsonl_out_path = os.path.join(out, 'valid.jsonl')
            else:
                jsonl_out_path = os.path.join(out, 'test.jsonl')
                with open(os.path.join(out, 'list.txt'), 'a') as f:
                    f.write(row['filename'] + '\n')
            with jsonlines.open(jsonl_out_path, mode='a') as writer:
                writer.write(row)
                count += 1
                print("have processed " + str(count) + "/" + str(size) + " rows", flush=True)
    if mode == 'train':
        if os.path.exists(os.path.join(out, 'train.jsonl.gz')):
            os.remove(os.path.join(out, 'train.jsonl.gz'))
        if os.path.exists(os.path.join(out, 'valid.jsonl.gz')):
            os.remove(os.path.join(out, 'valid.jsonl.gz'))
        os.system("gzip " + os.path.join(out, 'train.jsonl'))
        os.system("gzip " + os.path.join(out, 'valid.jsonl'))
    if os.path.exists(os.path.join(out, 'test.jsonl.gz')):
        os.remove(os.path.join(out, 'test.jsonl.gz'))
    os.system("gzip " + os.path.join(out, 'test.jsonl'))

def main():
    brand = r"""                                                                                             
     _ _ _     _   _____ _             __                  
    | | | |___| |_|     |_|___ ___ ___|  |   ___ _____ ___ 
    | | | | -_| . | | | | |   | -_|  _|  |__| .'|     | . |
    |_____|___|___|_|_|_|_|_|_|___|_| |_____|__,|_|_|_|  _|
                                                      |_|  
     """
    print(brand)
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', dest='mode', default='test', choices=['train', 'test'])
    parser.add_argument('-d', dest='dir', metavar='DIR', required=True,
                        help="the input dir of dataset")
    parser.add_argument('-o', dest='out', metavar='DIRNAME', required=True,
                        help="output dir name")
    args = parser.parse_args()
    dir = args.dir
    out = args.out
    mode = args.mode
    get_graphs(dir, out)
    generate_dataset(out, mode)

if __name__ == '__main__':
    main()