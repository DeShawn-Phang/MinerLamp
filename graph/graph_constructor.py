import json
import networkx as nx
import random
import matplotlib.pyplot as plt
import os

class GraphConstructor():

    def __init__(self):
        # basic info
        self.file_path = ""
        self.main_tid = 0
        self.sub_tids = []
        # graph construct info
        self.last_func = {}
        self.last_timeline = {}
        self.last_task = {}
        self.func_dict = {}
        self.task_arrs = {}
        self.timeline_arrs = {}
        self.empty_node = [0,0,0,0,0,0,0,0,0,0] # new
        self.last_func_sig = {}
        self.websocket_create = False
        # features
        self.feature_list = ['FunctionCall', 'ResourceSendRequest', 'WebSocketCreate', 'TimerInstall',
             'PostMessageToWorkerGlobalScope', 'PostMessageToWorkerObject', 'ResourceSendRequest-js', 'ResourceSendRequest-wasm']
        # graph
        self.node_features = []
        self.adjacency_lists = [[],[],[],[]]
        self.graph = {'node_features': self.node_features, 'adjacency_lists': self.adjacency_lists}
        # count
        self.index_count = {}
        self.index_dur = {}
        self.last_task_dur = {}

    # add a starting node to main thread
    def add_starting_node(self):
        # init sub thread node
        for sub_tid in self.sub_tids:
            self.last_func[sub_tid] = -1
            self.last_timeline[sub_tid] = -1
            self.last_task[sub_tid] = ""
            self.timeline_arrs[sub_tid] = []
            self.task_arrs[sub_tid] = []
            self.last_func_sig[sub_tid] = ""
            self.func_dict[sub_tid] = {}
            self.last_task_dur[sub_tid] = 0 # time feature

        # add starting node
        self.node_features.append(self.empty_node)
        # init last_xxx
        self.last_func[self.main_tid] = 0
        self.last_timeline[self.main_tid] = 0
        self.last_task[self.main_tid] = ""
        self.timeline_arrs[self.main_tid] = []
        self.task_arrs[self.main_tid] = []
        self.last_func_sig[self.main_tid] = ""
        self.func_dict[self.main_tid] = {}
        self.last_task_dur[self.main_tid] = 0 # time feature

    # construct the graph
    def construct(self, trace_path):
        self.__init__()
        self.file_path = trace_path
        with open(trace_path, 'r') as f:
            trace_json = json.load(f)
            trace_events = trace_json['traceEvents']
        # select some trace events
        tes = []
        func_te_temp = None
        for te in trace_events:
            # identify main thread and sub thread
            if te['cat'] == '__metadata':
                if 'name' in te['args'].keys():
                    if te['args']['name'] == 'CrRendererMain':
                        self.main_tid = te['tid']
                    if 'DedicatedWorker thread' in te['args']['name']:
                        self.sub_tids.append(te['tid'])
            # add function events
            elif te['name'] == 'FunctionCall':
                if te['ph'] == 'B':
                    func_te_temp = te
                    continue
                if te['ph'] == 'E':
                    if func_te_temp is not None:
                        func_te_temp['dur'] = te['ts'] - func_te_temp['ts']
                        tes.append(func_te_temp)
                else:
                    tes.append(te)
            # add timeline events
            elif te['cat'] == 'devtools.timeline':
                if 'data' in te['args'].keys():
                    if 'stackTrace' in te['args']['data'].keys(): # limit quantity
                        if te['name'] in self.feature_list:
                            tes.append(te)
            # add task events
            elif te['name'] == 'ThreadControllerImpl::RunTask':
                if 'src_func' in te['args'].keys():
                    tes.append(te)

        # sort and construct
        tes.sort(key = lambda x : x['ts'])
        self.add_starting_node()
        for te in tes:
            tid = te['tid']
            if tid not in self.sub_tids and tid != self.main_tid:
                continue
                # add function events
            elif te['name'] == 'FunctionCall':
                self.add_func(te)
            # add timeline events
            elif te['cat'] == 'devtools.timeline':
                if te['name'] in self.feature_list:
                    self.add_timeline(te)
            # add task events
            elif te['name'] == 'ThreadControllerImpl::RunTask':
                if te['args']['src_func'] in self.feature_list:  # limit quantity
                    self.add_task(te)

        mining = False
        for index in self.index_count:
            if self.index_count[index]>20:
                c = 1
            else:
                c = self.index_count[index]/20
            self.node_features[index][-2] = c

            if self.index_dur[index]>10000000:
                d = 1
            else:
                d = self.index_dur[index]/10000000
            self.node_features[index][-1] = d
            # if (c >= 0.1 and d >= 0.1):
            #     with open("record_file.txt", 'a') as rf:
            #         rf.write(self.file_path+" key-func-id:"+str(index)+" num-of-exec:"+str(c*20)+" time-of-exec:"+str(d*10)+"\n")
            if ((c>=0.15 and d>=0.2) or (c>=0.1 and d>=0.4)) and index in [e[1] for e in self.adjacency_lists[1]]:
                # print("key-func-id:"+str(index)+" num-of-exec:"+str(c*20)+" time-of-exec:"+str(d*10))
                mining = True
        return self.graph, self.websocket_create, mining

    def add_func(self, te):
        tid = te['tid']
        feature = 'FunctionCall'
        func_sig = self.get_func_sig(te['args']['data'])
        if func_sig not in self.func_dict[tid].keys():
            func_index = len(self.node_features)
            vector = self.feature2vector(feature)
            self.node_features.append(vector)
            self.func_dict[tid][func_sig] = func_index
        else:
            func_index = self.func_dict[tid][func_sig]
        # connect to last func
        if tid == self.main_tid:
            # connect to last node (avoid repetition)
            if [self.last_func[tid], func_index] not in self.adjacency_lists[0]:
                self.adjacency_lists[0].append([self.last_func[tid], func_index])
        else:
            if self.last_func[tid] == -1:
                # connect to main thread
                self.adjacency_lists[1].append([self.last_func[self.main_tid], func_index])
            else:
                # connect to last thread (avoid repetition)
                if [self.last_func[tid], func_index] not in self.adjacency_lists[1]:
                    self.adjacency_lists[1].append([self.last_func[tid], func_index])
        self.last_func[tid] = func_index
        self.last_func_sig[tid] = func_sig

        # time feature
        if func_index not in self.index_count.keys():
            self.index_count[func_index] = 1
            self.index_dur[func_index] = te['dur']
        else:
            self.index_count[func_index] += 1
            self.index_dur[func_index] += te['dur']

        # connect to nearby task
        if self.last_task[tid] != "":
            task_feature = self.last_task[tid]
            task_sig = func_sig + '-' + task_feature
            if task_sig not in self.task_arrs[tid]:
                task_index = len(self.node_features)
                vector = self.feature2vector(task_feature)
                self.node_features.append(vector)
                self.adjacency_lists[3].append([func_index, task_index])
                self.task_arrs[tid].append(task_sig)
        self.last_task[tid] = ""
        self.last_task_dur[tid] = 0

    def add_timeline(self, te):
        tid = te['tid']
        feature = te['name']
        if feature == "ResourceSendRequest":
            if 'blob' in te['args']['data']['url']:
                pass
            elif 'js' in te['args']['data']['url']:
                feature = feature+"-js"
            elif 'wasm' in te['args']['data']['url']:
                feature = feature + "-wasm"
            else:
                return
        if feature == "WebSocketCreate":
            self.websocket_create = True
        # connect to last func
        if self.last_func[tid] == -1:
            return
        timeline_sig = self.last_func_sig[tid] + '-' + feature
        if timeline_sig not in self.timeline_arrs[tid]:
            timeline_index = len(self.node_features)
            vector = self.feature2vector(feature)
            self.node_features.append(vector)
            func_index = self.last_func[tid]
            self.adjacency_lists[2].append([func_index, timeline_index])
            self.timeline_arrs[tid].append(timeline_sig)

    def add_task(self, te):
        tid = te['tid']
        feature = te['args']['src_func']
        self.last_task[tid] = feature

    def feature2vector(self, feature):
        vector = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # new
        vector[self.feature_list.index(feature)] = 1
        return vector

    # get function's signature
    def get_func_sig(self, func_info):
        scriptId = self.get_property(func_info, 'scriptId')
        functionName = self.get_property(func_info, 'functionName')
        url = self.get_property(func_info, 'url')
        lineNumber = self.get_property(func_info, 'lineNumber')
        columnNumber = self.get_property(func_info, 'columnNumber')
        func_sig = '-'.join([scriptId, functionName, url, lineNumber, columnNumber])
        return func_sig

    # get value according to the key in properties(dict)
    def get_property(self, properties, key):
        if key in properties.keys():
            return str(properties[key])
        else:
            return 'none'

    def print_graph(self):
        print("** GRAPH FROM TRACE **")
        print("node num:", len(self.node_features))
        print("【node features】:", self.node_features[:8])
        print("【main-thread edge】:", self.adjacency_lists[0][:8])
        print("【sub-thread edge】:", self.adjacency_lists[1][:8])
        print("【timeline edge】:", self.adjacency_lists[2][:8])
        print("【task edge】:", self.adjacency_lists[3][:8])
        print(self.index_count)
        print(self.index_dur)

    def draw_graph(self):
        plt.title(self.file_path.split('/')[-1])
        G = nx.path_graph(len(self.node_features), create_using=nx.OrderedDiGraph)
        pos = nx.spring_layout(G, seed=4)
        x = -1
        # y is from -1 to 1
        # print(max([pos[k][0] for k in pos.keys()]))
        # print(min([pos[k][0] for k in pos.keys()]))
        pos[0] = (-1, pos[0][1] * 1 + 0.2)
        for key in range(len(self.node_features)):
            x += 2 / len(self.node_features)
            if key in [e[1] for e in self.adjacency_lists[0]]:
                pos[key] = (x, pos[key][1] * 1 + 0.2) # main
            elif key in [e[1] for e in self.adjacency_lists[1]]:
                pos[key] = (x, pos[key][1] * 0.3 - 0.5) # sub
            else:
                for E in self.adjacency_lists[2]:
                    if key == E[1]:
                        func = E[0]
                        if func in [e[1] for e in self.adjacency_lists[0]] or func == 0:
                            pos[key] = (x, pos[key][1] * 0.8 + 0.9) # main
                        else:
                            pos[key] = (x, pos[key][1] * 0.3 - 0.9) # sub
                        continue
                for E in self.adjacency_lists[3]:
                    if key == E[1]:
                        func = E[0]
                        if func in [e[1] for e in self.adjacency_lists[0]]:
                            pos[key] = (x, pos[key][1] * 0.8 + 0.9) # main
                        else:
                            pos[key] = (x, pos[key][1] * 0.3 - 0.9) # sub

        node_size = 150
        # node_list = {'Starting':[0]}
        node_list = {}
        color_list = {'Starting':'blue', 'FunctionCall':'blue', 'ResourceSendRequest':'gold',
                       'ResourceSendRequest-js':'green', 'ResourceSendRequest-wasm':'orange', 'WebSocketCreate':'red',
                      'TimerInstall':'grey', 'PostMessageToWorkerGlobalScope':'brown', 'PostMessageToWorkerObject':'purple'}
        for name in self.feature_list:
            node_list[name] = []
        node_list['FunctionCall'].append(0)
        for index in range(len(self.node_features)):
            for name in self.feature_list:
                if self.node_features[index][:-2] == self.feature2vector(name)[:-2]:
                    node_list[name].append(index)
        for name in node_list.keys():
            label_name = name
            if name == "ResourceSendRequest":
                label_name = "ResourceSendRequest-blob"
            nx.draw_networkx_nodes(G, pos, nodelist=node_list[name], node_color=color_list[name], alpha=0.9, node_size=node_size, label=label_name)

        edges1 = []
        edges2 = []
        for edge in self.adjacency_lists[1]:
            if [edge[1], edge[0]] in edges1:
                edges1.remove([edge[1], edge[0]])
                edges2.append([edge[1], edge[0]])
            else:
                edges1.append([edge[0], edge[1]])

        if len(self.node_features)<200:
            nx.draw_networkx_labels(G, pos, font_size= 7, font_color="white", labels={n: str(n) for n in G})
        nx.draw_networkx_edges(G, pos, edgelist=self.adjacency_lists[0], edge_color="black", alpha=0.3, node_size=node_size, width=0.8)
        # nx.draw_networkx_edges(G, pos, edgelist=self.adjacency_lists[1], edge_color="black", alpha=0.6, node_size=node_size, width=0.8, style="--")
        nx.draw_networkx_edges(G, pos, edgelist=edges1, edge_color="black", alpha=0.6,
                               node_size=node_size, width=0.8, style="--")
        nx.draw_networkx_edges(G, pos, edgelist=edges2, edge_color="black", alpha=0.6,
                               node_size=node_size, width=0.8, style="--", arrowstyle="<|-|>")
        nx.draw_networkx_edges(G, pos, edgelist=self.adjacency_lists[2], edge_color="black", alpha=1, node_size=node_size, width=0.8, style="-.")
        nx.draw_networkx_edges(G, pos, edgelist=self.adjacency_lists[3], edge_color="black", alpha=1, node_size=node_size, width=0.8, style=":")

        if len(self.node_features)<20:
            legend1 = plt.legend(loc='lower left', frameon=True, labelspacing=0.1, markerscale=0.6, handletextpad=0.1)
            line1, = plt.plot([1], label="main-thread", color="black", alpha=0.3, linestyle='-', linewidth=0.8)
            line2, = plt.plot([1], label="sub-thread", color="black", alpha=0.6, linestyle='--', linewidth=0.8)
            line3, = plt.plot([1], label="related-action", color="black", alpha=1, linestyle='-.', linewidth=0.8)
            line4, = plt.plot([1], label="related-task", color="black", alpha=1, linestyle=':', linewidth=0.8)
            legend2 = plt.legend(handles=[line1, line2, line3, line4], loc="upper right", frameon=True, labelspacing=0.1, markerscale=1, handletextpad=0.5)
            plt.gca().add_artist(legend1)
            plt.gca().add_artist(legend2)
        plt.show()

if __name__ == '__main__':
    gc = GraphConstructor()
    path = "/Volumes/Common/2022/CryptojackingDetection/MinerLamp/trace/test-sok_known/http%3A%2F%2Fxn--80aafmzgsyhc.com-none/http%3A%2F%2Fxn--80aafmzgsyhc.com-none-trace.json"
    g, w, m = gc.construct(path)
    gc.print_graph()