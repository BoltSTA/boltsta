import pytest
import numpy as np
from utils import find_nearest_index


def interpolate_2d_formula(
    index_1_values: list,
    index_2_values: list,
    table_values: np.ndarray,
    x0: float,
    y0: float,
) -> float:
    """
    Interpolates 2D data using the formula in the Static Timing Analysis for
    Nanometer Designs A Practical Approach book .

    Parameters:
        index_1_values (list): Values of index_1.
        index_2_values (list): Values of index_2.
        table_values (np.ndarray): Corresponding table values.
        x0 (float): Target value of index_1 for interpolation.
        y0 (float): Target value of index_2 for interpolation.

    Returns:
        float: Interpolated value using the provided formula.
    """
    # Find the nearest index values
    x1, x2 = find_nearest_index(index_1_values[0], x0)
    y1, y2 = find_nearest_index(index_2_values[0], y0)

    # Calculate interpolation parameters
    x01 = (x0 - x1) / (x2 - x1)
    x20 = (x2 - x0) / (x2 - x1)
    y01 = (y0 - y1) / (y2 - y1)
    y20 = (y2 - y0) / (y2 - y1)

    # Find corresponding table values using numpy.where()
    (i1,) = np.where(index_1_values[0] == x1)
    (i2,) = np.where(index_2_values[0] == y1)
    T11 = table_values[i1, i2]

    (i2,) = np.where(index_2_values[0] == y2)
    T12 = table_values[i1, i2]

    (i1,) = np.where(index_1_values[0] == x2)
    (i2,) = np.where(index_2_values[0] == y1)
    T21 = table_values[i1, i2]

    (i2,) = np.where(index_2_values[0] == y2)
    T22 = table_values[i1, i2]

    # Perform interpolation using the provided formula
    interpolated_value = (
        x20 * y20 * T11 + x20 * y01 * T12 + x01 * y20 * T21 + x01 * y01 * T22
    )

    return interpolated_value



def test_basic_interpolation():
  """Tests the function with a basic 2D data table and target point."""
  index_1_values = [1, 2, 3]
  index_2_values = [4, 5, 6]
  table_values = np.array([[10, 15, 20], [20, 25, 30], [30, 35, 40]])
  x0, y0 = 1.5, 4.7

  interpolated_value = interpolate_2d_formula(index_1_values, index_2_values, table_values, x0, y0)
  assert np.isclose(interpolated_value, 23.25)  # Allow for floating-point precision

def test_edge_case_target_on_grid_point():
  """Tests the function with a target point on a grid point."""
  index_1_values = [1, 2, 3]
  index_2_values = [4, 5, 6]
  table_values = np.array([[10, 15, 20], [20, 25, 30], [30, 35, 40]])
  x0, y0 = 2, 5

  interpolated_value = interpolate_2d_formula(index_1_values, index_2_values, table_values, x0, y0)
  assert interpolated_value == 25  # Exact value since on a grid point

def test_target_outside_data_range():
  """Tests the function with a target point outside the data range."""
  index_1_values = [1, 2, 3]
  index_2_values = [4, 5, 6]
  table_values = np.array([[10, 15, 20], [20, 25, 30], [30, 35, 40]])
  x0, y0 = 3.5, 7

  # How to handle out-of-range targets depends on the specific use case.
  # This test checks for returning a defined value (e.g., NaN or raising an exception).
  interpolated_value = interpolate_2d_formula(index_1_values, index_2_values, table_values, x0, y0)
  assert not np.isnan(interpolated_value)  # Or raise an appropriate exception

def test_all_values_equal():
  """Tests the function with a data table where all values are equal."""
  index_1_values = [1, 2, 3]
  index_2_values = [4, 5, 6]
  table_values = np.ones((3, 3)) * 10  # All values are 10
  x0, y0 = 1.5, 4.7

  interpolated_value = interpolate_2d_formula(index_1_values, index_2_values, table_values, x0, y0)
  assert interpolated_value == 10  # Any interpolation will result in 10

def test_nan_in_table_values():
  """Tests the function with NaN values in the data table."""
  index_1_values = [1, 2, 3]
  index_2_values = [4, 5, 6]
  table_values = np.array([[10, 15, np.nan], [20, 25, 30], [30, 35, 40]])
  x0, y0 = 1.5, 4.7

  # How to handle NaN in the table depends on the specific use case.
  # This test checks for defined behavior (e.g., ignoring NaN or propagating it).
  interpolated_value = interpolate_2d_formula(index_1_values, index_2_values, table_values, x0, y0)
  assert not np.isnan(interpolated_value)  # Or check for specific behavior
