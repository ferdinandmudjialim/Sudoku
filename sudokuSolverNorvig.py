def cross(A, B):
    """Cross product of elements in A and elements in B."""
    return [a + b for a in A for b in B]


digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s], [])) - {s})  # includes squares in units[s], but excludes s itself
             for s in squares)

#print(unitlist)
#print(peers)

grid0 = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid1 = '400000805030000000000700000020000060000080400000010000000603070500200000104000000'
gridhard = '800000000003600000070090200050007000000045700000100030001000068008500010090000400'


def grid_values(grid):
    """Convert grid into a dict w/ chars, or '0' or '.' for empties"""
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))


def parse_grid(grid):
    """Convert grid to a dict of possible values, or
    return False if there is a contradiction detected.
    """
    # From a grid string to a values dictionary containing key and possible values in '123456' format
    values = dict((s, digits) for s in squares)  # initialize to '123456789' for all first
    i = 0
    for key in values:  # Populate fixed values
        if grid[i] not in '0.':
            values[key] = grid[i]
            if not assign(values, key, grid[i]):
                return False
        i += 1

    #return False w/ contradiction?
    return values


def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and
    propagate. Return values, except return False if a contradiction
    is detected."""
    other_values = values[s].replace(d, '')
    if not all(eliminate(values, s, d2) for d2 in other_values):
        return False  # Contradiction somewhere
    else:
        return values
    # Failed Attempt
    # for u in other_values: 
    #     if not eliminate(values, s, d): 
    #         return False  # Contradiction somewhere
    #     else: 
    #         return values


def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places
    <= 2. Return values, except return False if a contradiction
    is detected."""
    if d not in values[s]:
        return values  # Already eliminated
    values[s].replace(d, '')  # Eliminate d
    # (1) If a square has only one possible value, then eliminate that value from the square's peers.
    if len(values[s]) == 0:
        return False  # Contradiction; no value is suitable
    elif len(values[s]) == 1:
        d2 = values[s]  # Only value left
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False  # Contradiction somewhere in recursion
    # (2) If a unit has only one possible place for a value, then put the value there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False  # Contradiction; no place for d
        elif len(dplaces) == 1:
            # d can only be in one place, so assign it there
            if not assign(values, dplaces[0], d):  # Some contradiction is raised
                return False


def search(values):
    """Using depth-first search and propagation, try all possible values.
    Also use the heuristic of choosing the numbers w/ least number of possibilities first"""


def solve(grid):
    return search(parse_grid(grid))


def display(values):
    """Display these values as a 2-D grid."""
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in cols))
        if r in 'CF': print(line)


gridvalues = parse_grid(grid0)
#print(gridvalues)
display(gridvalues)
#solve(grid)
