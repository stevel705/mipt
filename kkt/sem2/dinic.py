# INF = float("inf")
 
 
# class Dinic:
#     def __init__(self, n):
#         self.lvl = [0] * n
#         self.ptr = [0] * n
#         self.q = [0] * n
#         self.adj = [[] for _ in range(n)]
 
#     """
#     Here we will add our edges containing with the following parameters:
#     vertex closest to source, vertex closest to sink and flow capacity
#     through that edge ...
#     """
 
#     def add_edge(self, a, b, c, rcap=0):
#         self.adj[a].append([b, len(self.adj[b]), c, 0])
#         self.adj[b].append([a, len(self.adj[a]) - 1, rcap, 0])
 
#     # This is a sample depth first search to be used at max_flow
#     def depth_first_search(self, vertex, sink, flow):
#         if vertex == sink or not flow:
#             return flow
 
#         for i in range(self.ptr[vertex], len(self.adj[vertex])):
#             e = self.adj[vertex][i]
#             if self.lvl[e[0]] == self.lvl[vertex] + 1:
#                 p = self.depth_first_search(e[0], sink, min(flow, e[2] - e[3]))
#                 if p:
#                     self.adj[vertex][i][3] += p
#                     self.adj[e[0]][e[1]][3] -= p
#                     return p
#             self.ptr[vertex] = self.ptr[vertex] + 1
#         return 0
 
#     # Here we calculate the flow that reaches the sink
#     def max_flow(self, source, sink):
#         flow, self.q[0] = 0, source
#         for l in range(31):  # noqa: E741  l = 30 maybe faster for random data
#             while True:
#                 self.lvl, self.ptr = [0] * len(self.q), [0] * len(self.q)
#                 qi, qe, self.lvl[source] = 0, 1, 1
#                 while qi < qe and not self.lvl[sink]:
#                     v = self.q[qi]
#                     qi += 1
#                     for e in self.adj[v]:
#                         if not self.lvl[e[0]] and (e[2] - e[3]) >> (30 - l):
#                             self.q[qe] = e[0]
#                             qe += 1
#                             self.lvl[e[0]] = self.lvl[v] + 1
 
#                 p = self.depth_first_search(source, sink, INF)
#                 while p:
#                     flow += p
#                     p = self.depth_first_search(source, sink, INF)
 
#                 if not self.lvl[sink]:
#                     break
 
#         return flow
 
 
# # Example to use
 
# """
# Will be a bipartite graph, than it has the vertices near the source(4)
# and the vertices near the sink(4)
# """
# # Here we make a graphs with 10 vertex(source and sink includes)
# graph = Dinic(10)
# source = 0
# sink = 9
# """
# Now we add the vertices next to the font in the font with 1 capacity in this edge
# (source -> source vertices)
# """
# for vertex in range(1, 5):
#     graph.add_edge(source, vertex, 1)
# """
# We will do the same thing for the vertices near the sink, but from vertex to sink
# (sink vertices -> sink)
# """
# for vertex in range(5, 9):
#     graph.add_edge(vertex, sink, 1)
# """
# Finally we add the verices near the sink to the vertices near the source.
# (source vertices -> sink vertices)
# """
# for vertex in range(1, 5):
#     graph.add_edge(vertex, vertex + 4, 1)

# import pprint
# pprint.pprint(graph.adj)
# # Now we can know that is the maximum flow(source -> sink)
# print(graph.max_flow(source, sink))

#Dinic Algorithm

#build level graph by using BFS
def Bfs(C, F, s, t):  # C is the capacity matrix
        n = len(C)
        queue = []
        queue.append(s)
        global level
        level = n * [0]  # initialization
        level[s] = 1  
        while queue:
            k = queue.pop(0)
            for i in range(n):
                if (F[k][i] < C[k][i]) and (level[i] == 0): # not visited
                    level[i] = level[k] + 1
                    queue.append(i)
        return level[t] > 0

#search augmenting path by using DFS
def Dfs(C, F, k, cp):
        tmp = cp
        if k == len(C)-1:
            return cp
        for i in range(len(C)):
            if (level[i] == level[k] + 1) and (F[k][i] < C[k][i]):
                f = Dfs(C,F,i,min(tmp,C[k][i] - F[k][i]))
                F[k][i] = F[k][i] + f
                F[i][k] = F[i][k] - f
                tmp = tmp - f
        return cp - tmp

#calculate max flow
#_ = float('inf')
def MaxFlow(C,s,t):
        n = len(C)
        F = [n*[0] for i in range(n)] # F is the flow matrix
        flow = 0
        while(Bfs(C,F,s,t)):
               flow = flow + Dfs(C,F,s,100000)
        return flow, F

#-------------------------------------
# make a capacity graph
# node   s   o   p   q   r   t
# C = [[ 0, 3, 3, 0, 0, 0 ],  # s
#      [ 0, 0, 2, 3, 0, 0 ],  # o
#      [ 0, 0, 0, 0, 2, 0 ],  # p
#      [ 0, 0, 0, 0, 4, 2 ],  # q
#      [ 0, 0, 0, 0, 0, 2 ],  # r
#      [ 0, 0, 0, 0, 0, 3 ]]  # t

# source = 0  # A
# sink = 5    # F


# graph = [[ 0, 193, 320, 346, 12, 0, 0, 0, 0, 0 ],  # s
#             [ 0, 0, 0, 0, 0, 100, 100, 100, 100, 0 ],  
#             [ 0, 0, 0, 0, 0, 100, 100, 100, 100, 0 ], 
#             [ 0, 0, 0, 0, 0, 100, 100, 100, 100, 0 ],  
#             [ 0, 0, 0, 0, 0, 100, 100, 100, 100, 0 ],  
#             [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 267 ],
#             [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 157 ],
#             [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 188 ],
#             [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 259 ],
#             [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]] # t
# source = 0
# sink = 9

# graph = [[ 0, 201, 201, 0, 0, 0 ],  # s
#             [ 0, 0, 0, 100, 100, 0],  # o
#             [ 0, 0, 0, 100, 100, 0],  # p
#             [ 0, 0, 0, 0, 0, 201],
#             [ 0, 0, 0, 0, 0, 201], 
#             [ 0, 0, 0, 0, 0, 0]]
# source = 0
# sink = 5
# N = int(input())
# SR = list(map(int, input().split()))
# SC = list(map(int, input().split()))
N = 100
SR = [10000 for _ in range(N)]
SC = [10000 for _ in range(N)]

shape_graph = (N*2)+2
graph = [[0] * shape_graph for _ in range(shape_graph)]

source = 0  
sink = shape_graph-1

for i in range(len(SC)):
    graph[source][i+1] = SC[i]

for i in range(len(SR), len(SR)*2):
    idx =  i - len(SR)
    graph[i+1][sink] = SR[idx]

for i in range(1, len(SC)+1):
    for j in range(len(SR)+1, (len(SR)*2)+1):
        graph[i][j] = 100

# print("Dinic's Algorithm")
max_flow_value, A = MaxFlow(graph, source, sink)
if max_flow_value == sum(SR):
    print("YES")
    for j in range(len(SR)+1, (len(SR)*2)+1):
        lis_ = []
        for i in range(1, len(SC)+1):
            lis_.append(A[i][j])
        print(*lis_)
else:
    print("NO")