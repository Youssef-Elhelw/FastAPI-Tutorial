import pickle
import os
import sys

# parent of the current directory, because the json_w_r.py file is in the avoid directory, which is a sibling of the prefered directory.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR) 

from avoid.json_w_r import Fruit

orange = Fruit("Orange", "orange")

# now instead of writing to a json file, we will write to a pickle file, which will preserve the methods of the class.
with open("prefered/fruit.pkl", "wb") as f: # here the "wb" means write binary mode, because pickle files are binary files, if the file does not exist, it will be created, if it exists, it will be overwritten
    pickle.dump(orange, f)

# to read the pickle file back
with open("prefered/fruit.pkl", "rb") as f:
    orange_from_pickle = pickle.load(f) # here the "rb" means read binary mode, because pickle files are binary files
    print(orange_from_pickle.describe()) # notice that we can still use the describe method, which is a huge advantage of using pickle over json.

orange_from_pickle.color = "dark orange"
print(orange_from_pickle.describe())