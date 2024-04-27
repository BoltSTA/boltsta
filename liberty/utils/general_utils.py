import numpy as np

# Function to concatenate pin name and related pin with an underscore
def concatenate_pins(pin_name: str, related_pin: str) -> str:
    """
    Concatenates pin name and related pin with an underscore.

    Args:
        pin_name (str): Name of the pin.
        related_pin (str): Name of the related pin.

    Returns:
        str: Concatenated string of pin name and related pin with an underscore.
    """
    # Convert EscapedString objects to regular strings
    pin_name = str(pin_name)
    related_pin = str(related_pin)
    # Remove double quotes from pin names
    pin_name = pin_name.strip('"')
    related_pin = related_pin.strip('"')
    return f"{pin_name}_{related_pin}"



# Function to interpolate 2D data using a provided formula
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
