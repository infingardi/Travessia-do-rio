from anytree import Node, RenderTree

# Inicialização dos estados
initial_state = (frozenset({"policial", "prisioneira", "pai", "mãe", "filho1", "filho2", "filha1", "filha2"}), frozenset(), "esquerda")
goal_state = (frozenset(), frozenset({"policial", "prisioneira", "pai", "mãe", "filho1", "filho2", "filha1", "filha2"}), "direita")

# Regras de transição
rules = [
    frozenset({"pai", "mãe"}),
    frozenset({"policial", "prisioneira"}),
    frozenset({"policial"}),
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
    # Os filhos não podem ficar sozinhos com a mãe;
    if 'mãe' in left and ('filho1' in left or 'filho2' in left) and 'pai' not in left:
        return False
    if 'mãe' in right and ('filho1' in right or 'filho2' in right) and 'pai' not in right:
        return False
   
    # As filhas não podem ficar sozinhas com o pai;
    if 'pai' in left and ('filha1' in left or 'filha2' in left) and 'mãe' not in left:
        return False
    if 'pai' in right and ('filha1' in right or 'filha2' in right) and 'mãe' not in right:
        return False
   
    # A prisioneira não pode ficar sozinha com os membros da família na ausência do policial.
    if 'prisioneira' in left and any(p in left for p in ['pai', 'mãe', 'filho1', 'filho2', 'filha1', 'filha2']) and 'policial' not in left:
        return False
    if 'prisioneira' in right and any(p in right for p in ['pai', 'mãe', 'filho1', 'filho2', 'filha1', 'filha2']) and 'policial' not in right:
        return False
   
    return True

# Função para gerar os próximos estados
def get_next_states(state, path):
    left, right, boat = state
    next_states = []

    current_side = left if boat == "esquerda" else right
    opposite_side = right if boat == "esquerda" else left

    for rule in rules:
        if rule.issubset(current_side):  # Apenas se a regra puder ser aplicada
            new_left, new_right = set(left), set(right)

            if boat == "esquerda":
                new_left -= rule
                new_right |= rule
                new_boat = "direita"
            else:
                new_right -= rule
                new_left |= rule
                new_boat = "esquerda"

            new_state = (frozenset(new_left), frozenset(new_right), new_boat)

            # Verifica se é válido
            if is_valid(new_state):
                if new_state not in path:
                    next_states.append((new_state, rule))  # Adiciona o estado junto com a regra

    return next_states

# Função para resolver o problema com backtracking usando anytree
# Função para resolver o problema com backtracking usando anytree
def solveBacktracking(root):
    # Pilha de nós a serem explorados
    stack = [(root, [initial_state])]  # Cada item da pilha é (nó_atual, caminho_percorrido)

    while stack:
        current_node, path = stack.pop()

        # Se já foi visitado, ignora o nó
        if current_node.visited and len(current_node.possible_rules) > 0:
            next_state, rule = current_node.possible_rules[0]
            current_node.possible_rules.pop(0)
            
            next_node = Node(name=f"Node-{next_state}", state=next_state, visited=False, rule=rule, parent=current_node)
            stack.append((next_node, path + [next_state]))  # Adiciona o novo nó e caminho
            continue
        elif current_node.visited and len(current_node.possible_rules) == 0:
            if(current_node.parent.name == 'Root'):
                break
            # Ao retornar ao nó pai, adicione o caminho correto ao pai
            stack.append((current_node.parent, path)) 
            continue

        # Marca o nó como visitado
        current_node.visited = True

        # Se chegamos ao estado objetivo
        if current_node.state[:2] == goal_state[:2]:
            return path  # Retorna a solução encontrada
        
        current_node.possible_rules = get_next_states(current_node.state, path)

        if len(current_node.possible_rules) > 0:
            next_state, rule = current_node.possible_rules[0]
            current_node.possible_rules.pop(0)
            
            next_node = Node(name=f"Node-{next_state}", state=next_state, visited=False, rule=rule, parent=current_node)
            stack.append((next_node, path + [next_state]))  # Adiciona o novo nó e caminho
        else:
            # Ao retornar ao nó pai, adicione o caminho correto ao pai
            stack.append((current_node.parent, path))

    return None  # Sem solução encontrada


# Cria o nó raiz da árvore com a flag visited inicialmente como False
root = Node(name="Root", state=initial_state, visited=False, rule=None, possible_rules=None)
solution = solveBacktracking(root)

# Exibe a solução
# if solution:
#     print("Caminho encontrado:")
#     for state in solution:
#         print(f"Estado: {state}")
# else:
#     print("Nenhuma solução encontrada.")

for pre, fill, node in RenderTree(root):
    print(f"{pre}{node.name}")
