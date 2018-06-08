import json

#
#
#
class JsonDumper:
    def dumps(self, data):
        return json.dumps(data, sort_keys=True, indent=4)
        