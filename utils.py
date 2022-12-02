import os
import sys
from pymongo import MongoClient

def get_DB():
    with open(os.path.join(sys.path[0], "config.ini"), "r") as f:
        content=f.readlines()
    client = MongoClient("mongodb+srv://ncsuse123:"+content[0]+"@cluster0.vceghwv.mongodb.net/?retryWrites=true&w=majority")

    
    return client.SEProj2
