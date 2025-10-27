import numpy as np
import cv2
from torchvision.datasets import CIFAR10
import torchvision.transforms as transforms

print("Loading CIFAR-10 dataset...")
dataset = CIFAR10(root='../data', train=True, download=True, transform=transforms.ToTensor())
images = dataset.data
labels = np.array(dataset.targets)

# 只用一部分数据加快测试
subset_ratio = 0.1
n_subset = int(subset_ratio * len(images))
indices = np.arange(len(images))
np.random.shuffle(indices)
images = images[indices[:n_subset]]
labels = labels[indices[:n_subset]]

split = int(0.1 * len(images))
query_idx, db_idx = np.arange(split), np.arange(split, len(images))

print(f"Query set: {len(query_idx)} images, Database: {len(db_idx)} images")

def extract_hsv_hist(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h = cv2.calcHist([hsv], [0], None, [30], [0,180])
    s = cv2.calcHist([hsv], [1], None, [32], [0,256])
    v = cv2.calcHist([hsv], [2], None, [32], [0,256])
    feat = np.concatenate([h, s, v]).astype('float32')
    feat /= np.sum(feat) + 1e-6
    return feat

print("Extracting HSV features...")
features = np.array([extract_hsv_hist(img) for img in images], dtype='float32')

def bhattacharyya_batch(f_query, f_db):
    return np.sqrt(1 - np.dot(f_query, f_db.T))

def bhattacharyya(f1, f2):
    return cv2.compareHist(f1, f2, cv2.HISTCMP_BHATTACHARYYA)

K = 10
recalls = []
print("Performing retrieval and computing Recall...")

f_query = features[query_idx]
f_db = features[db_idx]

for cls in range(10):
    q_idx = [i for i in range(len(query_idx)) if labels[query_idx[i]] == cls]
    hits = 0
    for qi in q_idx:
        dists = [bhattacharyya(features[query_idx[qi]], features[di]) for di in db_idx]
        topk = [labels[db_idx[di]] for di in np.argsort(dists)[:K]]
        if cls in topk:
            hits += 1
    recall = hits / len(q_idx)
    recalls.append(recall)
    print(f"Class {cls}: Recall = {recall:.4f}")
print("Mean Recall:", np.mean(recalls))
