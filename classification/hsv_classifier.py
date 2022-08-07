import cv2
import numpy as np
import matplotlib.pyplot as plt

def standardize_input(image):
    
    ## TODO: Resize image and pre-process so that all "standard" images are the same size  
    standard_im = np.copy(image)
    standard_im = cv2.resize(standard_im,(32,32))
    
    return standard_im

## TODO: One hot encode an image label
## Given a label - "red", "green", or "yellow" - return a one-hot encoded label

# Examples: 
# one_hot_encode("red") should return: [1, 0, 0]
# one_hot_encode("yellow") should return: [0, 1, 0]
# one_hot_encode("green") should return: [0, 0, 1]

def one_hot_encode(label):
    
    ## TODO: Create a one-hot encoded label that works for all classes of traffic lights
    one_hot_encoded = [0, 0, 0]
    if(label == 'red'):
        one_hot_encoded[0] = 1
    elif(label == 'yellow'):
        one_hot_encoded[1] = 1
    else:
        one_hot_encoded[2] = 1
    
    return one_hot_encoded

def standardize(image_list):
    
    # Empty image data array
    standard_list = []

    # Iterate through all the image-label pairs
    for item in image_list:
        image = item[0]
        label = item[1]

        # Standardize the image
        standardized_im = standardize_input(image)


        # One-hot encode the label
        one_hot_label = one_hot_encode(label)    

        # Append the image, and it's one hot encoded label to the full, processed list of image data 
        standard_list.append((standardized_im, one_hot_label))
        
    return standard_list

## TODO: Create a brightness feature that takes in an RGB image and outputs 
## a feature vector and/or value
## This feature should use HSV colorspace values
def create_feature(rgb_image):
    
    feature = []
    sliced_image=np.copy(rgb_image)
    
    upper_part = sliced_image[3:12, 5:27, :]
    mid_part = sliced_image[12:21, 5:27, :]
    lower_part = sliced_image[21:30, 5:27, :]
    
    hsv_upper = cv2.cvtColor(upper_part, cv2.COLOR_RGB2HSV)
    hsv_mid = cv2.cvtColor(mid_part, cv2.COLOR_RGB2HSV)
    hsv_lower = cv2.cvtColor(lower_part, cv2.COLOR_RGB2HSV)

    sum_brightness_upper = np.sum(hsv_upper[:,:,2])
    sum_brightness_mid = np.sum(hsv_mid[:,:,2])
    sum_brightness_lower = np.sum(hsv_lower[:,:,2])
    
    feature = [sum_brightness_upper, sum_brightness_mid, sum_brightness_lower]
    return feature, upper_part, mid_part, lower_part

def estimate_label(rgb_image):
    
    ## TODO: Extract feature(s) from the RGB image and use those features to
    ## classify the image and output a one-hot encoded label
    predicted_label = [0, 0, 0]
    feature = create_feature(rgb_image)
    
    predicted_label[np.argmax(feature[0])] = 1
    
    pred_img = feature[1:][np.argmax(feature[0])]
    #plt.imshow(pred_img)
    #plt.show()

    return predicted_label