from liberty.parser import parse_liberty


# Function to parse Liberty file and extract content
def parse_liberty_file(liberty_file_path: str) -> dict:
    """
    Parse the Liberty file and extract its content.

    Args:
        liberty_file_path (str): Path to the Liberty file.

    Returns:
        dict: Parsed data from the Liberty file.
    """
    # Read Liberty file content
    with open(liberty_file_path, "r") as f:
        liberty_content = f.read()

    # Parse the Liberty content
    parsed_data = parse_liberty(liberty_content)

    return parsed_data
