from anytree import Node
from busca.helpers import initial_state, goal_state, get_next_states, a_star_heuristic

# Função para resolver com busca A*
def solve_a_star():
    root = Node(name="Root", state=initial_state, visited=False, rule=None, possible_rules=None)
    open_list = [(root, [initial_state], 0)]  # (nó, caminho, custo)
    i = 0

    while open_list:
        open_list.sort(key=lambda x: x[2] + a_star_heuristic(x[0].state))  # Ordena pela função f(n) = g(n) + h(n)
        current_node, path, cost = open_list.pop(0)
        current_node.visited = True

        if current_node.state[:2] == goal_state[:2]:
            return path, root
        
        current_node.possible_rules = get_next_states(current_node.state, path)

        for next_state, rule in current_node.possible_rules:
            i += 1
            next_node = Node(name=f"Node-{i}", state=next_state, visited=False, rule=rule, parent=current_node)
            open_list.append((next_node, path + [next_state], cost + 1))

    return None