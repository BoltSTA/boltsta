import pytest 
import numpy as np


# Function to find the two nearest values in an array to a given value
def find_nearest_index(arr: list, value: float) -> tuple:
    """
    Find the two nearest values in an array to a given value.

    Parameters:
        arr (list): Array of values.
        value (float): Target value.

    Returns:
        tuple: The two nearest values.
    """
    idx = (np.abs(np.array(arr) - value)).argsort()[:2]
    return arr[idx[0]], arr[idx[1]]





def test_empty_array():
  """Tests the function with an empty array."""
  with pytest.raises(ValueError):
    find_nearest_index([], 5)

def test_single_element():
  """Tests the function with a single element array."""
  arr = [10]
  result = find_nearest_index(arr, 10)
  assert result == (10, 10)

def test_basic_case():
  """Tests the function with a basic array and target value."""
  arr = [5, 8, 2, 9, 1]
  result = find_nearest_index(arr, 6)
  assert result == (5, 8)

def test_duplicates():
  """Tests the function with an array containing duplicates."""
  arr = [3, 1, 2, 1, 5]
  result = find_nearest_index(arr, 2)
  # Two possible valid outputs due to duplicates
  assert result in [(1, 2), (2, 3)]

def test_edge_case_target_equal_to_min():
  """Tests the function with a target value equal to the minimum value."""
  arr = [5, 2, 8, 1, 9]
  result = find_nearest_index(arr, 1)
  assert result == (1, 2)

def test_edge_case_target_equal_to_max():
  """Tests the function with a target value equal to the maximum value."""
  arr = [3, 7, 1, 9, 4]
  result = find_nearest_index(arr, 9)
  assert result == (7, 9)

def test_target_less_than_min():
  """Tests the function with a target value less than the minimum value."""
  arr = [5, 8, 2, 9, 1]
  result = find_nearest_index(arr, 0)
  assert result == (1, 2)

def test_target_greater_than_max():
  """Tests the function with a target value greater than the maximum value."""
  arr = [3, 7, 1, 9, 4]
  result = find_nearest_index(arr, 10)
  assert result == (7, 9)

def test_all_elements_equal():
  """Tests the function with an array where all elements are equal."""
  arr = [5, 5, 5, 5]
  result = find_nearest_index(arr, 5)
  assert result == (5, 5)  # Any two elements are the same distance

def test_nan_value():
  """Tests the function with an array containing NaN."""
  arr = [3, 1, np.nan, 7]
  result = find_nearest_index(arr, 5)
  assert result == (3, 7)  # Ignore NaN in distance calculation
