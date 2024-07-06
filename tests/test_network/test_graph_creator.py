import pytest
from boltsta.readers import preprocess_verilog
from boltsta.readers import parse_modified_verilog
from boltsta.readers import extract_input_output_ports
from boltsta.readers import extract_input_output_pins_of_cells
from boltsta.readers import modify_input_pins
from boltsta.readers import extract_mod_input_pins
from boltsta.readers import extract_unique_internal_nodes
from boltsta.network import build_digraph
from boltsta.network import graph_creation_func
import networkx as nx


@pytest.fixture
def setup_data():
    file_path = ("tests/test_network/ClkDiv.v")
    modified_file = preprocess_verilog(file_path)
    ast = parse_modified_verilog(modified_file)
    input_list, output_list = extract_input_output_ports(ast)
    pins = extract_input_output_pins_of_cells(ast)
    input_pins, output_pins = pins
    ast = modify_input_pins(ast, input_pins, output_pins)
    eximp = extract_mod_input_pins(ast)
    mod_input_pins, port_to_node_to_instance = eximp
    internal_connections = extract_unique_internal_nodes(
        ast, mod_input_pins, port_to_node_to_instance
    )
    return {
        "file_path": file_path,
        "ast": ast,
        "input_list": input_list,
        "output_list": output_list,
        "internal_connections": internal_connections,
        "port_to_node_to_instance": port_to_node_to_instance,
        "mod_input_pins": mod_input_pins,
        "input_list_test": ["in1", "in2"],
        "output_list_test": ["out1", "out2"],
        "internal_connections_test": [["1", "sky_AND", "2", "sky_OR", "X_A"]],
        "port_to_node_to_instance_test": {
            "in1": [("1", "sky_AND", "X_A")],
            "in2": [("2", "sky_OR", "X_B")],
            "out1": [("1", "sky_AND", "X")],
            "out2": [("2", "sky_OR", "X")],
            "3": [("1", "sky_AND", "X"), ("2", "sky_OR", "X_A")],
            },
        "mod_input_pins_test": ["X_A", "X_B"]
    }


def test_build_digraph(setup_data):
    print("test build_digraph")
    # -------------- First Test -------------- #
    print("First actual test on ClkDiv.v")
    graph_props = build_digraph(
        setup_data["internal_connections"],
        setup_data["input_list"],
        setup_data["output_list"],
        setup_data["port_to_node_to_instance"],
        setup_data["mod_input_pins"],
    )
    g, pos, node_cells, edge_labels = graph_props
    # Checking output data types
    assert isinstance(g, nx.DiGraph)
    assert isinstance(pos, dict)
    assert isinstance(node_cells, dict)
    assert isinstance(edge_labels, dict)

    # -------------- Second Test --------------
    print("Second Test on fake inputs")
    graph_props = build_digraph(
        setup_data["internal_connections_test"],
        setup_data["input_list_test"],
        setup_data["output_list_test"],
        setup_data["port_to_node_to_instance_test"],
        setup_data["mod_input_pins_test"]
    )
    g_test, pos_test, node_cells_test, edge_labels_test = graph_props
    # Check output data types
    assert isinstance(g_test, nx.DiGraph)
    assert isinstance(pos_test, dict)
    assert isinstance(node_cells_test, dict)
    assert isinstance(edge_labels_test, dict)

    # --- Testing correct graph building ---
    # Check if nodes are correctly added to the graph
    expected_in_nodes = ["in1", "in2"]
    for node in expected_in_nodes:
        assert node in g_test.nodes
        assert g_test.nodes[node]["cell"] == "Input"

    expected_out_nodes = ["out1", "out2"]
    for node in expected_out_nodes:
        assert node in g_test.nodes
        assert g_test.nodes[node]["cell"] == "Output"

    expected_internal_nodes = ["1", "2"]
    for node in expected_internal_nodes:
        assert node in g_test.nodes
        assert "sky" in g_test.nodes[node]["cell"]

    # Check if edges are correctly added to the graph
    expected_edges = [
        ("in1", "1"),
        ("in2", "2"),
        ("1", "out1"),
        ("2", "out2"),
        ("1", "2"),
    ]
    for edge in expected_edges:
        assert edge in g_test.edges
    assert g_test.edges[("in1", "1")]["input_pin"] == "X_A"
    assert g_test.edges[("in2", "2")]["input_pin"] == "X_B"
    assert g_test.edges[("1", "2")]["input_pin"] == "X_A"
    assert g_test.edges[("1", "out1")] == {}
    assert g_test.edges[("2", "out2")] == {}

    # --- Testing correct output lists ---
    assert node_cells_test == {
        "in1": "Input",
        "in2": "Input",
        "out1": "Output",
        "out2": "Output",
        "1": "sky_AND",
        "2": "sky_OR",
    }
    assert edge_labels_test == {
        ("in1", "1"): "X_A",
        ("in2", "2"): "X_B",
        ("1", "2"): "X_A",
    }


def test_graph_creation_func(setup_data):
    print("test graph_creation_func")
    # -------------- First Test -------------- #
    g = graph_creation_func(setup_data["file_path"])
    assert isinstance(g, nx.DiGraph)


if __name__ == "__main__":
    pytest.main()
