from flask import Flask, render_template, url_for, request, redirect, send_file
import time
import matplotlib.pyplot as plt
import os
import networkx as nx
from networkx.algorithms.flow import dinitz
from networkx.generators.community import random_partition_graph
from networkx.generators.geometric import random_geometric_graph
from dinic import MaxFlow
from random import randrange


lista = []
lista.append("x")
lista.append("a")
lista.append("b")
lista.append("c")
lista.append("d")
lista.append("e")
C = [[ 0, 16, 13, 0, 0, 0 ],
     [ 0, 0, 10, 12, 0, 0 ], 
     [ 0, 4, 0, 0, 14, 0 ], 
     [ 0, 0, 9, 0, 0, 20 ],
     [ 0, 0, 0, 7, 0, 4],  
     [ 0, 0, 0, 0, 0, 3 ]]  

app=Flask(__name__)

@app.route('/',  methods=['POST', 'GET'])
def index():
    figure = plt.figure()
    path2 = os.getcwdb();
    print()
    path = os.path.abspath(__file__).strip('app.py')
    save = path + '/static/Graph.png'
    save2 = path + '/static/Graph2.png'
    try:
        if(os.path.exists(save)):
            os.remove(save)
    except:
        pass

    G = nx.DiGraph()

    G.add_edge("x", "a", capacity=16);
    G.add_edge("x", "b", capacity=13);
    G.add_edge("a", "b", capacity=10);
    G.add_edge("a", "c", capacity=12);
    G.add_edge("b", "a", capacity=4);
    G.add_edge("b", "d", capacity=14);
    G.add_edge("c", "b", capacity=9);
    G.add_edge("c", "e", capacity=20);
    G.add_edge("d", "c", capacity=7);
    G.add_edge("d", "e", capacity=4);

    seed = randrange(700)
    pos=nx.spring_layout(G, seed=seed)

    nx.draw(G,pos, with_labels = True,)
    labels = nx.get_edge_attributes(G,'capacity')
    nx.draw_networkx_edge_labels(G,pos, edge_labels=labels)
    plt.savefig(save, format="PNG")
    
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            R = dinitz(G, lista[int(data['content0'])], lista[int(data['content2'])])
            flow_value = nx.maximum_flow_value(G, lista[int(data['content0'])], lista[int(data['content2'])])
            if (flow_value == R.graph["flow_value"]):
                test = R.graph["flow_value"]
            else:
                test = MaxFlow(C,int(data['content0']),int(data['content2']))
            
            
            tes = list(nx.maximum_flow(G, lista[int(data['content0'])], lista[int(data['content2'])]))[1:]
            
            try:
                if(os.path.exists(save)):
                    os.remove(save2)
            except:
                pass
            N = nx.DiGraph()
            for d in tes:
                for k, v in d.items():
                    for k1, v1 in v.items():
                        N.add_edge(k, k1, capacity=int(v1));
            figure = plt.figure()
            nx.draw(N,pos, with_labels = True,)
            labels = nx.get_edge_attributes(N,'capacity')
            nx.draw_networkx_edge_labels(N,pos,edge_labels=labels)
            plt.savefig(save2, format="PNG")


            return render_template('resultado.html', flow = str(test))
        except nx.NetworkXError:
            return render_template('erro.html', erro = "Parametros inválidos") 
        

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=False)


