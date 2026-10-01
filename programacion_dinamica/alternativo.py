import sys
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class Item:
    weight: int
    benefit: int

def parse_filename(filename: str) -> Tuple[int, List[Item], int]:
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        
    if not lines:
        return 0, [], 0
        
    capacity = int(lines[0])
    items = []
    max_benefit = 0
    for line in lines[1:]:
        if line.strip():
            w, b = map(int, line.split(','))
            items.append(Item(w, b))
            max_benefit += b
            
    return capacity, items, max_benefit

"""
Planteo alternativo: minimizar el peso para un beneficio fijo
"""
def solve(filename: str) -> int:
    capacity, items, max_benefit = parse_filename(filename)
    if not items:
        return 0
        
    solutions = [float('inf')] * (max_benefit + 1)
    solutions[0] = 0
    
    for item in items:
        for v in range(max_benefit, -1, -1):
            solutions[v] = min(solutions[v], solutions[max(0, v - item.benefit)] + item.weight)
            
    result = 0
    for v in range(max_benefit, -1, -1):
        if solutions[v] <= capacity:
            result = v
            break
            
    return result

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(solve(sys.argv[1]))
