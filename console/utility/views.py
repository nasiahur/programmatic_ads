from django.shortcuts import render

# Create your views here.

class ListViewTransposer:
    
    def transpose(self, list, columns):
    
        # debug check 
        assert(columns)  > 1
        
        table = []
        if columns > len(list):
            table.append(list)
            return table
        
        # create number of columns requred
        for i in xrange(0, columns):
             table.append([])
             
        if len(list) == 0:
            return table
        
        # see how many elements will fit into each column
        num = len(list) / columns + len(list) % columns
        
        # polulate the table
        for i in xrange(0, columns):
            for j in xrange(0, num):
                table[i].append(list.pop(0))
                if len(list) == 0:
                    break
            if len(list) == 0:
                    break
                    
        # transpose it
        table = map(None,*table)
        
        # and return        
        return table