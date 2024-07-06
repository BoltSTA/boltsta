import pytest
from boltsta.readers import find_partial_match


@pytest.fixture(scope="module")
def setup_test_data():
    """
    Fixture to setup test data for find_partial_match testing.

    Returns:
        tuple: Tuple containing nets list and input_list.
    """
    nets = ['IN1', 'IN2', 'IN3', '_1_', 'D1', 'IN3', 'IN5', 'IN4', '_0_',
            'D3', 'IN2', 'IN3', 'D2', 'CLK', 'OUT3', 'D2', 'OUT2', 'D1', 'OUT1']
    input_list = ['CLK', 'IN1', 'IN2', 'IN3', 'IN4', 'IN5']
    return nets, input_list


@pytest.mark.parametrize("nets, input_list, expected_matching_elements", [
    (['IN1', 'IN2', 'IN3', '_1_', 'D1', 'OUT'], ['IN1', 'IN3'], ['IN1', 'IN3']),  # Test case 1
    (['A', 'B', 'C'], ['A', 'D'], ['A']),  # Test case 2
])
def test_find_partial_match(nets, input_list, expected_matching_elements):
    """
    Test case for find_partial_match function.

    Args:
        nets (list): List of nets to search.
        input_list (list): List of inputs to match against nets.
        expected_matching_elements (list): Expected list of matching elements.

    Asserts:
        Compares sorted actual matching elements with sorted expected matching elements.
    """
    # Find partial matches in nets
    actual_matching_elements = find_partial_match(nets, input_list)
    # Assert equal after sorting
    assert sorted(actual_matching_elements) == sorted(expected_matching_elements)


if __name__ == '__main__':
    pytest.main()
