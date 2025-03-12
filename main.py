from busca.backtracking  import solve_backtracking
from busca.largura  import solve_bfs
from busca.gulosa import solve_greedy_search
from busca.profundidade  import solve_dfs
from busca.helpers import export_tree
from busca.a_estrela import solve_a_star

from anytree import Node

if __name__ == "__main__":
    # solution, root = solve_backtracking()
    # export_tree(root, "backtrackingTree")

    # solution, root = solve_bfs()
    # export_tree(root, "larguraTree")

    # solution, root = solve_dfs()
    # export_tree(root, "profundidadeTree")

    solution, root = solve_a_star()
    export_tree(root, "aEstrelaTree")
    # path, root, abertos, fechados = solve_dfs()
    # export_tree(root, "profundidadeTree", abertos, fechados)

    # solution, root = solve_greedy_search()
    # export_tree(root, "gulosaTree")
    # if solution:
    #     print("Solução encontrada:")
    #     for state in solution:
    #         print(f"Estado: {state}")
    # else:
    #     print("Nenhuma solução encontrada.")

    


