import torch
import pickle
import importlib
import numpy as np
from utils.torch_utils import select_device
from utils.datasets import letterbox
from utils.general import non_max_suppression, scale_coords
from .experimental import attempt_load

# Initialize device and other parameters
device = ''
classes = 0
agnostic_nms = False
conf_thres = 0.85
iou_thres = 0.45
augment = False
imgsz = 640
weights = 'static/weights/best.pt'

# Select the computation device
device = select_device(device)
half = device.type != 'cpu'  # half precision only supported on CUDA

# Load the model
model = attempt_load(weights, map_location=device)  # load FP32 model

# Get model names
names = model.module.names if hasattr(model, 'module') else model.names

def detect(img0):
    """
    Perform detection on an image.

    Args:
    img0 (numpy array): The original image.

    Returns:
    tuple: Bounding box coordinates and confidence score.
    """
    conf = ''
    box = ()
    half = device.type != 'cpu'  # half precision only supported on CUDA
    stride = int(model.stride.max())  # model stride

    # Convert model to half precision if possible
    if half:
        model.half()  # to FP16

    # Run a dummy input through the model once if using CUDA
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))

    # Preprocess the image
    img = letterbox(img0, 640, stride=stride)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.half() if half else img.float()  # uint8 to fp16/32
    img /= 255.0  # Normalize to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # Run the model inference
    pred = model(img, augment=augment)[0]

    # Apply Non-Maximum Suppression (NMS)
    pred = non_max_suppression(pred, conf_thres, iou_thres, classes=classes, agnostic=agnostic_nms)

    # Process detections
    for i, det in enumerate(pred):  # detections per image
        if len(det):
            # Rescale boxes from img size to original img0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()
            
            # Extract bounding box coordinates and confidence
            for *xyxy, conf, cls in det:
                x1 = int(xyxy[0].item())
                y1 = int(xyxy[1].item())
                x2 = int(xyxy[2].item())
                y2 = int(xyxy[3].item())
                box = (x1, y1, x2, y2)
    
    return box, conf
