from anytree import RenderTree
from anytree.exporter import DotExporter
from graphviz import Source

# Inicialização dos estados
initial_state = (frozenset({"policial", "prisioneira", "pai", "mãe", "filho1", "filho2", "filha1", "filha2"}), frozenset(), "esquerda")
goal_state = (frozenset(), frozenset({"policial", "prisioneira", "pai", "mãe", "filho1", "filho2", "filha1", "filha2"}), "direita")

# Regras de transição
rules = [
    frozenset({"policial", "prisioneira"}),
    frozenset({"policial"}),
    frozenset({"pai", "mãe"}),
    frozenset({"policial", "filha1"}),
    frozenset({"policial", "filha2"}),
    frozenset({"policial", "filho1"}),
    frozenset({"policial", "filho2"}),
    frozenset({"pai", "filho1"}),
    frozenset({"pai", "filho2"}),
    frozenset({"mãe", "filha1"}),
    frozenset({"mãe", "filha2"}),
    frozenset({"pai"}),
    frozenset({"mãe"})
]

# Função para verificar se um estado é válido
def is_valid(state):
    left, right, boat = state
    if 'mãe' in left and ('filho1' in left or 'filho2' in left) and 'pai' not in left:
        return False
    if 'mãe' in right and ('filho1' in right or 'filho2' in right) and 'pai' not in right:
        return False
    if 'pai' in left and ('filha1' in left or 'filha2' in left) and 'mãe' not in left:
        return False
    if 'pai' in right and ('filha1' in right or 'filha2' in right) and 'mãe' not in right:
        return False
    if 'prisioneira' in left and any(p in left for p in ['pai', 'mãe', 'filho1', 'filho2', 'filha1', 'filha2']) and 'policial' not in left:
        return False
    if 'prisioneira' in right and any(p in right for p in ['pai', 'mãe', 'filho1', 'filho2', 'filha1', 'filha2']) and 'policial' not in right:
        return False
    return True

# Função para gerar os próximos estados
def get_next_states(state, visited):
    left, right, boat = state
    next_states = []
    current_side = left if boat == "esquerda" else right

    for rule in rules:
        if rule.issubset(current_side):
            new_left = set(left)
            new_right = set(right)
            
            if boat == "esquerda":
                new_left -= rule
                new_right |= rule
                new_boat = "direita"
            else:
                new_right -= rule
                new_left |= rule
                new_boat = "esquerda"
            
            new_state = (frozenset(new_left), frozenset(new_right), new_boat)
            if is_valid(new_state) and new_state not in visited:
                next_states.append((new_state, rule))
    
    return next_states

def get_path_from_node(node):
    path = []
    while node:
        path.insert(0, node.state)
        node = node.parent
    return path

def insert_ordered(open_nodes, node, value_extractor):
    for i, n in enumerate(open_nodes):
        if value_extractor(n) < value_extractor(node):
            open_nodes.insert(i, node)
            return
    open_nodes.append(node)
    
def get_rule_from_states(state_before, state_after):
    left, right, boat_side = state_before
    next_left, next_right, next_boat_side = state_after
    return (next_left - left) if boat_side == "direita" else (next_right - right)

def anytree_to_dot(root, filename="tree.dot", open_states=None, closed_states=None):
    def color_attr(*nodes):
        if all(hasattr(node, "is_solution") and node.is_solution for node in nodes):
            return '[color="red"]'
        return ""
    
    def stringify_node(node):
        node_cost = f"\n{node.weight_state}" if hasattr(node, "weight_state") else ""
        return f"L: {' '.join(node.state[0])}\nR: {' '.join(node.state[1])}\n{node_cost}"
    
    def stringify_edge(node_before, node_after):
        boat = get_rule_from_states(node_before.state, node_after.state)
        direction = "-->" if node_after.state[2] == "direita" else "<--"
        edge_cost = node_after.weight_path - node_before.weight_path if hasattr(node_after, "weight_path") and hasattr(node_before, "weight_path") else ""
        return f"{direction}\n{' '.join(boat)}\n{edge_cost}"

    def write_tree(root, f):
        f.write(f"{root.name} [label=\"{stringify_node(root)}\"]{color_attr(root)}\n")
        for child in root.children:
            f.write(f"{root.name} -> {child.name} [label=\"{stringify_edge(root, child)}\"]{color_attr(root, child)}\n")
            write_tree(child, f)
    
    # Nova subfunção responsável por renderizar as listas de estados abertos e fechados
    def write_legend(f, open_states, closed_states):
        f.write('subgraph cluster_legend {\n')
        f.write('label="Legenda";\n')
        
        if open_states:
            open_label = "Abertos:\\n" + "\\n".join(
                [f"L: {', '.join(sorted(s[0]))}\\nR: {', '.join(sorted(s[1]))}" for s in open_states]
            )
            f.write(f'open [label="{open_label}", shape=box, color=green];\n')
        
        if closed_states:
            closed_label = "Fechados:\\n" + "\\n".join(
                [f"L: {', '.join(sorted(s[0]))}\\nR: {', '.join(sorted(s[1]))}" for s in closed_states]
            )
            f.write(f'closed [label="{closed_label}", shape=box, color=red];\n')
        
        f.write("}\n")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("digraph {\n")
        write_tree(root, f)
        if open_states or closed_states:
            write_legend(f, open_states, closed_states)
        f.write("}\n")

def tag_solution_path(node):
    node_aux = node
    while node_aux:
        node_aux.is_solution = True
        node_aux = node_aux.parent

def export_tree(root, filename="tree", open_states=None, closed_states=None):
    # Gera o caminho do arquivo DOT dentro da pasta Trees
    path = f"Trees/{filename}"
    anytree_to_dot(root, path + ".dot", open_states, closed_states)
    Source.from_file(path + ".dot").render(path, format="png", cleanup=True)

def a_star_heuristic(state):
    """
    Função heurística para o algoritmo A*.
    Mede a quantidade de pessoas que ainda precisam atravessar o rio.
    """
    left, right, boat = state
    return len(left)  # Quanto mais pessoas na margem inicial, maior o custo estimado