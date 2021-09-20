import os
import pandas as pd
import json

def pynax_chart_builder():
    import pyanx

    chart = pyanx.Pyanx()

    tyrion = chart.add_node(entity_type='Person', label='Tyrion')  # n0
    tywin = chart.add_node(entity_type='Person', label='Tywin')  # n1
    jaime = chart.add_node(entity_type='Person', label='Jaime')  # n2
    cersei = chart.add_node(entity_type='Woman', label='Cersei')  # n3

    chart.add_edge(tywin, tyrion, 'Father of')
    chart.add_edge(jaime, tyrion, 'Brother of')
    chart.add_edge(cersei, tyrion, 'Sister of')

    probe = 'test_probe.anx'

    print(pyanx.__file__)
    chart.create(probe)
    return


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
            print(max_occurences)
            if entitys_type in type_of:
                edge_tup = (entitys_name,val_name, {"occurrence":max_occurences})
                edge_list.append(edge_tup)
        
        df_nx_graph.add_edges_from(edge_list)
        # G = nx_pydot.graphviz_layout(df_nx_graph)
        occurrence = [1 if df_nx_graph[u][v] == {} else df_nx_graph[u][v]['occurrence'] for u,v in df_nx_graph.edges()]
        nx.draw_shell(df_nx_graph, width=occurrence, with_labels=True)
        plt.savefig(os.path.join(file_out_path, "data.png"))
        plt.show()

    except Exception as e:
        print("%s \nmoving on" % e)
        pass

    return

if __name__=='__main__':
    
    json_data_save_path = os.path.join("C:\\Users\\wirksc\\NTC Tools\\NLP_Project\\data\\e2b9a4a429008824c88bb99f5a843a193047c3c7e173b14216f7b1690e45b581\\downloaded\\data.json")
    file_out_path = os.path.dirname(json_data_save_path)
    with open(json_data_save_path, 'r') as fp:
        json_data_save = json.load(fp)
    if len(json_data_save) > 1:
        df_data = pd.DataFrame(pd.json_normalize(json_data_save).squeeze().reset_index())
        df_data = df_data.rename(columns={df_data.columns[0]: "name", df_data.columns[1]: "value"})
        df_data = df_data.explode("value").reset_index(drop=True)
    else:
        df_data = pd.DataFrame(json_data_save)
    
    online_network_analysis(df_anb=df_data, file_out_path=file_out_path)
