
# conversion functions

def _n2c(notation): # notation to coords
    # converts chess notation to row and column indices
    # e.g. 'a1' -> (0,0), 'a2' -> (1,0), 'e4' -> (3,4), 'h8' -> (7,7)
    return int(notation[1]) - 1, ord(notation[0]) - ord('a')

def _c2n(row, col): # coords to notation
    # converts row and column indices to chess notation
    # e.g. (0,0) -> 'a1', (1,0) -> 'a2', (3,4) -> 'e4', (7,7) -> 'h8'
    return chr(col + ord('a')) + str(row + 1)
