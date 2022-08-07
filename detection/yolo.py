from unittest import result
import torch

def yolov3(img):
    model = torch.hub.load('ultralytics/yolov3', 'yolov3')
    results = model(img)
    return results

def yolov5n(img):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5n')
    results = model(img)
    return results