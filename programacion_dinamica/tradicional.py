import sys
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class Item:
    weight: int
    benefit: int

def parse_filename(filename: str) -> Tuple[int, List[Item]]:
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        
    if not lines:
        return 0, []
        
    capacity = int(lines[0])
    items = []
    for line in lines[1:]:
        if line.strip():
            _weight, _benefit = map(int, line.split(','))
            items.append(Item(_weight, _benefit))
            
    return capacity, items

"""
Planteo tradicional: maximiza el beneficio para un capacidad fija
"""
def solve(filename: str) -> int:
    capacity, items = parse_filename(filename)
    if not items:
        return 0
        
    solutions = [0] * (capacity + 1)
    
    for item in items:
        for w in range(capacity, item.weight - 1, -1):
            solutions[w] = max(solutions[w], solutions[w - item.weight] + item.benefit)
            
    return solutions[capacity]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(solve(sys.argv[1]))
