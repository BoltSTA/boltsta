import unittest
import boltsta as bs
import networkx as nx


class TestNetwork(unittest.TestCase):

    def setUp(self):
        print("setUp")
        self.file_path = "Verilog_Netlist/verilog_files/ClkDiv.v"
        self.modified_file = bs.preprocess_verilog(self.file_path)
        self.ast = bs.parse_modified_verilog(self.modified_file)
        self.input_list, self.output_list = bs.extract_input_output_ports(
            self.ast)
        pins = bs.extract_input_output_pins_of_cells(self.ast)
        self.input_pins, self.output_pins = pins
        self.ast = bs.modify_input_pins(self.ast, self.input_pins,
                                        self.output_pins)
        self.mod_input_pins = bs.extract_mod_input_pins(self.ast)
        conn_port = bs.extract_unique_internal_nodes(self.ast,
                                                     self.mod_input_pins)
        self.internal_connections, self.port_to_node_to_instance = conn_port

    def tearDown(self):
        print("tearDown\n")

    def test_build_digraph(self):
        print("test build_digraph")
    # -------------- First Test -------------- #
        print("First actual test on ClkDiv.v")
        graph_props = bs.build_digraph(self.ast, self.internal_connections,
                                       self.input_list, self.output_list,
                                       self.port_to_node_to_instance,
                                       self.mod_input_pins)
        g, pos, node_cells, edge_labels = graph_props
        # print(edge_labels)
        # Checking output data types
        self.assertIsInstance(g, nx.DiGraph)
        self.assertIsInstance(pos, dict)
        self.assertIsInstance(node_cells, dict)
        self.assertIsInstance(edge_labels, dict)

    # -------------- Second Test --------------
        print("Second Test on fake inputs")
        input_list_test = ["in1", "in2"]
        output_list_test = ["out1", "out2"]
        internal_connections_test = [['1', 'sky_AND', '2', 'sky_OR', 'X_A']]
        port_to_node_to_instance_test = {'in1': [('1', 'sky_AND', 'X_A')],
                                         'in2': [('2', 'sky_OR', 'X_B')],
                                         'out1': [('1', 'sky_AND', 'X')],
                                         'out2': [('2', 'sky_OR', 'X')],
                                         '3': [('1', 'sky_AND', 'X'),
                                               ('2', 'sky_OR', 'X_A')]}
        mod_input_pins_test = ['X_A', 'X_B']
        graph_props = bs.build_digraph(self.ast, internal_connections_test,
                                       input_list_test, output_list_test,
                                       port_to_node_to_instance_test,
                                       mod_input_pins_test)
        g_test, pos_test, node_cells_test, edge_labels_test = graph_props
        # Check output data types
        self.assertIsInstance(g_test, nx.DiGraph)
        self.assertIsInstance(pos_test, dict)
        self.assertIsInstance(node_cells_test, dict)
        self.assertIsInstance(edge_labels_test, dict)

        # --- Testing correct graph building ---
        # Check if nodes are correctly added to the graph
        expected_in_nodes = ['in1', 'in2']
        for node in expected_in_nodes:
            self.assertIn(node, g_test.nodes)
            self.assertEqual(g_test.nodes[node]['cell'], 'Input')

        expected_out_nodes = ['out1', 'out2']
        for node in expected_out_nodes:
            self.assertIn(node, g_test.nodes)
            self.assertEqual(g_test.nodes[node]['cell'], 'Output')

        expected_internal_nodes = ['1', '2']
        for node in expected_internal_nodes:
            self.assertIn(node, g_test.nodes)
            self.assertIn('sky', g_test.nodes[node]['cell'])

        # Check if edges are correctly added to the graph
        expected_edges = [('in1', '1'), ('in2', '2'), ('1', 'out1'),
                          ('2', 'out2'), ('1', '2')]
        for edge in expected_edges:
            self.assertIn(edge, g_test.edges)
        self.assertEqual(g_test.edges[('in1', '1')]['input_pin'], 'X_A')
        self.assertEqual(g_test.edges[('in2', '2')]['input_pin'], 'X_B')
        self.assertEqual(g_test.edges[('1', '2')]['input_pin'], 'X_A')
        self.assertEqual(g_test.edges[('1', 'out1')], {})
        self.assertEqual(g_test.edges[('2', 'out2')], {})

        # --- Testing correct output lists ---
        self.assertEqual(node_cells_test, {'in1': 'Input', 'in2': 'Input',
                                           'out1': 'Output', 'out2': 'Output',
                                           '1': 'sky_AND', '2': 'sky_OR'})
        self.assertEqual(edge_labels_test, {('in1', '1'): 'X_A',
                                            ('in2', '2'): 'X_B',
                                            ('1', '2'): 'X_A'})

    def test_graph_creation_func(self):
        print("test graph_creation_func")
        # -------------- First Test -------------- #
        g = bs.graph_creation_func(self.file_path)
        self.assertIsInstance(g, nx.DiGraph)


if __name__ == '__main__':
    unittest.main()
