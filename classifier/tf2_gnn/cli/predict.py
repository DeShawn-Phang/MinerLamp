#!/usr/bin/env python3
import os
import sys
from typing import Callable

import tensorflow as tf
from dpu_utils.utils import run_and_debug, RichPath

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from tf2_gnn import DataFold, GraphDataset, GraphTaskModel
from tf2_gnn.cli_utils.training_utils import get_model_and_dataset


def test(
    model: GraphTaskModel,
    dataset: GraphDataset,
    log_fun: Callable[[str], None],
    data_path: str,
    quiet: bool = False,
):
    log_fun("== Running on test dataset")
    test_data = dataset.get_tensorflow_dataset(DataFold.TEST)
    test_results = model.predict(test_data)
    # _, _, test_results = model.run_one_epoch(test_data, training=False, quiet=quiet)
    # test_metric, test_metric_string = model.compute_epoch_metrics(test_results)
    # log_fun(test_metric_string)

    import numpy as np
    import csv
    test_results = test_results.numpy()
    predict_float = list(test_results.tolist())
    predict = list(np.around(test_results).tolist())
    log_fun(str(predict))

    file_name = []
    with open(data_path + "/list.txt") as f:
        for line in f.readlines():
            file_name.append(line[:-1])

    print(len(file_name))
    print(len(predict))
    if(len(file_name)==len(predict)):
        print("length matched, write result to csv.")
    else:
        print("length not matched, please check!")

    with open(data_path + "/minerlamp_predict.csv", 'w') as f:
        w = csv.writer(f)
        i = 0
        while(i<len(predict)):
            print(file_name[i],int(predict[i]),predict_float[i])
            w.writerow([file_name[i],int(predict[i]),predict_float[i]])
            i+=1


def run_from_args(args) -> None:
    data_path = RichPath.create(args.DATA_PATH, args.azure_info)
    dataset, model = get_model_and_dataset(
        msg_passing_implementation=None,
        task_name=None,
        data_path=data_path,
        trained_model_file=args.TRAINED_MODEL,
        cli_data_hyperparameter_overrides=args.data_param_override,
        cli_model_hyperparameter_overrides=args.model_param_override,
        folds_to_load={DataFold.TEST},
    )
    test(model, dataset, lambda msg: print(msg), args.DATA_PATH, quiet=args.quiet)


def run():
    import argparse

    parser = argparse.ArgumentParser(description="Test a GNN model.")
    parser.add_argument(
        "TRAINED_MODEL",
        type=str,
        help="File to load model from (determines model architecture & task).",
    )
    parser.add_argument("DATA_PATH", type=str, help="Directory containing the task data.")
    parser.add_argument(
        "--model-params-override",
        dest="model_param_override",
        type=str,
        help="JSON dictionary overriding model hyperparameter values.",
    )
    parser.add_argument(
        "--data-params-override",
        dest="data_param_override",
        type=str,
        help="JSON dictionary overriding data hyperparameter values.",
    )
    parser.add_argument(
        "--azure-info",
        dest="azure_info",
        type=str,
        default="azure_auth.json",
        help="Azure authentication information file (JSON).",
    )
    parser.add_argument(
        "--quiet", dest="quiet", action="store_true", help="Generate less output during testing.",
    )
    parser.add_argument("--debug", dest="debug", action="store_true", help="Enable debug routines")
    args = parser.parse_args()

    # Shut up tensorflow:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
    tf.get_logger().setLevel("ERROR")
    import warnings
    warnings.simplefilter("ignore")

    run_and_debug(lambda: run_from_args(args), args.debug)


if __name__ == "__main__":
    run()