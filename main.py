import argparse
import cv2

from detection.yolo import yolov3
from detection.yolo import yolov5n

from classification.hsv_classifier import *

def main():
    
    def traffic_light_detector_classifier(filename):
    
        img = cv2.imread(filename)
        res = yolov3(img)
        
        detections = res.xyxy
        detect_list = np.array([])

        occurrency_num = 0
        for i,detect in enumerate(detections[0]):
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
        print('Detect loc: ', detect_list)
        
        #Se la lista non è vuota
        if len(detect_list) != 0:
            
            for i in range(0,len(detect_list)):

              e = detect_list[i]
              
              #slice del semaforo
              det_img = img[int(e[0]):int(e[1]),int(e[2]):int(e[3])]
              #Se semafori verticali, effettuiamo la color classification
              if len(det_img) > len(det_img[0]) :
                
                #HSV classification
                pred_label = estimate_label(standardize_input(det_img))

                pred = ''

                #Etichettiamo
                if pred_label == [0,0,1]:
                  pred = 'green'
                elif pred_label == [0,1,0]:
                  pred = 'yellow'
                elif pred_label == [1,0,0]:
                  pred = 'red'

                print('Label pred: ', pred)
        else:
            print('Label pred: null')
            
    parser = argparse.ArgumentParser(description="Traffic light detector + classifier")
    parser.add_argument("filename", type=str, help="file location")
    args = parser.parse_args()
    traffic_light_detector_classifier(args.filename)
        
main()
