from skimage import io
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from scipy.stats import moment

globalModel = 0


def classifier_learning():
    path = "D:/Studia/IWM/Oko/"
    image = []
    mask = []
    output = []
    for i in range(1, 7):
        if i < 10:
            image.append(io.imread(path + "images/0" + str(i) + "_h.jpg"))
            mask.append(io.imread(path + "mask/0" + str(i) + "_h_mask.tif", as_gray=True))
            output.append((io.imread(path + "perfect/0" + str(i) + "_h.tif", as_gray=True)))
        else:
            image.append(io.imread(path + "images/" + str(i) + "_h.jpg"))
            mask.append(io.imread(path + "mask/" + str(i) + "_h_mask.tif", as_gray=True))
            output.append((io.imread(path + "perfect/" + str(i) + "_h.tif", as_gray=True)))

    for j in range(1, 7):
        image[j - 1] = image[j - 1][:, :, 1]
    h, w = image[0].shape[0], image[0].shape[1]

    # Size 5x5
    PATCH_SIZE = 5
    HALF_PATCH_SIZE = 2
    LEARN_OFFSET = 2 * PATCH_SIZE

    # Learning phase
    answers = []
    features = []
    nr = -1

    for row in range(0, h - PATCH_SIZE, LEARN_OFFSET):
        for col in range(0, w - PATCH_SIZE, LEARN_OFFSET):
            nr = nr + 1
            if nr > 5:
                nr = 0
            if mask[nr][row + HALF_PATCH_SIZE, col + HALF_PATCH_SIZE] == 0:
                continue
            if output[nr][row + HALF_PATCH_SIZE, col + HALF_PATCH_SIZE] > 0:
                answers.append(1)
            else:
                answers.append(0)
            patch = image[nr][row:(row + PATCH_SIZE), col:(col + PATCH_SIZE)]
            m = moment(patch, [2, 3], axis=None)
            features.append([np.mean(patch), m[0], m[1]])
    X = np.array(features)
    X.shape
    y = np.array(answers)

    param_grid = {
        'n_estimators': [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'max_features': ['auto', 'sqrt', 'log2'],
        'max_depth': [4, 5, 6, 7, 8],
        'criterion': ['gini', 'entropy']
    }

    RFC = RandomForestClassifier(n_estimators=10)
    GSCV = GridSearchCV(estimator=RFC, param_grid=param_grid, cv=5)
    global globalModel
    globalModel = make_pipeline(StandardScaler(), GSCV)
    globalModel.fit(X, y)

    return GSCV.best_estimator_

