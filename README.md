# Instance Detection Challenge
Workshop Webpage<br>
EvalAI Challenge Server<br>

![intro](https://raw.githubusercontent.com/shenqq377/InsDet_Challenge/challenge/templates/objdet-insdet.png)

This github repository is a complimentary resource for the Instance Detection Challenge. From python files we provided, you can see how the challenge dataset is organized, how the evaluation is done, and how the required json file is generated for benchmarking on EvalAI. We provide jupyter notebook files to demonstrate comparison between two baselines in [paper](https://github.com/insdet/instance-detection).

## Installation
You may want to install necessary packages. Run `pip install -r requirements.txt` in your python environment. Note that we only tested the code on python >= 3.8.

**Note**: `pascal2coco.py` and `pascal2coco4CPL.py` are used to convert all XML files to a single JSON file, to ensure a COCO compatible format.

## Evaluation
You should be able to run the following command line to evaluate.

## Generating the json file for benchmarking
The challenge server at EvalAI requires participants to upload a json file that lists results on the test-set.

## Question?
Should you have technical questions, please create an issue here.
