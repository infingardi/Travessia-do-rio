def a_star():
    open_list = []
    heapq.heappush(open_list, (0, 0, initial_state, []))  # (f, g, estado, caminho percorrido)
    visited = set()
    
    while open_list:
        _, g, state, path = heapq.heappop(open_list)
        
        if state == goal_state:
            return path  # Caminho encontrado
        
        if state in visited:
            continue
        visited.add(state)
        
        for next_state, rule in get_next_states(state, path):
            new_g = g + 1
            f = new_g + heuristic(next_state)
            heapq.heappush(open_list, (f, new_g, next_state, path + [rule]))
    
    return None  # Nenhuma solução encontrada