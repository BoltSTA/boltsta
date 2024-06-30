def get_fanout_dict(G, adjacency_dict):
    """
    Returns the fanout dictionary for delay calculation purposes.

    Parameters:
    G (networkx.DiGraph): The directed graph representing the design.
    adjacency_dict (dict): A dictionary where keys are nodes in the format 'node,cell_type',
                           and values are lists of fanout nodes in the same format.

    Returns:
    dict: A dictionary where the keys are any node in the design,
          and the values are lists of the key node's fanouts in the format
          'node2,cell_type,input_attr'.
    """
    fanout_dict = {}
    for key_node in adjacency_dict.keys():
        fanout_list = []
        for fanout_node in adjacency_dict[key_node]:
            key_splitted = key_node.split(',')[0]
            fanout_splitted = fanout_node.split(',')[0]
            input_attr = G[key_splitted][fanout_splitted].get('input_pin', None)
            fanout_temp = fanout_node + ',' + str(input_attr)
            fanout_list.append(fanout_temp)
        fanout_dict[key_node] = fanout_list

    return fanout_dict
