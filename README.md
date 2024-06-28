<div align="center">
 <img src="res/WebMinerLamp.jpg">
</div>
<p align="center">
  <i>One tool for detecting in-browser Cryptojacking.</i>
</p>


# MinerLamp

## Data Set

- Dataset 1 contains 1310 samples from CoinBlockerLists.
- Dataset 2 contains 4748 samples from Tekiner et al.
- Dataset 3 contains 15899 samples from the top 30,000 to 50,000 in Alexa-Top-1M.

We collect data before January 15, 2022, as datasets.

### Test data

Trace data can be downloaded from the links below.

| DataSet | Link  |
|  ----  | ----  |
| Dataset 1 (test-coinblocklist.zip)|  [Download](https://drive.google.com/drive/folders/1BU3o1ZJOv2CQZDxFkRh9wwztaSHePxBT?usp=sharing) |
| Dataset 2 (test-sok.zip)|  [Download](https://drive.google.com/drive/folders/1BU3o1ZJOv2CQZDxFkRh9wwztaSHePxBT?usp=sharing) |
| Dataset 3 Part1 (alexa.zip, alexa.z01) |  [Download](https://drive.google.com/drive/folders/1BU3o1ZJOv2CQZDxFkRh9wwztaSHePxBT?usp=sharing) |
| Dataset 3 Part2 (alexa.z02, alexa.z03) |  [Download](https://drive.google.com/drive/folders/10z3wdew4ls776NOWf2Lp_wWBK6qqWEMA?usp=sharing) |

**Note:** Dataset 3 (alexa.zip, alexa.z01, alexa.z02, and alexa.z03) contains four files, you have to download them all before unzipping.

### Obfuscated data sets


| Sample          | JS or Wasm | Lable | URL                                                                  | 
|-----------------|------------|-------|----------------------------------------------------------------------|
| 2048            | Wasm       | 0     | https://github.com/inishchith/2048.wasm/tree/main                    |
| Breakout        | Wasm       | 0     | https://github.com/vtan/breakout-wasm/tree/main                      |
| Circle Collide  | Wasm       | 0     | https://github.com/TurkeyMcMac/circle-collide                        |
| Dave            | Wasm       | 0     | https://github.com/shlomnissan/dave-wasm                             |
| Interplanetary  | Wasm       | 0     | https://github.com/s-macke/Interplanetary-Postal-Service/tree/master |
| Asteroids       | Wasm       | 0     | https://github.com/robertaboukhalil/wasm-asteroids                   |
| Snake           | Wasm       | 0     | https://github.com/tsoding/snake-c-wasm                              |
| Tetris          | Wasm       | 0     | https://github.com/olzhasar/sdl-tetris                               |
| OpenGL          | Wasm       | 0     | https://github.com/timhutton/opengl-canvas-wasm                      |
| BF Interpreter  | Wasm       | 0     | https://github.com/pablojorge/brainfuck                              |
| Conway Life     | Wasm       | 0     | https://github.com/iximiuz/golife.c                                  |
| Markdown Parser | Wasm       | 0     | https://github.com/rsms/markdown-wasm/tree/master                    |
| Garliccoin      | Wasm       | 1     | https://github.com/AnanthVivekanand/garlicoinhash-wasm               |
| xmr-wasm        | Wasm       | 1     | https://github.com/jtgrassie/xmr-wasm                                |
| deepMiner       | Wasm       | 1     | https://github.com/deepwn/deepMiner                                  |
| webminerpool    | Wasm       | 1     | https://github.com/notgiven688/webminerpool                          |
| 2048            | JS         | 0     | https://github.com/kubowania/2048                                    |
| Tetris          | JS         | 0     | https://github.com/melcor76/js-tetris                                |
| Breakout        | JS         | 0     | https://github.com/city41/breakouts                                  |
| Fruit Ninja     | JS         | 0     | https://github.com/yeesunday/WebFruitNinja                           |
| Astray          | JS         | 0     | https://github.com/wwwtyro/Astray                                    |
| Markdown Parser | JS         | 0     | https://github.com/LeoYuan/markdown-editor                           |
| BF Interpreter  | JS         | 0     | https://github.com/kcal2845/bf_js                                    |
| Conway Life     | JS         | 0     | https://github.com/cwilso/conway                                     |
| Calculator      | JS         | 0     | https://github.com/LucioFex/Simple-Web-Calculator                    |
| CyberChef       | JS         | 0     | https://github.com/gchq/CyberChef                                    |
| Crypto-Webminer | JS         | 1     | https://github.com/PiTi2k5/Crypto-Webminer                           |
| WebMinePool     | JS         | 1     | https://www.webminepool.com/                                         |
| Crypto-Loot     | JS         | 1     | https://crypto-loot.org/                                             |
| Monero Webminer | JS         | 1     | https://github.com/NajmAjmal/monero-webminer/tree/main               |
| BrowserMine     | JS         | 1     | https://cp.browsermine.com/                                          |


## Directory

### data_lable

This folder stores the labels for each dataset. The `all_positive.csv` file stores all positive samples.

### url
This folder contains the url of the dataset website.

| DataSet |  file   | source  |
|  ----  |  ----  | ----  |
| Dataset 1 | coinblocklist.txt  | [Download](https://zerodot1.gitlab.io/CoinBlockerLists/list_browser.txt) |
| Dataset 2 | sok_known.csv  | [Download](https://raw.githubusercontent.com/sokcryptojacking/SoK/main/PublicWWW%20Dataset/known_service_provider_domain_list.csv) |
| Dataset 2 | sok_unknown.csv | [Download](https://raw.githubusercontent.com/sokcryptojacking/SoK/main/PublicWWW%20Dataset/unknown_service_provider_domain_list.csv) |
| Dataset 3 | top-1m.csv | [Download](http://s3.amazonaws.com/alexa-static/top-1m.csv.zip) |


### trace
This folder contains a tool to get website trace.

```shell script
usage: get_trace.py [-h] [-m MODE] -l CSV/TXT -o DIR [-b NUMBER] [-e NUMBER]
                    [-a] [-c] [-n DOCKER_NAME] [-p PORT]
example: python get_trace.py -m test -l ../url/top-1m.csv -o alexa0_5 -b 0 -e 5 -a -c
```

### graph
This folder contains a tool that converts website trace to the graph.

```shell script
usage: get_graph.py [-h] [-m {train,test}] -d DIR -o DIRNAME
example: python get_graph.py -m test -d ../trace/alexa0_5 -o alexa0_5
```

### training_data
This folder stores the training data for the model.

- `train.jsonl.gz` file is the training set.
- `valid.jsonl.gz` file is the validation set.

### classifier
This folder contains MinerLamp's classifiers.

```shell script
usage: predict.py trained_model/RGIN_MODEL.hdf5 INPUT_DIR
example: python predict.py trained_model/RGIN_GraphBinaryClassification__2022-02-15_18-07-18_best.hdf5 ../../../graph/alexa0_5/
```

