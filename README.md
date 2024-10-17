# Instance Detection Challenge
**`2024/06/18`**: **[Object Instance Detection Challenge](https://eval.ai/web/challenges/challenge-page/2277/overview)** was held at [Workshop on Visual Perception and Learning in an Open World, CVPR 2024](https://vplow.github.io/vplow_4th.html)<br>
**`2024/12/08`**: **[1st Object Instance Detection Workshop](https://insdet.github.io)** will be held at [ACCV 2024](https://accv2024.org).<br>

![intro](https://raw.githubusercontent.com/shenqq377/InsDet-Challenge/challenge/templates/objdet-insdet.png)

This github repository is a complimentary resource for the Instance Detection Challenge. From python files and jupyter notebook files we provided, you can see how the challenge dataset is organized, how the evaluation is done, and how the required json file is generated for benchmarking on EvalAI. We also provide detailed comparison between two baselines in [paper](https://proceedings.neurips.cc/paper_files/paper/2023/file/832ea0ff01bd512aab28bf416db9489c-Paper-Datasets_and_Benchmarks.pdf).

## Installation
You may want to install necessary packages. Run `pip install -r requirements.txt` in your python environment. Note that we only tested the code on python >= 3.8.

## Generating the json file for benchmarking
The challenge server at EvalAI requires participants to upload a json or csv file that lists results on the test-set. We also provide examples of `submission.json` and `submission_fasterrcnn_dev.csv`here.

## Question?
Should you have technical questions, please create an issue here. If you have high-level questions, please contact Qianqian Shen (shenqq377@gmail.com) and Yunhan Zhao (yzhao117@gmail.com).
