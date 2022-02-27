# MinerLamp

## Directory

### url

|  file   | source  |
|  ----  | ----  |
| coinblocklist.txt  | https://zerodot1.gitlab.io/CoinBlockerLists/list_browser.txt |
| sok_known.csv  | https://raw.githubusercontent.com/sokcryptojacking/SoK/main/PublicWWW%20Dataset/known_service_provider_domain_list.csv |
| sok_unknown.csv | https://raw.githubusercontent.com/sokcryptojacking/SoK/main/PublicWWW%20Dataset/unknown_service_provider_domain_list.csv |
| top-1m.csv | http://s3.amazonaws.com/alexa-static/top-1m.csv.zip |

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

### filter

```shell script
python extract.py -i sok -o sok
python do_filter.py -i urllist-sok -o sok
```