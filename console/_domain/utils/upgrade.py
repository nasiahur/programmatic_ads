import json

#
#
#
def read_json_object(json_file):

    try:
        with open(json_file) as fin:
            return json.load(fin)
    except Exception as e:
         return {}

#
#
#
def read_json_array(json_file):
    
    try:
        with open(json_file) as fin:
            return json.load(fin)
    except Exception as e:
         return []