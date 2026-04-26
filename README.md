## Question 1:
My initial plan to traverse a min-heap to find k values that satisfy x was to recursively delete the root node and add a condition to check if the new root satisfied x. After some research I found that it would take O(klogn) time. So I then thought to do a search using BFS or DFS. I decided on BFS for no particular reason. Both BFS and DFS would result in O(k) time. My algorithm is an implementation of BFS. When a node is visited, it gets checked if its value is smaller than x. If so, count is incremented and its children are added to the queue for future exploration. If the node's value is greater than or equal to x, its children are never added to the queue. This pruning is what guarantees O(k) time, as we never explore branches that cannot contain values smaller than x. The program returns true when count reaches k.

## Question 2:
To determine if a graph is a tree, I needed three checks.
- The number of edges should be vertices - 1 (edges == v -1).
- Starting from one vertex, I should be able to reach all other vertices (Connectivity).
- Ensure that you can't visit a node that has already been visited in my current path (Cycle detection).

For this problem, I chose an adjacency list for how my input graph would be represented. I found it the easiest to work with, and using it I was able to do a DFS traversal to check connectivity and detect cycles in one pass. I was also able to easily count my edges. I started with a quick check to see if my edges were equal to my vertices - 1. Then I used DFS to check for connectivity and cycle detection simultaneously.

## Question 4 (Analysis & Comparison)

### Path Differences:
BFS finds the shortest path because it explores level by level. In my implementation, it was able to find the shortest path.

While it is possible for DFS to find the shortest path, it is not guaranteed. In my case, it didnt find the shortest path. 

### Nodes Visited Before Target:
BFS visits fewer nodes then DFS due to its expanding behavior. When the target is close to the starting node, BFS is able to expand outwards and find the target while visiting fewer nodes. DFS chooses a path at random and searches the branches depth. If that path doesnt contain the target, it backtracks and visits even more nodes. 

### Adjacency List vs. Adjacency Matrix:
**Adjacency List**

An adjacency list uses O(V + E) space, making it efficient for sparse graphs. Neighbor lookup involves iterating only through existing edges, which avoids unnecessary work. Because of this, it seems generally faster in practice for BFS and DFS on sparse graphs.

**Adjacency Matrix**

An adjacency matrix uses O(V^2) space, which can be expensive for large or sparse graphs. Neighbor lookup requires scanning an entire row, O(V) per node, even if a lot of entries are zero. But checking if an edge exists is very fast (O(1)). Despite this advantage, it is typically slower for BFS and DFS due to scanning many non-existent edges.

### Execution Time:
Adjacency List is generally faster because it skips non-existent edges. Matrix must scan every column even if most entries are 0. Both BFS and DFS have the same O(V + E) complexity on a list, and O(V^2) on a matrix.

### Memory Usage:
Adjacency Matrix uses more memory (V^2 entries). BFS also uses more memory than DFS at runtime because it stores all frontier paths in the queue, while DFS only keeps one branch on the stack. 

