import numpy as np
import pandas as pd
from scipy import stats


class BagLearner(object):

    def __init__(self, learner, kwargs={}, bags=20, boost=False, verbose=False): 
        
        self.learners = []
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.kwargs = kwargs
        
        for i in range(bags):
            self.learners.append(learner(**self.kwargs))
        
        
        
    def add_evidence(self, features, labels):
        
        data_size = features.shape[0]
        
        if data_size == 0:
            return
                
        data_index = np.arange(data_size)
        
        for i in range(self.bags):
            
            sampled_index = np.random.choice(data_index, size=data_size, replace=True)
            sampled_features = features[sampled_index]
            sampled_labels = labels[sampled_index]            
            self.learners[i].add_evidence(sampled_features, sampled_labels)
            
    
    def query(self, features):
                
        data_size = features.shape[0]
        if data_size == 0:
            return
        
        pred = np.zeros((self.bags, data_size))
        
        for i in range(self.bags):
            pred[i, :] = self.learners[i].query(features)

        return stats.mode(pred).mode[0] # convert regression learner to use mode rather than mean



# if __name__ == "__main__":
#     print("the secret clue is 'zzyzx'") 
