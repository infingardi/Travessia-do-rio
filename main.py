from busca.backtracking  import solve_backtracking, export_tree
from anytree import Node

if __name__ == "__main__":
    solution, root = solve_backtracking()

    export_tree(root, "backtrackingTree")

    if solution:
        print("Solução encontrada:")
        for state in solution:
            print(f"Estado: {state}")
    else:
        print("Nenhuma solução encontrada.")

    


