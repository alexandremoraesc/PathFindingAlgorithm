class Tiles:
    def __init__(self, r, c, filesnumber, filled = False, start = False, end = False):
        self.r = r
        self.c = c
        self.vizinhos = []
        self.filled = filled 
        self.start = start
        self.end = end
        self.number = filesnumber*r + c

    def __eq__(self, o):
        if isinstance(o, Tiles):
            if (o.r == self.r and o.c == self.c):
                return True 
        
        return False

    def __repr__(self):
        return f'({self.r}, {self.c})'

