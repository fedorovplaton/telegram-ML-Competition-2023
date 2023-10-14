from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble._forest import _accumulate_prediction
from sklearn.utils.validation import check_is_fitted
from sklearn.ensemble._base import _partition_estimators
from sklearn.utils.fixes import _joblib_parallel_args
from joblib import Parallel, delayed
import threading
import numpy as np

X, y = make_classification(
    n_samples=1000,
    n_features=8,
    n_informative=4,
    n_classes=4,
    n_redundant=0,
    random_state=0,
    shuffle=False)


class CustomDecisionTreeClassifier(DecisionTreeClassifier):
    def predict_proba(self, X, check_input=True):
        check_is_fitted(self)
        X = self._validate_X_predict(X, check_input)
        proba = self.tree_.predict(X)

        if self.n_outputs_ == 1:
            proba = proba[:, :self.n_classes_]

            custom_proba = np.zeros_like(proba)
            custom_proba[np.arange(len(proba)), proba.argmax(1)] = 1

            return custom_proba

            # normalizer = proba.sum(axis=1)[:, np.newaxis]
            # normalizer[normalizer == 0.0] = 1.0
            # proba /= normalizer
            #
            # print("normalizer proba", proba)
            # return proba

        else:
            all_proba = []

            for k in range(self.n_outputs_):
                proba_k = proba[:, k, :self.n_classes_[k]]

                normalizer = proba_k.sum(axis=1)[:, np.newaxis]
                normalizer[normalizer == 0.0] = 1.0
                proba_k /= normalizer
                all_proba.append(proba_k)

            return all_proba

class CustomRandomForestClassifier(RandomForestClassifier):
    def __init__(self,
                 n_estimators=100,
                 criterion="gini",
                 max_depth=None,
                 min_samples_split=2,
                 min_samples_leaf=1,
                 min_weight_fraction_leaf=0.,
                 max_features="auto",
                 max_leaf_nodes=None,
                 min_impurity_decrease=0.,
                 min_impurity_split=None,
                 bootstrap=True,
                 oob_score=False,
                 n_jobs=None,
                 random_state=None,
                 verbose=0,
                 warm_start=False,
                 class_weight=None,
                 ccp_alpha=0.0,
                 max_samples=None):
        super(RandomForestClassifier, self).__init__(
            base_estimator=CustomDecisionTreeClassifier(),
            n_estimators=n_estimators,
            estimator_params=("criterion", "max_depth", "min_samples_split",
                              "min_samples_leaf", "min_weight_fraction_leaf",
                              "max_features", "max_leaf_nodes",
                              "min_impurity_decrease", "min_impurity_split",
                              "random_state", "ccp_alpha"),
            bootstrap=bootstrap,
            oob_score=oob_score,
            n_jobs=n_jobs,
            random_state=random_state,
            verbose=verbose,
            warm_start=warm_start,
            class_weight=class_weight,
            max_samples=max_samples)

        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.min_weight_fraction_leaf = min_weight_fraction_leaf
        self.max_features = max_features
        self.max_leaf_nodes = max_leaf_nodes
        self.min_impurity_decrease = min_impurity_decrease
        self.min_impurity_split = min_impurity_split
        self.ccp_alpha = ccp_alpha

# clf = CustomRandomForestClassifier(max_depth=4, random_state=0, n_estimators=8)
# clf.fit(X, y)
#
# result = clf.predict([
#     list(range(0, 8)),
#     list(range(8, 0, -1))
# ])
#
# print(result)
