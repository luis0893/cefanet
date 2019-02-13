import os
import pickle

user_db = {}
if os.path.exists('./database/user_dict.pickle'):
    with open('./database/user_dict.pickle', 'rb') as handle:
        user_db = pickle.load(handle)
        print("base de datos" + user_db)
else:
    print("no se encontro el archvo")
    user_db = {}