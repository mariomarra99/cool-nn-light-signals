import argparse
import cv2

from detection.yolo import yolov3
from detection.yolo import yolov5n

from classification.hsv_classifier import *
from classification.k_means import * 


#HSV classifier
def hsv_classifier(img):
    #Se semafori verticali, effettuiamo la color classification
    pred = ''
    if len(img) > len(img[0]) :
        #Estimation
        pred_label = estimate_label(standardize_input(img))
        
        #Etichettiamo
        if pred_label == [0,0,1]:
            pred = 'green'
        elif pred_label == [0,1,0]:
            pred = 'yellow'
        elif pred_label == [1,0,0]:
            pred = 'red'
    return pred
    
#K-means clustering
def k_means_clustering(img):
    COLORS = {
    'red': [255,0,0],
    'yellow': [255, 255, 0],
    'green' : [0,128,0],
    'coral' : [255,127,80],
    'light green' : [102,255,178]
    }       
    pred = ''
    if match_image_by_color(img,COLORS['light green'],threshold = 60, number_of_colors=10):
        pred = 'green'
    elif match_image_by_color(img,COLORS['coral'],threshold = 80, number_of_colors=10):
        pred = 'red'
    else:
        pred = 'yellow'
    return pred
        
def traffic_light_detector_classifier(filename,detector,classifier):
    
    img = cv2.imread(filename)
    
    if detector == 'yolov3':
        res = yolov3(img)
    elif detector == 'yolov5n':
        res = yolov5n(img)
    else:
        print('ERROR: invalid detector argument')
        return 
    
    detections = res.xyxy
    detect_list = np.array([])
    print(detections)
    
    occurrency_num = 0
    for detect in detections[0]:
        #legenda struttura array detect
        #0      xmin
        #1      ymin
        #2      xmax
        #3      ymax
        #4      confidence
        #5      class
        #6      name
        
        #consideriamo solo i casi di cui ci fidiamo (confidence > 0.5)
        if int(detect[5]) == 9 and detect[4]>0.5 : 
            occurrency_num += 1
            
            ymin = int(detect[1])
            ymax = int(detect[3])
            xmin = int(detect[0])
            xmax = int(detect[2])
            
            detect_list = np.append(detect_list,[ymin,ymax,xmin,xmax])
            
    detect_list = np.reshape(detect_list,(occurrency_num,4))
    detect_list = sorted(detect_list, key=lambda x: x[2])
        
    print('Detect num: ', occurrency_num)
    print('Detect loc: ', detect_list)
        
    #Se la lista non è vuota
    if len(detect_list) != 0:
        for i in detect_list:
                
            e = i
              
            #slice del semaforo
            det_img = img[int(e[0]):int(e[1]),int(e[2]):int(e[3])]
            if classifier == 'hsv' :
                pred = hsv_classifier(det_img)
            elif classifier =='cluster':
                pred = k_means_clustering(det_img)
            elif classifier == 'dt':
                print('DA IMPLEMENTARE: LAVORI IN CORSO')
            print('Label pred: ', pred)
    else:
        print('Label pred: no traffic light detected')
            
def main():
    parser = argparse.ArgumentParser(description="Traffic light detector + classifier args")
    parser.add_argument("filename", type=str, help="image location")
    parser.add_argument("detector", type=str, help="detector name: <yolov3,yolov5n>")
    parser.add_argument("classifier", type=str, help="classifier name: <hsv,cluster,dt>")
    args = parser.parse_args()
    traffic_light_detector_classifier(args.filename,args.detector,args.classifier)
        
main()
