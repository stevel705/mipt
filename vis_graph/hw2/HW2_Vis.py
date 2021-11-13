#!/usr/bin/env python
# coding: utf-8

# In[109]:


import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
# import re
# import pylab
import warnings
warnings.filterwarnings("ignore")
#unnamed(1).graphml
DAG = nx.read_graphml("unnamed.graphml")


# In[5]:


# DAG


# In[8]:


# from networkx.drawing.nx_pydot import graphviz_layout
# import pydot
# pos = graphviz_layout(DAG, prog="twopi")
# nx.draw(DAG, pos, with_labels=True)
# plt.show()


# In[17]:


# Этап 1
vertices_sorted = list(reversed(list(nx.lexicographical_topological_sort(DAG))))


# In[258]:


def get_neighbors(G, parent):
    parents = list(G.predecessors(parent))
    children = list(G.neighbors(parent))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)
    return children, parents


# In[249]:


def get_max_P_vertex(v, sets):
#     return max(coffman_graham(DAG), key=coffman_graham(DAG).get)
    max_ = ["", 0]
    for i in sets:
        if v[i] > max_[1]:
            max_[0] = i
            max_[1] = v[i]
    return max_[0]


# In[307]:


def get_all_elements_on_layers(L):
    all_layers = set()
    for k, v in L.items():
        all_layers.update(v)
#     for i in range(k-1):
# #         print(L[i])
#         all_layers.update(L[i])
    return all_layers


# In[310]:


def coffman_graham(G, W=3):
    '''
    '''
    λ = {}
    vertices_sorted = list(reversed(list(nx.lexicographical_topological_sort(DAG))))
    
    V = set(vertices_sorted)
    
    for i, v in enumerate(vertices_sorted[::-1]):
        λ[v] = i+1
    
    k = 1 # Номер слоя
    U = set() # Множество изначально распределенных по слоям вершины
    L = defaultdict(list) # Множество вершин i-го слоя 
    
    count = 0
    while U != V:
        v_sub_u = V.difference(U)
        u = get_max_P_vertex(λ, v_sub_u)
#         print(u)
        
        neighbors = get_neighbors(DAG, u)
       
        L_k = get_all_elements_on_layers(L)
        L_k = L_k.difference(set(L[k]))

        if len(L[k]) < W and set(neighbors[0]).issubset(L_k):
            L[k].append(u)
        else:
            k += 1
            L[k].append(u)
        U.add(u)
        # count += 1
#         break
    return λ, L
    
    


# In[311]:


v, L = coffman_graham(DAG)
print(L)



# In[313]:


##### list(nx.edge_dfs(DAG, "n11",orientation='reverse'))
# get_neighbors(DAG, "n11")


# In[154]:


# get_children(DAG, "n5")
# a = ['n11']
# L = defaultdict(list)
# get_all_elements_on_layers(L)


# In[260]:


# b = set(reversed(list(nx.lexicographical_topological_sort(DAG))))
# b


# In[ ]:




