#
#
#
class Reader:

    @staticmethod
    def read(file):

        lines = []
        with open(file, 'r') as fin:
            lines = fin.readlines()
        return lines


#
#
#
class Splitter:

    @staticmethod
    def split(value_str, separator=' '):

        items = [x.strip() for x in value_str.split(separator)]
        items = [x for x in items if x]

        return items
