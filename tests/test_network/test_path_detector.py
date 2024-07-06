import pytest
from boltsta.network import graph_creation_func
from boltsta.network import create_adjacency_dict
from boltsta.network import set_targets
from boltsta.network import set_source_nodes
from boltsta.network import find_paths_BFS
from boltsta.network import find_all_paths_non_rec_pro
from boltsta.network import get_input_attr
from boltsta.network import graph_path_handler
from boltsta.network import all_paths_info
import networkx as nx


@pytest.fixture
def setup_data():
    Graph = graph_creation_func("tests/test_network/andor.v")
    file_path = "tests/test_network/andor.v"
    targets = ['dfsbp', 'sdfrtp', 'edfxbp', 'dlxtn', 'sdfrbp', 'dfstp', 'dlclkp', 'dlxbn', 'dfxtp',
               'sdfxtp', 'sdfxbp', 'dfrtn', 'dlrtn', 'dlrbp', 'dfrbp', 'edfxt', 'sdfsbp', 'sdfbbn',
               'dlxtp', 'dlxbp', 'ff', 'dlrtp', 'dlrbn', 'sdfrtn', 'sdfstp', 'dfxbp', 'sdfbbp',
               'dfbbp', 'dfrtp', 'dfbbn', 'dd']
    expected_targets = ['sdfxbp', 'dlxtp', 'dlxtn', 'edfxbp', 'dlxbp', 'sdfrbp', 'dfstp', 'sdfbbp',
                        'dlrtn', 'dfrtp', 'dlrbp', 'sdfstp', 'sdfsbp', 'dfbbn', 'dlrtp', 'dlxbn',
                        'dfrbp', 'dlrbn', 'sdfrtp', 'dd', 'dfbbp', 'sdfxtp', 'sdfbbn', 'dfxbp',
                        'sdfrtn', 'dfxtp', 'dlclkp', 'ff', 'dfrtn', 'edfxt', 'dfsbp']
    adjacency_dict = {'_2_,sky130_fd_sc_hd__dfrtp_2': ['out2,Output'],
                      'rst,Input': ['_2_,sky130_fd_sc_hd__dfrtp_2', '_3_,sky130_fd_sc_hd__dfrtp_2'],
                      '_3_,sky130_fd_sc_hd__dfrtp_2': ['out,Output'],
                      'a,Input': ['_3_,sky130_fd_sc_hd__dfrtp_2'],
                      '_1_,sky130_fd_sc_hd__a21o_2': ['_2_,sky130_fd_sc_hd__dfrtp_2'],
                      'b,Input': ['_1_,sky130_fd_sc_hd__a21o_2'],
                      'clk,Input': ['_2_,sky130_fd_sc_hd__dfrtp_2', '_3_,sky130_fd_sc_hd__dfrtp_2'],
                      'c,Input': ['_1_,sky130_fd_sc_hd__a21o_2'], 'out2,Output': [],
                      'out,Output': ['_1_,sky130_fd_sc_hd__a21o_2']
                      }
    source_nodes_rr = ['_2_,sky130_fd_sc_hd__dfrtp_2', '_3_,sky130_fd_sc_hd__dfrtp_2']
    source_nodes_ro = ['_2_,sky130_fd_sc_hd__dfrtp_2', '_3_,sky130_fd_sc_hd__dfrtp_2']
    source_nodes_ir = ['rst,Input', 'a,Input', 'b,Input', 'clk,Input', 'c,Input']
    input_ports = ['rst,Input', 'a,Input', 'b,Input', 'clk,Input', 'c,Input']
    paths_rr = [['_3_,sky130_fd_sc_hd__dfrtp_2', 'out,Output',
                 '_1_,sky130_fd_sc_hd__a21o_2', '_2_,sky130_fd_sc_hd__dfrtp_2']]
    paths_ro = [['_2_,sky130_fd_sc_hd__dfrtp_2', 'out2,Output'],
                ['_3_,sky130_fd_sc_hd__dfrtp_2', 'out,Output']]
    paths_ir = [['rst,Input', '_2_,sky130_fd_sc_hd__dfrtp_2'],
                ['rst,Input', '_3_,sky130_fd_sc_hd__dfrtp_2'],
                ['a,Input', '_3_,sky130_fd_sc_hd__dfrtp_2'],
                ['b,Input', '_1_,sky130_fd_sc_hd__a21o_2',
                 '_2_,sky130_fd_sc_hd__dfrtp_2'],
                ['clk,Input', '_2_,sky130_fd_sc_hd__dfrtp_2'],
                ['clk,Input', '_3_,sky130_fd_sc_hd__dfrtp_2'],
                ['c,Input', '_1_,sky130_fd_sc_hd__a21o_2', '_2_,sky130_fd_sc_hd__dfrtp_2']]
    rr_attr = [[None, 'X_A2', 'Q_D']]
    ir_attr = [['X_B1', 'Q_D'], ['Q_D'], ['Q_CLK'], ['Q_CLK'],
               ['X_A1', 'Q_D'], ['Q_RESET_B'], ['Q_RESET_B']]
    ro_attr = [[None], [None]]
    fanout_dict = {'_1_,sky130_fd_sc_hd__a21o_2': ['_2_,sky130_fd_sc_hd__dfrtp_2,Q_D'],
                   'c,Input': ['_1_,sky130_fd_sc_hd__a21o_2,X_B1'],
                   '_3_,sky130_fd_sc_hd__dfrtp_2': ['out,Output,None'],
                   'a,Input': ['_3_,sky130_fd_sc_hd__dfrtp_2,Q_D'],
                   '_2_,sky130_fd_sc_hd__dfrtp_2': ['out2,Output,None'],
                   'clk,Input': ['_2_,sky130_fd_sc_hd__dfrtp_2,Q_CLK',
                                 '_3_,sky130_fd_sc_hd__dfrtp_2,Q_CLK'],
                   'b,Input': ['_1_,sky130_fd_sc_hd__a21o_2,X_A1'],
                   'rst,Input': ['_2_,sky130_fd_sc_hd__dfrtp_2,Q_RESET_B',
                                 '_3_,sky130_fd_sc_hd__dfrtp_2,Q_RESET_B'],
                   'out2,Output': [], 'out,Output': ['_1_,sky130_fd_sc_hd__a21o_2,X_A2']}

    return {
        "G": Graph,
        "file_path": file_path,
        "targets": targets,
        "adjacency_dict": adjacency_dict,
        "output_list_test": ["out1", "out2"],
        "expected_targets": expected_targets,
        "source_nodes_rr": source_nodes_rr,
        "source_nodes_ro": source_nodes_ro,
        "source_nodes_ir": source_nodes_ir,
        "input_ports": input_ports,
        "paths_rr": paths_rr,
        "paths_ro": paths_ro,
        "paths_ir": paths_ir,
        "rr_attr": rr_attr,
        "ir_attr": ir_attr,
        "ro_attr": ro_attr,
        "fanout_dict": fanout_dict,
    }


def test_create_adjacency_dict():
    print("test create_adjacency_dict")
    # -------------- First Test -------------- #
    # Creating the test graph
    G = nx.DiGraph()
    G.add_node("in1", cell="Input")
    G.add_node("in2", cell="Input")
    G.add_node("out1", cell="Output")
    G.add_node("out2", cell="Output")
    G.add_node("1", cell="sky_AND")
    G.add_node("2", cell="sky_OR")
    G.add_edge("in1", "1", input_pin="X_A")
    G.add_edge("in2", "2", input_pin="X_B")
    G.add_edge("1", "out1")
    G.add_edge("2", "out2")
    G.add_edge("1", "2", input_pin="X_A")
    adj_dict = create_adjacency_dict(G, 'cell')
    expected_adj_dict = {'1,sky_AND': ['out1,Output', '2,sky_OR'],
                         'in1,Input': ['1,sky_AND'],
                         '2,sky_OR': ['out2,Output'],
                         'in2,Input': ['2,sky_OR'],
                         'out2,Output': [],
                         'out1,Output': []}
    assert adj_dict == expected_adj_dict


def test_set_targets(setup_data):
    print("test set_targets")
    # -------------- First Test -------------- #
    ff_file = "ff_names.txt"
    ir_targets = set_targets(ff_file, "IR")
    rr_targets = set_targets(ff_file, "RR")
    ro_targets = set_targets(ff_file, "RO", setup_data["output_list_test"])
    assert ro_targets == setup_data["output_list_test"]
    assert set(ir_targets) == set(setup_data["expected_targets"])
    assert set(rr_targets) == set(setup_data["expected_targets"])


def test_set_source_nodes(setup_data):

    actual_rr = set_source_nodes(setup_data["adjacency_dict"], 'RR', setup_data["targets"])
    actual_ro = set_source_nodes(setup_data["adjacency_dict"], 'RO', setup_data["targets"],
                                 targets_file_name='ff_names.txt')
    actual_ir = set_source_nodes(setup_data["adjacency_dict"], 'IR', setup_data["targets"],
                                 input_ports=setup_data["input_ports"])
    print(actual_ro)

    assert sorted(actual_rr) == sorted(setup_data["source_nodes_rr"])
    assert sorted(actual_ro) == sorted(setup_data["source_nodes_ro"])
    assert sorted(actual_ir) == sorted(setup_data["source_nodes_ir"])

# TEST invalid_mode:
    with pytest.raises(ValueError):
        set_source_nodes(setup_data["adjacency_dict"], 'INVALID', setup_data["targets"])


def test_find_paths_BFS(setup_data):
    acutal_paths_rr = find_paths_BFS(setup_data["adjacency_dict"],
                                     setup_data["source_nodes_rr"], setup_data["targets"])
    actual_paths_ro = find_paths_BFS(setup_data["adjacency_dict"],
                                     setup_data["source_nodes_ro"], ['out,Output', 'out2,Output'])
    actual_paths_ir = find_paths_BFS(setup_data["adjacency_dict"],
                                     setup_data["source_nodes_ir"], setup_data["targets"])

    assert sorted(setup_data["paths_rr"]) == sorted(acutal_paths_rr)
    assert sorted(setup_data["paths_ro"]) == sorted(actual_paths_ro)
    assert sorted(setup_data["paths_ir"]) == sorted(actual_paths_ir)


def test_find_all_paths_non_rec_pro(setup_data):

    reg_reg = find_all_paths_non_rec_pro(setup_data["adjacency_dict"], "ff_names.txt", 'RR')
    in_reg = find_all_paths_non_rec_pro(setup_data["adjacency_dict"], "ff_names.txt", 'IR')
    reg_out = find_all_paths_non_rec_pro(setup_data["adjacency_dict"], "ff_names.txt", 'RO')

    assert sorted(setup_data["paths_rr"]) == sorted(reg_reg)
    assert sorted(setup_data["paths_ro"]) == sorted(reg_out)
    assert sorted(setup_data["paths_ir"]) == sorted(in_reg)


def test_get_input_attr(setup_data):

    rr_attr_list = get_input_attr(setup_data["G"], setup_data["paths_rr"])
    ir_attr_list = get_input_attr(setup_data["G"], setup_data["paths_ir"])
    ro_attr_list = get_input_attr(setup_data["G"], setup_data["paths_ro"])
    print(f"out: {ir_attr_list}")
    assert sorted(setup_data["rr_attr"]) == sorted(rr_attr_list)
    assert sorted(setup_data["ir_attr"]) == sorted(ir_attr_list)
    assert sorted(setup_data["ro_attr"]) == sorted(ro_attr_list)


def test_all_paths_info(setup_data):
    rr, rr_atr_list, ir, ir_atr_list, ro, ro_atr_list, adjacency_dict = all_paths_info(
                                                                        setup_data["G"])

    assert sorted(setup_data["paths_rr"]) == sorted(rr)
    assert sorted(setup_data["rr_attr"]) == sorted(rr_atr_list)
    assert sorted(setup_data["paths_ir"]) == sorted(ir)
    assert sorted(setup_data["ir_attr"]) == sorted(ir_atr_list)
    assert sorted(setup_data["paths_ro"]) == sorted(ro)
    assert sorted(setup_data["ro_attr"]) == sorted(ro_atr_list)
    assert sorted(setup_data["adjacency_dict"]) == sorted(adjacency_dict)


def test_graph_path_handler(setup_data):
    rr, rr_atr_list, ir, ir_atr_list, ro, ro_atr_list, fanout_dict = graph_path_handler(
        setup_data["file_path"])

    assert sorted(setup_data["paths_rr"]) == sorted(rr)
    assert sorted(setup_data["rr_attr"]) == sorted(rr_atr_list)
    assert sorted(setup_data["paths_ir"]) == sorted(ir)
    assert sorted(setup_data["ir_attr"]) == sorted(ir_atr_list)
    assert sorted(setup_data["paths_ro"]) == sorted(ro)
    assert sorted(setup_data["ro_attr"]) == sorted(ro_atr_list)
    assert sorted(setup_data["fanout_dict"]) == sorted(fanout_dict)


if __name__ == "__main__":
    pytest.main()
