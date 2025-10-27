import numpy as np
import pytest
import cv2
from app.retrieval import extract_hsv_hist,bhattacharyya

def test_extract_hsv_hist_shape():
    img = np.random.randint(0,256,(32,32,3),dtype=np.uint8)
    feat = extract_hsv_hist(img)
    assert feat.shape[0] == 94

def test_bhattacharyya_distance_nonnegative():
    f1 = np.random.rand(94).astype('float32')
    f2 = np.random.rand(94).astype('float32')
    dist = bhattacharyya(f1, f2)
    assert dist >= 0

def test_retrieval_topk_labels():
    features = [np.random.rand(94).astype('float32') for _ in range(10)]
    labels = np.array([0,1]*5)
    db_idx = list(range(5,10))
    query_idx = list(range(5))
    K = 3
    for qi in query_idx:
        dists = [bhattacharyya(features[qi], features[di]) for di in db_idx]
        topk = [labels[di] for di in np.argsort(dists)[:K]]
        assert len(topk) == K
        for t in topk:
            assert t in labels[db_idx]
