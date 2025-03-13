from anytree import Node
from busca.helpers import initial_state, goal_state, get_next_states, tag_solution_path

def solve_dfs():
    root = Node(name=0, state=initial_state, parent=None)
    stack = [root]
    abertos = [initial_state]  # Lista de estados abertos (simples)
    fechados = []              # Lista de estados fechados (simples)
    i = 0

    while stack:
        current_node = stack.pop()
        current_state = current_node.state

        if current_state in fechados:
            continue

        fechados.append(current_state)
        if current_state in abertos:
            abertos.remove(current_state)

        # Verifica se é o estado objetivo
        if current_state[:2] == goal_state[:2]:
            path = [node.state for node in current_node.path]
            tag_solution_path(current_node)
            return root

        # Gera próximos estados e adiciona à pilha
        next_states = get_next_states(current_state, fechados + abertos)
        for next_state, rule in next_states:
            i += 1
            next_node = Node(name=i, state=next_state, parent=current_node)
            stack.append(next_node)
            if next_state not in abertos:
                abertos.append(next_state)

    return None