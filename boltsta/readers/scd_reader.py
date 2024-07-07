import re


def sdc_parser(file_path):
    """
    Takes the SDC constratints file and returns important
    constratints to be used in STA.

    Args:
        file_path (str): path to the .sdc file

    Returns:
        (dict): a dictionary containing the following constraints:
        clock_transition, clock_hold_uncertainty, clock_setup_uncertainty,
        in_out_delays, load_value, timing_derates
    """
    # Initialize variables to store results
    clock_transition = None
    clock_hold_uncertainty = None
    clock_setup_uncertainty = None
    in_out_delays = []
    load_value = None
    timing_derates = []

    # Read the content of the SDC file
    with open(file_path, 'r') as file:
        tcl_content = file.read()

    # Clock Transition
    match = re.search(r'set_clock_transition\s+([\d.]+)', tcl_content)
    if match:
        clock_transition = match.group(1)

    # Clock Setup and Hold Uncertainty
    pattern_setup = r'set_clock_uncertainty\s+-setup\s+([\d.]+)'
    pattern_hold = r'set_clock_uncertainty\s+-hold\s+([\d.]+)'
    match = re.search(pattern_hold, tcl_content)
    if match:
        clock_hold_uncertainty = match.group(1)
    match = re.search(pattern_setup, tcl_content)
    if match:
        clock_setup_uncertainty = match.group(1)

    # Input and Output Delay
    pattern = (r'set_(input|output)_delay\s+'
               r'-(max|min)\s+([\d.]+)\s+'
               r'-clock\s+\[get_clocks\s+\{[\w_]+\}\]\s+'
               r'-add_delay\s+\[get_ports\s+\{([\w_\[\]\*]+)\}\]')
    for line in tcl_content.splitlines():
        match = re.search(pattern, line.strip())
        if match:
            delay_type = match.group(1) + "_delay_" + match.group(2)
            delay_value = match.group(3)
            port = match.group(4)
            in_out_delays.append([delay_type, delay_value, port])

    # Output Load
    pattern_load = r'set_load\s+([\d.]+)\s+\[all_outputs\]'
    for line in tcl_content.splitlines():
        match = re.search(pattern_load, line.strip())
        if match:
            load_value = match.group(1)
            break

    # Timing Derates
    pattern_derate_env = r'set\s+::env\(SYNTH_TIMING_DERATE\)\s+([\d.]+)'
    pattern_derate_early = r'set_timing_derate\s+-early\s+\[expr\s+\{1-\$::env\(SYNTH_TIMING_DERATE\)\}\]'
    pattern_derate_late = r'set_timing_derate\s+-late\s+\[expr\s+\{1\+\$::env\(SYNTH_TIMING_DERATE\)\}\]'

    synth_timing_derate = None
    for line in tcl_content.splitlines():
        match_env = re.search(pattern_derate_env, line.strip())
        if match_env:
            synth_timing_derate = float(match_env.group(1))
            continue

        if re.search(pattern_derate_early, line.strip()) and synth_timing_derate is not None:
            early_derate = 1 - synth_timing_derate
            timing_derates.append([early_derate, 'early'])
            continue

        if re.search(pattern_derate_late, line.strip()) and synth_timing_derate is not None:
            late_derate = 1 + synth_timing_derate
            timing_derates.append([late_derate, 'late'])

    # Return the results as a dictionary
    return {
        'clock_transition': clock_transition,
        'clock_hold_uncertainty': clock_hold_uncertainty,
        'clock_setup_uncertainty': clock_setup_uncertainty,
        'in_out_delays': in_out_delays,
        'load_value': load_value,
        'timing_derates': timing_derates
    }
