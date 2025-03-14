from time import perf_counter
from anytree import Node
from busca.helpers import create_log, initial_state, goal_state, get_next_states, tag_solution_path

# Função para resolver com busca em largura
def solve_bfs():
    start = perf_counter()
    root = Node(name=0, state=initial_state, visited=False, rule=None, possible_rules=None)
    all_nodes = [root]
    stack = [(root, [initial_state])]
    i = 0
    solution = None

    while stack and not solution:
        i += 1
        current_node, path = stack.pop(0)
        current_node.visited = True

        if current_node.state[:2] == goal_state[:2]:
            solution = current_node
            continue
        
        current_node.possible_rules = get_next_states(current_node.state, path)
        for next_state, rule in current_node.possible_rules:
            next_node = Node(name=len(all_nodes), state=next_state, visited=False, rule=rule, parent=current_node)
            stack.append((next_node, path + [next_state]))
            all_nodes.append(next_node)
        current_node.closed = True
    
    if not solution:
        return None
    tag_solution_path(solution)
    create_log((root, i, perf_counter() - start), "bfs")
    return root

