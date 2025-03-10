from busca.backtracking  import solve_backtracking
from busca.largura  import solve_bfs
from busca.profundidade  import solve_dfs
from busca.helpers import export_tree

from anytree import Node


if __name__ == "__main__":
    solution, root = solve_backtracking()
    export_tree(root, "backtrackingTree")

    solution, root = solve_bfs()
    export_tree(root, "larguraTree")

    solution, root = solve_dfs()
    export_tree(root, "profundidadeTree")

    # if solution:
    #     print("Solução encontrada:")
    #     for state in solution:
    #         print(f"Estado: {state}")
    # else:
    #     print("Nenhuma solução encontrada.")

    


