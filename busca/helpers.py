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

def export_tree(root, filename="tree", open_states=None, closed_states=None):
    dot_content = ["digraph G {"]
    
    # Adiciona todos os nós e conexões da árvore
    for _, _, node in RenderTree(root):
        # Formata o estado do nó sem exibir o "Barco"
        left = ', '.join(sorted(node.state[0]))
        right = ', '.join(sorted(node.state[1]))
        dot_content.append(f'{node.name} [label="L: {left}\\nR: {right}"]')
        
        # Adiciona conexão com o pai
        if node.parent:
            dot_content.append(f'{node.parent.name} -> {node.name}')

    # Adiciona legenda com abertos/fechados
    if open_states or closed_states:
        legend = ['subgraph cluster_legend {', 'label="Legenda";']
        
        if open_states:
            estados = "\\n".join([f"L: {', '.join(sorted(s[0]))}\\nR: {', '.join(sorted(s[1]))}" for s in open_states])
            legend.append('open [label="Abertos:\\n' + estados + '", shape=box, color=green];')
            
        if closed_states:
            estados = "\\n".join([f"L: {', '.join(sorted(s[0]))}\\nR: {', '.join(sorted(s[1]))}" for s in closed_states])
            legend.append('closed [label="Fechados:\\n' + estados + '", shape=box, color=red];')
            
        legend.append('}')
        dot_content.extend(legend)

    dot_content.append("}")  # Fecha o digraph

    # Gera o arquivo e a imagem
    path = f"Trees/{filename}"
    with open(f"{path}.dot", "w", encoding="utf-8") as f:
        f.write("\n".join(dot_content))
    
    Source.from_file(f"{path}.dot").render(path, format="png", cleanup=True)
