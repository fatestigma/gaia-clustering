import os
import sys
import multi_layer_network.src.minhash2 as lel
import networkx as nx
import json
from ast import literal_eval
import time

start = time.clock()

outputs_prefix = os.path.join(os.path.dirname(__file__), '../../outputs/') if len(sys.argv) < 2 else (sys.argv[1].rstrip('/') + '/')

input_file = outputs_prefix + 'entity.json'
output_file = outputs_prefix + 'entity.edgelist'

lel.get_links_edge_list(input_file, output_file)
G = nx.Graph()
path_to_cluster_heads = input_file
edgelist = output_file
outputfile = outputs_prefix + "entity.jl"

with open(edgelist, "r") as edges:
    G.add_nodes_from(literal_eval(edges.readline()))
    for edge in edges:
        edge_nodes = literal_eval(edge)
        G.add_edge(edge_nodes[0], edge_nodes[1])

cc = nx.connected_components(G)
cluster_heads = json.load(open(path_to_cluster_heads))
with open(outputfile + '_with_attr', 'w') as output:
    for c in cc:
        answer = dict()
        answer['entities'] = [cluster_heads[x] for x in c]
        json.dump(answer, output)
        output.write('\n')

cc = nx.connected_components(G)
with open(outputfile, 'w') as output:
    for c in cc:
        answer = dict()
        answer['entities'] = list(c)
        json.dump(answer, output)
        output.write('\n')

elapsed = (time.clock() - start)
print("Time used:", elapsed)
