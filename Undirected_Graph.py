# graph = adjacency list 
# i.g graph = {'A': ['B', 'C'], 'B': ['A'], 'C': ['A']}

def isTree(graph):
    edge_count = sum(len(neighbors) for neighbors in graph.values()) // 2
    
    if edge_count != len(graph) - 1:
        return False
    
    visited = set()
    stack = [next(iter(graph))]
    
    while stack:
        node = stack.pop()
        
        if node in visited:
            return False
        
        visited.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
    
    return len(visited) == len(graph)
