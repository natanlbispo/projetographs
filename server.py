from flask import Flask, render_template, url_for, request, redirect, send_file

import matplotlib.pyplot as plt
from io import BytesIO
import os
import networkx as nx
from networkx.algorithms.flow import dinitz
from dinic import MaxFlow
C = [[ 0, 16, 13, 0, 0, 0 ],  # s
     [ 0, 0, 10, 12, 0, 0 ],  # o
     [ 0, 4, 0, 0, 14, 0 ],  # p
     [ 0, 0, 9, 0, 0, 20 ],  # q
     [ 0, 0, 0, 7, 0, 4],  # r
     [ 0, 0, 0, 0, 0, 3 ]]  # t

app=Flask(__name__)

@app.route('/',  methods=['POST', 'GET'])
def index():
    figure = plt.figure()
    path2 = os.getcwdb();
    print()
    path = os.path.abspath(__file__).strip('server.py')
    save = path + '/static/Graph.png'
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
    pos=nx.spring_layout(G) 
    nx.draw(G,pos, with_labels = True,)
    labels = nx.get_edge_attributes(G,'capacity')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.savefig(save, format="PNG")
    
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            test = MaxFlow(C,int(data['content0']),int(data['content2']))
            print (test)
        except nx.NetworkXError:
            pass       
        
        return render_template('resultado.html', flow = str(test), entrada="x", sainda="y")

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)


