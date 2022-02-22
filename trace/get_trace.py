import argparse
import csv
import time
import random
import threading
import os
import json
import subprocess
from urllib import parse

# remove unrelated info from json to make it small
def compress_json(json_path):
    with open(json_path, 'r') as f:
        trace_json = json.load(f)
        trace_events = trace_json['traceEvents']
    new_events = []
    for te in trace_events:
        # mark main thread and sub thread
        if te['cat'] == '__metadata':
            new_events.append(te)
        # build a mapping table for stack events
        elif te['name'] == 'Profile':
            new_events.append(te)
        # add function events
        elif te['name'] == 'FunctionCall':
            new_events.append(te)
        # add timeline events
        elif te['cat'] == 'devtools.timeline':
            if 'data' in te['args'].keys():
                if 'stackTrace' in te['args']['data'].keys():
                    new_events.append(te)
        # add task events
        elif te['name'] == 'ThreadControllerImpl::RunTask':
            if 'src_func' in te['args'].keys():
                new_events.append(te)
        # add stack events
        elif te['name'] == 'ProfileChunk':
            if 'cpuProfile' in te['args']['data'].keys():
                new_events.append(te)
    with open(json_path, 'w') as f:
        json.dump({'traceEvents': new_events}, f)

class TraceRecorder():

    def __init__(self, docker_name, port, compress=False):

        # seven kinds of miner
        self.miner_list = ['coinIMP', 'cryptowebminer', 'monerominer', 'webminepool', 'webmine', 'cryptoloot', 'bmst']
        self.result = None
        self.compress = compress
        self.docker_name = docker_name
        self.port = port

    # default protocol is http
    def get_url(self, url):
        if 'http' not in url:
            return 'http://' + url
        else:
            return url

    # record trace
    def start_record(self, url, output, mode, agent=False, miner='none'):
        # get encoded string as file/dir name
        site_name = parse.quote_plus(url)
        if len(site_name) > 240:
            site_name = site_name[:240]
        trace_name = site_name + '-' + miner
        trace_dir = os.path.join(output, trace_name)
        trace_path = os.path.join(trace_dir, trace_name + '-trace.json')
        # if existed, skip
        if miner == 'none' and os.path.exists(trace_path):
            print('[EXISTED!]', trace_path)
            self.result = 0
            return
        if miner != 'none':
            for m in self.miner_list:
                tname = site_name + '-' + m
                tdir = os.path.join(output, tname)
                tpath = os.path.join(tdir, tname + '-trace.json')
                if os.path.exists(tpath):
                    print('[MINER EXISTED!]', tpath)
                    self.result = 0
                    return
        # get current path and print related info
        current_path = os.getcwd()
        print("Time:", time.asctime(time.localtime((time.time()))))
        print("Inserted miner:", miner)
        print("Agent:", agent)
        print("---------------------Docker-----------------------")
        shell_file = "start_record.sh"
        # run docker, set shared memory as 1G, port mapped to 1088
        self.result = os.system('docker run --name=' + self.docker_name + ' --shm-size 1G --rm --cpus=1.0 -p '
                                + self.port + ':1088 -v ' + current_path + ':/app alekzonder/puppeteer:latest bash '
                                + shell_file + ' ' + url + ' ' + trace_dir + ' '
                                + miner + ' ' + str(agent) + ' ' + mode + ' 2>bash.log')  # 2>bash.log
        # if fail, remove it
        if self.result == 256 or self.result == 1:
            if os.path.exists(trace_dir):
                os.rmdir(trace_dir)
        # if compress switch is on, compress it
        if self.compress and os.path.exists(trace_path):
            print("compress the trace...")
            compress_json(trace_path)

    # set timeout to avoid stuck.
    def setTimeOut(self, url, output, mode, agent, miner):
        # if container is still working after 200s, kill it
        t = threading.Thread(target=self.start_record, args=(url, output, mode, agent, miner))
        t.setDaemon(True)
        t.start()
        t.join(200)
        r = os.popen('docker ps --format "{{.Names}}"')
        for name in r.readlines():
            if self.docker_name == name[:-1]:
                os.popen('docker kill ' + self.docker_name)  # os.popen is more stable then os.system
                print("[TIMEOUT ERROR] kill docker")
                with open('error.log', 'a') as f:
                    f.write(url + ", TimeoutError: killed by get_trace.py\n")
                self.result = 256

    # get train set
    def get_train_trace(self, begin, url_list, output, agent):
        count = begin
        for url in url_list:
            url = self.get_url(url)
            # print the order of url in url list
            print('[', count, ']', url)
            # try to get the trace of original website
            self.setTimeOut(url, output, "train", agent, 'none')
            # if error, skip it
            if self.result != 0: # windows error code is 1, linux error code is 256
                print("--------------------------------------------------")
                count += 1
                continue
            # if there is no error, try to insert random miner into website, and record again
            miner = random.choice(self.miner_list)
            self.setTimeOut(url, output, "train", agent, miner)
            print("--------------------------------------------------")
            count += 1

    # get test set
    def get_test_trace(self, begin, url_list, output, agent):
        count = begin
        for url in url_list:
            url = self.get_url(url)
            # print the order of url in url list
            print('[', count, ']', url)
            self.setTimeOut(url, output, "test", agent, 'none')
            print("--------------------------------------------------")
            count += 1

    # all the trace is miner-inserted
    def get_simulate_trace(self, begin, url_list, output, agent):
        count = begin
        for url in url_list:
            url = self.get_url(url)
            # print the order of url in url list
            print('[', count, ']', url)
            miner = random.choice(self.miner_list)
            self.setTimeOut(url, output, "test", agent, miner)
            print("--------------------------------------------------")
            count += 1

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
    parser.add_argument('-m', dest='mode', metavar='MODE', choices=['train', 'test', 'simulate'], default='test',
                        help="choose the mode of recorder")
    parser.add_argument('-l', dest='list', metavar='CSV/TXT', required=True,
                        help="the input csv of url list")
    parser.add_argument('-o', dest='output', metavar='DIR', required=True,
                        help="the output dir of trace")
    parser.add_argument('-b', dest='begin', metavar='NUMBER', default=0,
                        help="the begin index of url list")
    parser.add_argument('-e', dest='end', metavar='NUMBER', default=-1,
                        help="the end index of url list")
    parser.add_argument('-a', dest='agent', action='store_true', default=False,
                        help="open agent")
    parser.add_argument('-c', dest='compress', action='store_true', default=False,
                        help="compress size of trace")
    parser.add_argument('-n', dest='docker_name', default='mydocker',
                        help="the name of docker")
    parser.add_argument('-p', dest='port', default='1088',
                        help='the local port number, not allowed occupied, which will be mapped to 1088 in container')

    args = parser.parse_args()
    mode = args.mode
    list = args.list
    begin = int(args.begin)
    end = int(args.end)
    output = args.output
    agent = args.agent
    compress = args.compress
    docker_name = args.docker_name
    port = args.port

    # get list
    if '.csv' in list:
        with open(list, 'r') as f:
            reader = csv.reader(f)
            if end!=-1:
                url_list =[row[1] for row in reader][begin: end]
            else:
                url_list = [row[1] for row in reader][begin:]
    elif '.txt' in list:
        with open(list, 'r') as f:
            if end!=-1:
                url_list = [line[:-1] for line in f.readlines()][begin: end]
            else:
                url_list = [line[:-1] for line in f.readlines()][begin:]

    # check docker
    try:
        subprocess.check_output('docker ps', shell=True)
        # kill the remaining container
        r = os.popen('docker ps --format "{{.Names}}"')
        for name in r.readlines():
            if docker_name == name[:-1]:
                os.popen('docker kill ' + docker_name)
    except:
        exit()

    # make output dir
    if not os.path.exists(output):
        os.mkdir(output)

    # authorize
    os.popen("chmod -R 777 record_trace.js")
    os.popen("chmod -R 777 " + output)

    # clear error.log
    with open('error.log', 'a') as f:
        f.write("-----------------" + time.asctime(time.localtime((time.time()))) + "-----------------\n")

    # get trace according to url list
    tr = TraceRecorder(docker_name, port, compress)
    if mode=='train':
        tr.get_train_trace(begin, url_list, output, agent)
    elif mode=='test':
        tr.get_test_trace(begin, url_list, output, agent)
    elif mode=='simulate':
        tr.get_simulate_trace(begin, url_list, output, agent)


if __name__ == '__main__':
    main()