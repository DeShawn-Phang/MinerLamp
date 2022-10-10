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
| Dataset 1 |  [Download](https://drive.google.com/drive/folders/1BU3o1ZJOv2CQZDxFkRh9wwztaSHePxBT?usp=sharing) |
| Dataset 2 |  [Download](https://drive.google.com/drive/folders/1BU3o1ZJOv2CQZDxFkRh9wwztaSHePxBT?usp=sharing) |
| Dataset 3 Part1 |  [Download](https://drive.google.com/drive/folders/1BU3o1ZJOv2CQZDxFkRh9wwztaSHePxBT?usp=sharing) |
| Dataset 3 Part2 |  [Download](https://drive.google.com/drive/folders/10z3wdew4ls776NOWf2Lp_wWBK6qqWEMA?usp=sharing) |


## Directory

### url

| DataSet |  file   | source  |
|  ----  |  ----  | ----  |
| Dataset 1 | coinblocklist.txt  | [Download](https://zerodot1.gitlab.io/CoinBlockerLists/list_browser.txt) |
| Dataset 2 | sok_known.csv  | [Download](https://raw.githubusercontent.com/sokcryptojacking/SoK/main/PublicWWW%20Dataset/known_service_provider_domain_list.csv) |
| Dataset 2 | sok_unknown.csv | [Download](https://raw.githubusercontent.com/sokcryptojacking/SoK/main/PublicWWW%20Dataset/unknown_service_provider_domain_list.csv) |
| Dataset 3 | top-1m.csv | [Download](http://s3.amazonaws.com/alexa-static/top-1m.csv.zip) |


### trace

```shell script
usage: get_trace.py [-h] [-m MODE] -l CSV/TXT -o DIR [-b NUMBER] [-e NUMBER]
                    [-a] [-c] [-n DOCKER_NAME] [-p PORT]
example: python get_trace.py -m test -l ../url/top-1m.csv -o alexa0_5 -b 0 -e 5 -a -c
```

### graph

```shell script
usage: get_graph.py [-h] [-m {train,test}] -d DIR -o DIRNAME
example: python get_graph.py -m test -d ../trace/alexa0_5 -o alexa0_5
```

### classifier

```shell script
usage: predict.py trained_model/RGIN_MODEL.hdf5 INPUT_DIR
example: python predict.py trained_model/RGIN_GraphBinaryClassification__2022-02-15_18-07-18_best.hdf5 ../../../graph/alexa0_5/
```

