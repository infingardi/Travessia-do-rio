from anytree import Node
from busca.helpers import initial_state, goal_state, get_next_states

# Função para resolver com busca em profundidade
def solve_dfs():
    root = Node(name=0, state=initial_state, visited=False, rule=None, possible_rules=None)
    stack = [(root, [initial_state])]  # Usando pilha (stack) para DFS
    i = 0  # Contador para identificar cada nó

    while stack:
        current_node, path = stack.pop()  # Pop do final da pilha (DFS)

        if current_node.visited:  # Se o nó já foi visitado, pula ele
            continue
        current_node.visited = True

        if current_node.state[:2] == goal_state[:2]:
            return path, root
        
        current_node.possible_rules = get_next_states(current_node.state, path)

        for next_state, rule in current_node.possible_rules:
            i += 1
            next_node = Node(name=i, state=next_state, visited=False, rule=rule, parent=current_node)
            stack.append((next_node, path + [next_state]))  # Adiciona ao final da pilha

    return None

