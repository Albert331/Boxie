import cv2
import numpy as np
import onnxruntime as ort


session = ort.InferenceSession(
    "yolo26n-pose.onnx",
    providers=["CPUExecutionProvider"]
)
input_name = session.get_inputs()[0].name
print(session.get_providers())

IMG_SIZE = 416
CONF_THRESHOLD = 0.7

def preprocess(frame):
    h, w = frame.shape[:2]
    img = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.transpose(2, 0, 1).astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    scale_x, scale_y = w / IMG_SIZE, h / IMG_SIZE
    return img, scale_x, scale_y

def run_inference(frame):
    input_tensor, scale_x, scale_y = preprocess(frame)
    outputs = session.run(None, {input_name: input_tensor})
    detections = outputs[0][0]  

    people = []
    for det in detections:
        conf = det[4]
        if conf < CONF_THRESHOLD:
            continue 

        keypoints_raw = det[6:]              
        keypoints = keypoints_raw.reshape(17, 3)   

        
        keypoints_scaled = keypoints.copy()
        keypoints_scaled[:, 0] *= scale_x
        keypoints_scaled[:, 1] *= scale_y

        people.append(keypoints_scaled)   

    return people


import time

def run_inference_timed(frame):
    t0 = time.time()
    input_tensor, scale_x, scale_y = preprocess(frame)
    t1 = time.time()

    outputs = session.run(None, {input_name: input_tensor})
    t2 = time.time()

    detections = outputs[0][0]
    people = []
    for det in detections:
        conf = det[4]
        if conf < CONF_THRESHOLD:
            continue
        keypoints_raw = det[6:]
        keypoints = keypoints_raw.reshape(17, 3)
        keypoints_scaled = keypoints.copy()
        keypoints_scaled[:, 0] *= scale_x
        keypoints_scaled[:, 1] *= scale_y
        people.append(keypoints_scaled)
    t3 = time.time()

    print(f"preprocess: {(t1-t0)*1000:.1f}ms | inference: {(t2-t1)*1000:.1f}ms | decode: {(t3-t2)*1000:.1f}ms | total: {(t3-t0)*1000:.1f}ms")
    return people

