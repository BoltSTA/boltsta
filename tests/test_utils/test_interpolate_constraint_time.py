from utils import interpolate_2d_formula

def interpolate_constraint_time(
    constraint_data, related_pin_transition, constrained_pin_transition
) -> float:
    """
    Interpolates the constraint time based on transition times.

    Parameters:
        constraint_data: The data group containing constraint values.
        related_pin_transition (float): Transition time of the related pin.
        constrained_pin_transition (float): Transition time of the constrained pin.

    Returns:
        float: Interpolated constraint time.
    """
    return interpolate_2d_formula(
        constraint_data.get_array("index_1"),
        constraint_data.get_array("index_2"),
        constraint_data.get_array("values"),
        related_pin_transition,
        constrained_pin_transition,
    )

