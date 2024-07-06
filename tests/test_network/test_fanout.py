import pytest
from boltsta.network import graph_creation_func, get_fanout_dict


@pytest.fixture
def setup_data():
    Graph = graph_creation_func("tests/test_network/andor.v")
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
        "adjacency_dict": adjacency_dict,
        "fanout_dict": fanout_dict
    }


def test_get_fanout_dict(setup_data):

    actual_fanout_dict = get_fanout_dict(setup_data["G"], setup_data["adjacency_dict"])
    assert sorted(setup_data["fanout_dict"]) == sorted(actual_fanout_dict)


if __name__ == "__main__":
    pytest.main()
