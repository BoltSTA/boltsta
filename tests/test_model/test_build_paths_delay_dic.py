import pytest
from boltsta.readers import parse_liberty_file
from boltsta import extract_cell_pin_mapping 
from boltsta.model import build_paths_delay_dict

library = parse_liberty_file("tests/sky130_fd_sc_hd__ff_100C_1v65.lib")


@pytest.fixture(scope="module")
def valid_cell_pin_mapping():
    cells_info = extract_cell_pin_mapping(library)
    return cells_info


valid_paths = [['_52_,sky130_fd_sc_hd__dfrtp_2', '_39_,sky130_fd_sc_hd__xor2_2',
                '_52_,sky130_fd_sc_hd__dfrtp_2'],
               ['_52_,sky130_fd_sc_hd__dfrtp_2', '_32_,sky130_fd_sc_hd__and4_2',
                '_38_,sky130_fd_sc_hd__o211a_2', '_39_,sky130_fd_sc_hd__xor2_2',
                '_52_,sky130_fd_sc_hd__dfrtp_2']]


valid_paths_attributes = [['X_A', 'Q_D'], ['X_B', 'X_A1', 'X_B', 'Q_D']]

valid_fanout = {'_52_,sky130_fd_sc_hd__dfrtp_2': ['_32_,sky130_fd_sc_hd__and4_2,X_B',
                                                  '_33_,sky130_fd_sc_hd__or4b_2,X_B',
                                                  '_39_,sky130_fd_sc_hd__xor2_2,X_A'],
                '_39_,sky130_fd_sc_hd__xor2_2': ['_52_,sky130_fd_sc_hd__dfrtp_2,Q_D'],
                '_32_,sky130_fd_sc_hd__and4_2': ['_38_,sky130_fd_sc_hd__o211a_2,X_A1',
                                                 '_41_,sky130_fd_sc_hd__o31a_2,X_A2'],
                '_38_,sky130_fd_sc_hd__o211a_2': ['_39_,sky130_fd_sc_hd__xor2_2,X_B']
                }

expected_output = {'path1': {'_52_,sky130_fd_sc_hd__dfrtp_2': 0.483067,
                             '_39_,sky130_fd_sc_hd__xor2_2': 0.08614,
                             '_52_,sky130_fd_sc_hd__dfrtp_2,end': 0.053965},
                   'path2': {'_52_,sky130_fd_sc_hd__dfrtp_2': 0.483067,
                             '_32_,sky130_fd_sc_hd__and4_2': 0.173581,
                             '_38_,sky130_fd_sc_hd__o211a_2': 0.167906,
                             '_39_,sky130_fd_sc_hd__xor2_2': 0.094448,
                             '_52_,sky130_fd_sc_hd__dfrtp_2,end': 0.057388}}


def test_build_paths_delay_dic_value(valid_cell_pin_mapping):
    paths_delay_dic = build_paths_delay_dict(
        paths=valid_paths,
        paths_attributes=valid_paths_attributes,
        fanout=valid_fanout,
        cell_pin_mapping=valid_cell_pin_mapping,
        library=library,
        related_pin_time=0.04,
        input_transition_time=1.5,
    )
    tolerance = 0.08
    for path, delays in expected_output.items():
        assert path in paths_delay_dic
        for key, expected_value in delays.items():
            assert key in paths_delay_dic[path]
            assert paths_delay_dic[path][key] == pytest.approx(expected_value, rel=tolerance)


def test_build_paths_delay_dic_negative_related_pin_time(valid_cell_pin_mapping):
    with pytest.raises(ValueError):
        build_paths_delay_dict(
            paths=valid_paths,
            paths_attributes=valid_paths_attributes,
            fanout=valid_fanout,
            cell_pin_mapping=valid_cell_pin_mapping,
            library=library,
            related_pin_time=-0.04,
            input_transition_time=1.5,
        )


def test_build_paths_delay_dic_negative_input_transition_time(valid_cell_pin_mapping):
    with pytest.raises(ValueError):
        build_paths_delay_dict(
            paths=valid_paths,
            paths_attributes=valid_paths_attributes,
            fanout=valid_fanout,
            cell_pin_mapping=valid_cell_pin_mapping,
            library=library,
            related_pin_time=0.04,
            input_transition_time=-1.5,
        )


if __name__ == '__main__':
    pytest.main()
