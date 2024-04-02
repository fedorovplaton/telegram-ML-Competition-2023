from sklearn.model_selection import StratifiedKFold
from tqdm import tqdm

import numpy as np


def evaluate(pipeline, X, y):
    skf = StratifiedKFold(n_splits=5, random_state=137, shuffle=True)
    metrics = []

    for i, (train_index, test_index) in tqdm(enumerate(skf.split(X, y)), total=5):
        # print(f"Fold {i}:")

        X_train, y_train = X[train_index], y[train_index]
        X_test, y_test = X[test_index], y[test_index]

        pipeline.fit(X_train, y_train)
        fold_accuracy = pipeline.score(X_test, y_test)
        metrics.append(fold_accuracy)

        # print(f'  Accuracy: {fold_accuracy}')

    # print(f"Mean Accuracy: {np.mean(metrics)}")
    return np.mean(metrics)
