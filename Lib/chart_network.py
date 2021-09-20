import os
import pandas as pd
import json
import plotly.graph_objects as go
import plotly.io as pio

def online_network_analysis(df_anb, file_out_path, num_of_occurrence=2):
    import networkx as nx
    from networkx import nx_pydot

    import matplotlib.pyplot as plt

    df_nx_graph = nx.Graph()

    try:
        df_anb_count = df_anb.value_counts(subset=['name', 'value'])
        df_anb_count = df_anb_count.reset_index()
        df_anb_count = df_anb_count.rename(columns={df_anb_count.columns[0]: 'name',
                                                    df_anb_count.columns[1]: 'value',
                                                    df_anb_count.columns[2]: 'occurrence'})

        df_anb_count = df_anb_count[df_anb_count['occurrence'] >= num_of_occurrence]

        type_of = ['PERSON', 'GPE', 'NORP', 'ORG']
        
        edge_list = []
             
        for index, row in df_anb_count.iterrows():
            ents_split = row['name'].split(' - ')
            entitys_name = ents_split[0]
            entitys_type = ents_split[1]
            val_split = row['value'].split(' - ')
            val_name = val_split[0]
            value_type = val_split[1]
            max_occurences = df_anb_count.occurrence.max()
            if entitys_type in type_of:
                edge_tup = (entitys_name,val_name, {"occurrence":max_occurences})
                edge_list.append(edge_tup)
        
        df_nx_graph.add_edges_from(edge_list)
        pos=nx.spring_layout(df_nx_graph)
        nx.set_node_attributes(df_nx_graph, pos, 'coord')
        
        edge_x = []
        edge_y = []
        for edge in df_nx_graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)


        node_x = []
        node_y = []
        for node in pos:
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)


        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='# Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))

        node_adjacencies = []
        node_text = []
        for node, adjacencies in enumerate(df_nx_graph.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            node_text.append(adjacencies[0])

        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text

    except Exception as e:
        print("%s \nUnable to create Network Analysis" % e)
        pass

    fig = go.Figure(data=[edge_trace, node_trace],
            layout=go.Layout(
            title='<br>Network graph',
            titlefont_size=16,
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002 ) ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
            )
    
    
    file_out_path = os.path.dirname(file_out_path)
    file_out_path = os.path.join(file_out_path,'plot_data.html')
    pio.write_html(fig, file=file_out_path, auto_open=False)

    return
