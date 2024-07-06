import pytest 

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



def test_concatenate_pins_no_quotes():
    assert concatenate_pins('pin1', 'pin2') == 'pin1_pin2'

def test_concatenate_pins_with_quotes():
    assert concatenate_pins('"pin1"', '"pin2"') == 'pin1_pin2'

def test_concatenate_pins_mixed_quotes():
    assert concatenate_pins('pin1', '"pin2"') == 'pin1_pin2'
    assert concatenate_pins('"pin1"', 'pin2') == 'pin1_pin2'

def test_concatenate_pins_empty_strings():
    assert concatenate_pins('', '') == '_'
    assert concatenate_pins('pin1', '') == 'pin1_'
    assert concatenate_pins('', 'pin2') == '_pin2'

def test_concatenate_pins_with_spaces():
    assert concatenate_pins(' pin1 ', ' pin2 ') == 'pin1_pin2'
    assert concatenate_pins('" pin1 "', '" pin2 "') == 'pin1_pin2'

def test_concatenate_pins_with_none():
    with pytest.raises(TypeError):
        concatenate_pins(None, 'pin2')
    with pytest.raises(TypeError):
        concatenate_pins('pin1', None)

def test_concatenate_pins_with_special_characters():
    assert concatenate_pins('pin-1', 'pin_2') == 'pin-1_pin_2'
    assert concatenate_pins('pin@1', 'pin#2') == 'pin@1_pin#2'

def test_concatenate_pins_with_long_strings():
    long_string1 = 'a' * 1000
    long_string2 = 'b' * 1000
    assert concatenate_pins(long_string1, long_string2) == f"{long_string1}_{long_string2}"

def test_concatenate_pins_with_numeric_strings():
    assert concatenate_pins('123', '456') == '123_456'
    assert concatenate_pins('"123"', '"456"') == '123_456'

def test_concatenate_pins_whitespace_only():
    assert concatenate_pins('   ', '   ') == '_'
    assert concatenate_pins('   ', 'pin2') == '_pin2'
    assert concatenate_pins('pin1', '   ') == 'pin1_'

# Run the tests
if __name__ == "__main__":
    pytest.main()
