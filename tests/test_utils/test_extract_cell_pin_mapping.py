from utils import concatenate_pins
from liberty.types import *
def extract_cell_pin_mapping(library: str) -> dict:
    """
    Extracts cell names along with their respective pin names from the Liberty library.

    Args:
        library (LibertyLibrary): Parsed Liberty library.

    Returns:
        dict: Dictionary where keys are cell names and values are dictionaries of input pins with timing information.
    """
    cell_pin_mapping = {}

    # Loop through all cells in the library
    for cell_group in library.get_groups("cell"):
        cell_name = cell_group.args[0]
        input_pins_with_timing = {}

        # Loop through all pins of the cell
        for pin_group in cell_group.get_groups("pin"):
            pin_name = pin_group.args[0]

            # Loop through timing tables for this pin
            for timing_group in pin_group.get_groups("timing"):
                related_pin = timing_group["related_pin"]
                full_pin_name = concatenate_pins(pin_name, related_pin)
                timing = select_timing_group(pin_group, related_pin=related_pin)
                input_pins_with_timing[full_pin_name] = timing

        # Store cell name and its input pins with timing information in the dictionary
        cell_pin_mapping[cell_name] = input_pins_with_timing

    return cell_pin_mapping


from collections import OrderedDict  # For ordered dictionary comparison

def test_empty_library():
  """Tests the function with an empty library."""
  empty_library = {}  # Simulate an empty Liberty library
  cell_pin_mapping = extract_cell_pin_mapping(empty_library)
  assert cell_pin_mapping == {}  # Empty dictionary expected

def test_single_cell_single_pin():
  """Tests the function with a library containing a single cell with a single pin."""
  library = {
      "cells": {
          "cell1": {
              "pins": {"pin1": {"timing": {"related_pin": "clk", "data": {"setup": 1.0}}}}
          }
      }
  }
  expected_mapping = {
      "cell1": {"clk": {"setup": 1.0}}
  }
  cell_pin_mapping = extract_cell_pin_mapping(library)
  assert cell_pin_mapping == expected_mapping  # Order-independent comparison

def test_multiple_cells_multiple_pins():
  """Tests the function with a library containing multiple cells and pins with timing."""
  library = {
      "cells": {
          "cell1": {
              "pins": {
                  "data_in": {
                      "timing": {"related_pin": None, "data": {"hold": 2.0}}
                  },
                  "clock": {"timing": {"related_pin": "data_in", "data": {"setup": 1.5}}}
              }
          },
          "cell2": {
              "pins": {"output": {"timing": {"related_pin": None, "data": {"rise_delay": 3.0}}}}
          }
      }
  }
  expected_mapping = {
      "cell1": {"data_in": {"hold": 2.0}, "data_in:clock": {"setup": 1.5}},
      "cell2": {"output": {"rise_delay": 3.0}}
  }
  cell_pin_mapping = extract_cell_pin_mapping(library)
  # Order-independent comparison since dictionaries are unordered
  assert cell_pin_mapping == OrderedDict(expected_mapping)

def test_multiple_timing_groups_per_pin():
  """Tests the function with a pin having multiple timing groups."""
  library = {
      "cells": {
          "cell1": {
              "pins": {
                  "data": {
                      "timing": [
                          {"related_pin": None, "data": {"hold": 2.0}},
                          {"related_pin": "clock", "data": {"setup": 1.5}}
                      ]
                  }
              }
          }
      }
  }
  expected_mapping = {"cell1": {"data": {"hold": 2.0}, "data:clock": {"setup": 1.5}}}
  cell_pin_mapping = extract_cell_pin_mapping(library)
  assert cell_pin_mapping == OrderedDict(expected_mapping)
