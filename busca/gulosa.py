from anytree import Node
from busca.helpers import get_path_from_node, initial_state, goal_state, get_next_states

def solve_greedy_search():
    def insert_ordered(open_nodes, node):
        for i, n in enumerate(open_nodes):
            if n.cost_global < node.cost_global:
                open_nodes.insert(i, node)
                return
        open_nodes.append(node)

    def get_heuristics(current_state, next_state):
        left, right, boat_side = current_state
        next_left, next_right, next_boat_side = next_state
        boat = (next_left - left) if boat_side == "direita" else (next_right - right)
        base_value = 1 if boat_side == "esquerda" else -1
        value = len(boat) * base_value
        for p in boat:
            if p in ["prisioneira", "policial"]:
                value += 1
        return value
    
    i = 0
    root = Node(name=0, parent=None, state=initial_state, cost_local=0, cost_global=0)
    open_nodes = [root]
    abertos = [initial_state]  # Lista de estados abertos
    fechados = []  # Lista de estados fechados
    solution = None
    
    while open_nodes:
        current_node = open_nodes.pop(0)
        current_state = current_node.state

        if current_state in fechados:
            continue

        fechados.append(current_state)
        if current_state in abertos:
            abertos.remove(current_state)

        if len(current_state[1]) == len(goal_state[1]):
            solution = current_node
            break

        possible_states = get_next_states(current_state, fechados + abertos)
        for next_state, rule in possible_states:
            if next_state in fechados:
                continue
            
            i += 1
            heuristics = get_heuristics(current_state, next_state)
            node = Node(
                name=i, 
                parent=current_node, 
                state=next_state, 
                cost_local=heuristics, 
                cost_global=current_node.cost_global + heuristics
            )
            insert_ordered(open_nodes, node)
            if next_state not in abertos:
                abertos.append(next_state)
    
    if not solution:
        return None, None, abertos, fechados
    return get_path_from_node(solution), root, abertos, fechados