import numpy as np
import pandas as pd
from scipy import stats
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
class RTLearner(object):  		  	   		     		  		  		    	 		 		   		 		  
 		  	   		     		  		  		    	 		 		   		 		  		  	   		     		  		  		    	 		 		   		 		  
    def __init__(self, leaf_size = 1, verbose = False): 
        self.leaf_size = leaf_size
        self.verbose = verbose
		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		
        
        
    def build_tree(self, features, labels):
                
        leaf = np.array([-1, stats.mode(labels).mode[0], np.nan, np.nan])
        
        if features.shape[0] <= self.leaf_size:
            return leaf
        
        # if values for labels are all the same
        if np.unique(labels).shape[0] == 1:
            return leaf

        
        random_feature = int(np.random.choice(features.shape[1], 1))
        random_feature_values = features[:, random_feature]
    
        # if values for random feature are all the same
        if np.unique(random_feature_values).shape[0] == 1:
            return leaf
    
        split_val = np.median(random_feature_values)
        
        smaller_half = random_feature_values <= split_val
        
        # if there edge is empty  
        if sum(smaller_half) == 0 or sum(~smaller_half) == 0:
            return leaf
        
        left_tree = self.build_tree(features[smaller_half], labels[smaller_half])
        right_tree = self.build_tree(features[~smaller_half], labels[~smaller_half])
        
        if left_tree.ndim == 1:
            left_tree_size = 1
        else:
            left_tree_size = left_tree.shape[0]
        
        root = np.array([random_feature, split_val, 1, left_tree_size+1])
        return np.vstack((root, left_tree, right_tree))
   

    def add_evidence(self, features, labels):
        self.tree = self.build_tree(features, labels)
     
    
    def find_leaf_value(self, feature, sub_tree):
        if sub_tree.shape[0] == 0:
            return 0.0

        curr_node = sub_tree[0]
        random_feature, split_val = int(curr_node[0]), curr_node[1]

        if random_feature == -1:
            return split_val
        else: 
            left_start, right_start = int(curr_node[2]), int(curr_node[3])

            if feature[random_feature] <= split_val:
                return self.find_leaf_value(feature, sub_tree[left_start:right_start])
            else:
                return self.find_leaf_value(feature, sub_tree[right_start:])
    
    
    def query(self, features):
        pred = np.zeros(features.shape[0])
        for idx, f in enumerate(features):
            pred[idx] = self.find_leaf_value(f, self.tree)
        return pred
		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
# if __name__ == "__main__":  		  	   		     		  		  		    	 		 		   		 		  
#     print("the secret clue is 'zzyzx'")  		  	   		     		  		  		    	 		 		   		 		  
