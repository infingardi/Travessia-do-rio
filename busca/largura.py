from anytree import Node
from busca.helpers import initial_state, goal_state, get_next_states

# Função para resolver com busca em largura
def solve_bfs():
    root = Node(name="Root", state=initial_state, visited=False, rule=None, possible_rules=None)
    stack = [(root, [initial_state])]
    i = 0

    while stack:
        current_node, path = stack.pop(0)
        current_node.visited = True

        if current_node.state[:2] == goal_state[:2]:
            return path, root
        
        current_node.possible_rules = get_next_states(current_node.state, path)

        for next_state, rule in current_node.possible_rules:
            i += 1
            next_node = Node(name=(f"Node-{i}"), state=next_state, visited=False, rule=rule, parent=current_node)
            stack.append((next_node, path + [next_state]))

    return None

