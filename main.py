from busca.backtracking  import solve_backtracking
from busca.largura  import solve_bfs
from busca.gulosa import solve_greedy_search
from busca.ordenada import solve_ordered_search
from busca.profundidade  import solve_dfs
from busca.helpers import export_tree
from busca.a_estrela import solve_a_star

from anytree import Node

if __name__ == "__main__":
    root = solve_backtracking()
    export_tree(root, "backtrackingTree")

    root = solve_bfs()
    export_tree(root, "larguraTree")

    root = solve_dfs()
    export_tree(root, "profundidadeTree")

    root = solve_a_star()
    export_tree(root, "aEstrelaTree")

    root = solve_greedy_search()
    export_tree(root, "gulosaTree")
    
    root = solve_ordered_search()
    export_tree(root, "ordenadaTree")
    # if solution:
    #     print("Solução encontrada:")
    #     for state in solution:
    #         print(f"Estado: {state}")
    # else:
    #     print("Nenhuma solução encontrada.")

    


