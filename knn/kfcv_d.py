from sklearn.neighbors import KNeighborsClassifier
from sklearn import cross_validation
import numpy as np

def my_distance(vec1,vec2):
    #return np.sum(np.multiply(vec1,vec2))
    return np.sum(np.logical_and(vec1,vec2))

def poly_param(d):
    def poly_weights(distances):
        '''Returns a list of weights given a polynomial weighting function'''
        weights = np.power(np.multiply(distances[0], 0.1), d)
        return np.array([weights])
    return poly_weights

def score(estimator, X, y):
    correct_predictions = 0
    for i, radiant_query in enumerate(X):
        dire_query = np.concatenate((radiant_query[NUM_HEROES:NUM_FEATURES], radiant_query[0:NUM_HEROES]))
        rad_prob = estimator.predict_proba(radiant_query)[0][1]
        dire_prob = estimator.predict_proba(dire_query)[0][0]
        overall_prob = (rad_prob + dire_prob) / 2
        prediction = 1 if (overall_prob > 0.5) else -1
        result = 1 if prediction == y[i] else 0
        correct_predictions += result
    accuracy = float(correct_predictions) / len(X)
    print('Accuracy: %f' % accuracy)
    return accuracy

NUM_HEROES = 112
NUM_FEATURES = NUM_HEROES*2
K = 2

# Import the preprocessed X matrix and Y vector
preprocessed = np.load('train_12420.npz')
X = preprocessed['X']
Y = preprocessed['Y']

NUM_MATCHES = 10000
X = X[0:NUM_MATCHES]
Y = Y[0:NUM_MATCHES]

print('Training using data from %d matches...' % NUM_MATCHES)

k_fold = cross_validation.KFold(n=NUM_MATCHES, n_folds=K, indices=True)

d_tries = [3, 4, 5]

d_accuracy_pairs = []
for d_index, d in enumerate(d_tries):
    model = KNeighborsClassifier(n_neighbors=NUM_MATCHES/K,metric=my_distance,weights=poly_param(d))
    model_accuracies = cross_validation.cross_val_score(model, X, Y, scoring=score, cv=k_fold)
    model_accuracy = model_accuracies.mean()
    d_accuracy_pairs.append((d, model_accuracy))
print(d_accuracy_pairs)
