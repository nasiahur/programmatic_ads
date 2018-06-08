#
#
#
class ConfReader:

    def __init__(self, path):
        self.path = path

    def read_lines(self, skip_comments):
        lines = self.read_contents(self.path)
        if not skip_comments:
            return lines

        return self.remove_comments(lines)

    def read_contents(self, path):

        with open(self.path) as fin:
            return fin.read().splitlines()

    def remove_comments(self, lines):
        
        result = []
        for line in lines:    
            pos = line.find('#')
            if pos != -1:
                line = line[0:pos]
            line = line.strip()
            if len(line) > 0:
                result.append(line)
        return result