from anytree import Node
from busca.helpers import initial_state, goal_state, get_next_states, tag_solution_path

# Função para resolver com backtracking
def solve_backtracking():
    root = Node(name=0, state=initial_state, visited=False, rule=None, possible_rules=None)
    stack = [(root, [initial_state])]
    i = 0

    while stack:
        current_node, path = stack.pop()

        if current_node.visited and len(current_node.possible_rules) > 0:
            i += 1
            next_state, rule = current_node.possible_rules.pop(0)
            next_node = Node(name=i, state=next_state, visited=False, rule=rule, parent=current_node)
            stack.append((next_node, path + [next_state]))
            continue
        elif current_node.visited and len(current_node.possible_rules) == 0:
            if current_node.parent.name == 0:
                break
            stack.append((current_node.parent, path))
            continue

        current_node.visited = True

        if current_node.state[:2] == goal_state[:2]:
            tag_solution_path(current_node)
            return root
        
        current_node.possible_rules = get_next_states(current_node.state, path)

        if current_node.possible_rules:
            i += 1
            next_state, rule = current_node.possible_rules.pop(0)
            next_node = Node(name=i, state=next_state, visited=False, rule=rule, parent=current_node)
            stack.append((next_node, path + [next_state]))
        else:
            stack.append((current_node.parent, path))

    return None
