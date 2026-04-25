def bfs(minHeap, k, x):
    if not minHeap:
        return False
    
    count = 0
    queue = [0]
    
    while queue:
        i = queue.pop(0)
        
        if i >= len(minHeap):
            continue
        
        if minHeap[i] < x:
            count += 1
            if count >= k:
                return True
            
            left = 2 * i + 1
            right = 2 * i + 2
            queue.append(left)
            queue.append(right)
    
    return False
