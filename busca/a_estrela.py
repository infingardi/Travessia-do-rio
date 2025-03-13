from anytree import Node
from busca.calc_weight import get_rule_weight, get_state_weight
from busca.helpers import get_path_from_node, initial_state, goal_state, get_next_states, insert_ordered, tag_solution_path

def solve_a_star():
    i = 0
    root = Node(name=0, parent=None, state=initial_state, weight_state=get_state_weight(initial_state), weight_path=0)
    open_nodes = [root]
    solution = None
    while open_nodes:
        current_node = open_nodes.pop(0)
        if len(current_node.state[1]) == len(goal_state[1]):
            solution = current_node
            break
        possible_states = get_next_states(current_node.state, get_path_from_node(current_node))
        for next_state, rule in possible_states:
          i += 1
          node = Node(
            name=i, 
            parent=current_node, 
            state=next_state, 
            weight_state=get_state_weight(next_state),
            weight_path=current_node.weight_path + get_rule_weight(current_node.state, next_state),
          )
          insert_ordered(open_nodes, node, lambda n: n.weight_path + n.weight_state)
    
    if not solution:
        return None
    tag_solution_path(solution)
    return root
  