from flask import Flask, render_template, url_for, request, redirect, send_file

import matplotlib.pyplot as plt
from io import BytesIO
import os
import networkx as nx
from networkx.algorithms.flow import dinitz
app=Flask(__name__)

# @app.route('/', methods=['POST', 'GET'])
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
        if(os.path.exists(save2)):
            os.remove(save2)
    except:
        pass


    G = nx.DiGraph()

    G.add_edge("x", "a", capacity=16 );
    G.add_edge("x", "b", capacity=13 );
    G.add_edge("a", "b", capacity=10 );
    G.add_edge("a", "c", capacity=12 );
    G.add_edge("b", "a", capacity=4 );
    G.add_edge("b", "d", capacity=14);
    G.add_edge("c", "b", capacity=9 );
    G.add_edge("c", "e", capacity=20 );
    G.add_edge("d", "c", capacity=7 );
    G.add_edge("d", "e", capacity=4);
    pos=nx.spring_layout(G) 
    nx.draw(G,pos, with_labels = True,)
    labels = nx.get_edge_attributes(G,'capacity')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.savefig(save, format="PNG")
    
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            R = dinitz(G, data['content0'], data['content2'])          
            flow_value = nx.maximum_flow_value(G,data['content0'], data['content2'])
            print (str(flow_value))
        except nx.NetworkXError:
            pass
        return render_template('resultado.html', flow = str(flow_value))

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)


