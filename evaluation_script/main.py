import csv
import random
import pickle
import json
import sys
import numpy as np
from .cocoapi.PythonAPI.pycocotools.coco import COCO
from .cocoapi.PythonAPI.pycocotools.cocoeval import COCOeval


def get_precisions(gt_file, result_file, metric="bbox"):
    """plot precision-recall curve based on testing results of json file.
    Args:
        gt_file: dict of ground-truth.
        result_file: dict of testing results.
        iou: list [0.5:0.05:0.95]
        metric: Metrics to be evaluated. Options are 'bbox', 'segm'.
    """
    # load ground-truth
    coco_gt = COCO(annotation_file=gt_file)

    # load testing results
    coco_dt = coco_gt.loadRes(result_file)

    # initialize COCOeval instance
    coco_eval = COCOeval(coco_gt, coco_dt, metric)
    coco_eval.evaluate()
    coco_eval.accumulate()
    coco_eval.summarize()

    # extract eval data
    res = coco_eval.stats
    
    return res

def csv2json4gt(csv_file):
    
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        csv_data = [row for row in reader]

    info = []
    licenses = []
    NumToImage = {}
    NumToCat = {}
    annotations = []

    for row in csv_data:
        data = {k.split(".")[0]:{} for k in row.keys()}
        for k,v in row.items():
            data[k.split(".")[0]][k.split(".")[-1]] = v
    
        info = data["info"]
        licenses = data["licenses"]
    
        images = {}
        for k,v in data["images"].items():
            if (k == "license") or (k == "height") or (k == "width") or (k == "id"):
                images[k] = int(v)
            else:
                images[k] = v            
        NumToImage[data["images"]["id"]] = images
    
        cats = {}
        for k,v in data["categories"].items():
            if k == 'id':
                cats[k] = int(v)
            else:
                cats[k] = v    
        NumToCat[data["categories"]["id"]] = cats

        annotations.append({k: eval(v) for k,v in data["annotations"].items()})

    json_data = {'info': info, 
                 'licenses': [licenses],
                 'images': [v for k,v in NumToImage.items()],
                 'annotations': annotations,
                 'categories': [v for k,v in NumToCat.items()]}
    
    return json_data 

def read_json(gt_file, res_file):
    """
    Read json file and separate easy/hard sub-dict
    """
    
    if 'json' in gt_file:
        gt_dic = json.load(open(gt_file, 'r'))
    elif 'csv' in gt_file:
        gt_dic = csv2json4gt(gt_file)
    else:
        sys.exit()
    
    tag = {'easy':[], 'hard':[]}
    for dic in gt_dic['images']:
        if 'easy' in dic['file_name']:
            tag['easy'].append(dic['id'])
        elif 'hard' in dic['file_name']:
            tag['hard'].append(dic['id'])
        else:
            continue
    
    gt_easy = {'info':gt_dic['info'],
               'licenses':gt_dic['licenses'],
               'images':[d for d in gt_dic['images'] if d['id'] in tag['easy']],
               'annotations':[d for d in gt_dic['annotations'] if d['image_id'] in tag['easy']],
               'categories':gt_dic['categories']}

    gt_hard = {'info':gt_dic['info'], 
               'licenses':gt_dic['licenses'],
               'images':[d for d in gt_dic['images'] if d['id'] in tag['hard']],
               'annotations':[d for d in gt_dic['annotations'] if d['image_id'] in tag['hard']],
               'categories':gt_dic['categories']}
    
    if 'json' in res_file:
        res_dic = json.load(open(res_file, 'r'))
    elif 'csv' in res_file:
        res_dic = []
        with open(res_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                for k,v in row.items():
                    row[k] = eval(v)
                res_dic.append(row)
    else:
        sys.exit()
    
    res_easy = [d for d in res_dic if d['image_id'] in tag['easy']]
    res_hard = [d for d in res_dic if d['image_id'] in tag['hard']]
    
    return gt_dic, gt_easy, gt_hard, res_dic, res_easy, res_hard
    

def evaluate(test_annotation_file, user_submission_file, phase_codename, **kwargs):
    print("Starting Evaluation.....")
    print("Submission related metadata:")
    """
    Evaluates the submission for a particular challenge phase adn returns score
    Arguments:

        `test_annotations_file`: Path to test_annotation_file on the server
        `user_submission_file`: Path to file submitted by the user
        `phase_codename`: Phase to which submission is made

        `**kwargs`: keyword arguments that contains additional submission
        metadata that challenge hosts can use to send slack notification.
        You can access the submission metadata
        with kwargs['submission_metadata']

        Example: A sample submission metadata can be accessed like this:
        >>> print(kwargs['submission_metadata'])
        {
            "status": u"running",
            "when_made_public": None,
            "participant_team": 5,
            "input_file": "https://abc.xyz/path/to/submission/file.json",
            "execution_time": u"123",
            "publication_url": u"ABC",
            "challenge_phase": 1,
            "created_by": u"ABC",
            "stdout_file": "https://abc.xyz/path/to/stdout/file.json",
            "method_name": u"Test",
            "stderr_file": "https://abc.xyz/path/to/stderr/file.json",
            "participant_team_name": u"Test Team",
            "project_url": u"http://foo.bar",
            "method_description": u"ABC",
            "is_public": False,
            "submission_result_file": "https://abc.xyz/path/result/file.json",
            "id": 123,
            "submitted_at": u"2017-03-20T19:22:03.880652Z",
        }
    """
    print(kwargs["submission_metadata"])
    output = {}
    if phase_codename == "dev":
        print("Evaluating for Dev Phase")
        
        gt_dic, gt_easy, gt_hard, submission_dic, submission_easy, submission_hard = read_json(test_annotation_file, user_submission_file)
        
        res = get_precisions(gt_dic, submission_dic) # all 160 imgs
        res_easy = get_precisions(gt_easy, submission_easy)# easy scenes
        res_hard = get_precisions(gt_hard, submission_hard)# hard scenes
        
        output["result"] = [
            {
                "val_split":{
                    "AP": res[0]*100,
                    "AP50": res[1]*100,
                    "AP75": res[2]*100,
                    "AP_easy": res_easy[0]*100,
                    "AP_hard": res_hard[0]*100,
                    "AP_small": res[3]*100,
                    "AP_medium": res[4]*100,
                    "AP_large": res[5]*100,
                    "AR_1": res[6]*100,
                    "AR_10": res[7]*100,
                    "AR_100": res[8]*100,
                    "AR_small": res[9]*100,
                    "AR_medium": res[10]*100,
                    "AR_large": res[11]*100,
                }
            }
        ]

        # To display the results in the result file
        output["submission_result"] = output["result"][0]["val_split"]
        print("Completed evaluation for Dev Phase")
    elif phase_codename == "test":
        print("Evaluating for Test Phase")
        
        gt_dic, gt_easy, gt_hard, submission_dic, submission_easy, submission_hard = read_json(test_annotation_file, user_submission_file)
        
        res = get_precisions(gt_dic, submission_dic) # all imgs
        res_easy = get_precisions(gt_easy, submission_easy)# easy scenes
        res_hard = get_precisions(gt_hard, submission_hard)# hard scenes
        
        output["result"] = [
            {
                "test_split":{
                    "AP": res[0]*100,
                    "AP50": res[1]*100,
                    "AP75": res[2]*100,
                    "AP_easy": res_easy[0]*100,
                    "AP_hard": res_hard[0]*100,
                    "AP_small": res[3]*100,
                    "AP_medium": res[4]*100,
                    "AP_large": res[5]*100,
                    "AR_1": res[6]*100,
                    "AR_10": res[7]*100,
                    "AR_100": res[8]*100,
                    "AR_small": res[9]*100,
                    "AR_medium": res[10]*100,
                    "AR_large": res[11]*100,
                }
            }
        ]
        # To display the results in the result file
        output["submission_result"] = output["result"][0]["test_split"]
        print("Completed evaluation for Test Phase")
    return output
