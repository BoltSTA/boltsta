from boltsta import calculate_constraint_time
from boltsta.readers import parse_liberty_file
import pytest


@pytest.fixture(scope="module")
def lib_test():
    library = parse_liberty_file("tests/sky130_fd_sc_hd__ff_100C_1v65.lib")
    return library


def test_calculate_constraint_time_rise(lib_test):
    setup_time = calculate_constraint_time(
        cell_name="sky130_fd_sc_hd__dfrtp_2",
        checking_type="setup_checking",
        input_pin="D",
        library_name=lib_test,
        constrained_pin_transition=1.5,
        related_pin_transition=0.010,
        )
    assert setup_time == pytest.approx(0.1714661)


def test_calculate_constraint_time_invalid_checking_type(lib_test):
    with pytest.raises(ValueError):
        calculate_constraint_time(
            cell_name="sky130_fd_sc_hd__dfrtp_2",
            checking_type="invalid_checking_type",
            input_pin="D",
            library_name=lib_test,
            constrained_pin_transition=1.5,
            related_pin_transition=0.010,
            )


def test_calculate_constraint_time_negative_constrained_pin_transition(lib_test):
    with pytest.raises(ValueError):
        calculate_constraint_time(
            cell_name="sky130_fd_sc_hd__dfrtp_2",
            checking_type="setup_checking",
            input_pin="D",
            library_name=lib_test,
            constrained_pin_transition=-1.5,
            related_pin_transition=0.010,
            )


def test_calculate_constraint_time_negative_related_pin_transition(lib_test):
    with pytest.raises(ValueError):
        calculate_constraint_time(
            cell_name="sky130_fd_sc_hd__dfrtp_2",
            checking_type="setup_checking",
            input_pin="D",
            library_name=lib_test,
            constrained_pin_transition=1.5,
            related_pin_transition=-0.010,
            )


if __name__ == '__main__':
    pytest.main()