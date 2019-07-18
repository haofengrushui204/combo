# -*- coding: utf-8 -*-
"""Example of combining multiple base classifiers. Two combination
frameworks are demonstrated:

1. Average: take the average of all base detectors
2. maximization : take the maximum score across all detectors as the score

"""
# Author: Yue Zhao <zhaoy@cmu.edu>
# License: BSD 2 clause


import os
import sys

# temporary solution for relative imports in case combo is not installed
# if combo is installed, no need to use the following line
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname("__file__"), '..')))

import numpy as np

from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import AgglomerativeClustering

from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler

from combo.models.cluster_comb import clusterer_ensemble_scores
from combo.models.cluster_comb import ClustererEnsemble
from combo.utils.utility import generate_bagging_indices

import warnings

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    # Define data file and read X and y
    random_state = 42
    X, y = load_breast_cancer(return_X_y=True)

    n_clusters = 5
    n_estimators = 3
    
    # Initialize a set of estimators
    estimators = [KMeans(n_clusters=n_clusters),
                  MiniBatchKMeans(n_clusters=n_clusters),
                  AgglomerativeClustering(n_clusters=n_clusters)]

    clf = ClustererEnsemble(estimators, n_clusters=n_clusters)
    clf.fit(X)
    predicted_labels = clf.labels_
    aligned_labels = clf.aligned_labels_
    
    # Clusterer Ensemble without ininializing a new Class
    original_labels = np.zeros([X.shape[0], n_estimators])
    
    for i, estimator in enumerate(estimators):
        estimator.fit(X)
        original_labels[:, i] = estimator.labels_
        
    # Invoke method directly without initialiing a new Class
    labels_by_vote1 = clusterer_ensemble_scores(original_labels, n_estimators,
                                                n_clusters)
    labels_by_vote2, aligned_labels = clusterer_ensemble_scores(
        original_labels, n_estimators, n_clusters, return_results=True)

    labels_by_vote3 = clusterer_ensemble_scores(original_labels, n_estimators,
                                                n_clusters, reference_idx=1)
