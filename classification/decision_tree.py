from sklearn.tree import DecisionTreeClassifier
import pickle

def dt_prediction(img):
    # load the pre-trained model from my google colab
    filename = 'pre_trained_dt.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    clf_en = pickle.load(open(filename, 'rb'))
    
    y_pred_en = clf_en.predict([img])
    return y_pred_en