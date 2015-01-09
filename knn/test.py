import numpy as np
import pickle
from sklearn.metrics import precision_recall_fscore_support

NUM_HEROES = 112
NUM_FEATURES = NUM_HEROES*2

# Import the test x matrix and Y vector
preprocessed = np.load('test_1380.npz')
X = preprocessed['X']
Y = preprocessed['Y']

NUM_MATCHES = len(X)

def my_distance(vec1,vec2):
    return np.sum(np.logical_and(vec1,vec2))

def poly_weights_evaluate(distances):
    '''Returns a list of weights given a polynomial weighting function'''
    # distances = distances[0]
    # weights = (distances * 0.1)
    # weights = weights ** 15
    weights = np.power(np.multiply(distances[0], 0.1), 4)
    return np.array([weights])

def test():
    with open('evaluate_model_10000.pkl', 'rb') as input_file:
            model = pickle.load(input_file)

    correct_predictions = 0
    Y_pred = np.zeros(NUM_MATCHES)
    for i, radiant_query in enumerate(X):
        dire_query = np.concatenate((radiant_query[NUM_HEROES:NUM_FEATURES], radiant_query[0:NUM_HEROES]))
        rad_prob = model.predict_proba(radiant_query)[0][1]
        dire_prob = model.predict_proba(dire_query)[0][0]
        overall_prob = (rad_prob + dire_prob) / 2
        prediction = 1 if (overall_prob > 0.5) else -1
        Y_pred[i] = 1 if prediction == 1 else 0
        result = 1 if prediction == Y[i] else 0
        if i % 100 == 0 :
            print('Predicted: ',prediction)
            print('Result: ',result)
        correct_predictions += result

    accuracy = float(correct_predictions) / NUM_MATCHES
    print('Accuracy of KNN model: %f' % accuracy)

    # flip all -1 true labels to 0 for f1 scoring
    for i, match in enumerate(Y):
        if match == -1:
            Y[i] = 0

    prec, recall, f1, support = precision_recall_fscore_support(Y, Y_pred, average='macro')
    print('Precision: ',prec)
    print('Recall: ',recall)
    print('F1 Score: ',f1)
    print('Support: ',support)

    # Accuracy of KNN model: 0.678074
    # Precision:  0.764119601329
    # Recall:  0.673499267936
    # F1 Score:  0.715953307393
    # Support:  3415

if __name__ == '__main__':
    test()
