from time import perf_counter
from anytree import Node
from busca.helpers import create_log, initial_state, goal_state, get_next_states, tag_solution_path

def solve_dfs():
    start = perf_counter()
    root = Node(name=0, state=initial_state, parent=None)
    all_nodes = [root]
    stack = [root]
    abertos = [initial_state]  # Lista de estados abertos (simples)
    fechados = []              # Lista de estados fechados (simples)
    i = 0
    solution = None

    while stack and not solution:
        i += 1
        current_node = stack.pop()
        current_state = current_node.state
        if current_state in fechados:
            continue

        fechados.append(current_state)
        if current_state in abertos:
            abertos.remove(current_state)

        # Verifica se é o estado objetivo
        if current_state[:2] == goal_state[:2]:
            solution = current_node
            continue

        # Gera próximos estados e adiciona à pilha
        next_states = get_next_states(current_state, fechados + abertos)
        for next_state, rule in next_states:
            next_node = Node(name=len(all_nodes), state=next_state, parent=current_node)
            all_nodes.append(next_node)
            stack.append(next_node)
            if next_state not in abertos:
                abertos.append(next_state)
        current_node.closed = True
    
    if solution:
        tag_solution_path(solution)
        create_log((all_nodes, i, perf_counter() - start), "dfs")
        return root
    return None