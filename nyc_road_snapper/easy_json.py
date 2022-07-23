import json
import os

def get(file, key=''):

    retrieval : dict = {}
    with open(file, 'r') as stream:
        retrieval = json.load(stream)

    if key != '':
        try:
            return retrieval[key]
        except:
            return 'error'

    return retrieval

def dump(dict : dict, file : str, PROTECT=True):
    if os.path.exists(file) and PROTECT:
        # logger.error(f"[ {file} ] already exists")
        return
    # if PROTECT and 
    with open(file, 'w') as stream:
        json.dump(dict, stream, indent=2)

    return

def update(file : str, key : str, value : str):
    d = json.load(open(file))
    d[key] = value
    dump(d, file, PROTECT=False)
    # logger.info(f"[ {file} ] updated")    
    return 

def to_dict(json_str: str):
    return json.loads(json_str)