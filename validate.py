def validate_base_parameter(value, parameter_name, min_value, max_value):
    if value is None:
        return min_value  # Default to min_value if parameter is not provided
    if min_value <= value <= max_value:
        return value
    else:
        raise ValueError(f"{parameter_name} must be between {min_value} and {max_value}")

def validate_special_parameter(value, parameter_name, reference_value, reference_name):
    if value is None:
        return reference_value + 10  # Default to reference_value + 10 if parameter is not provided
    if value >= reference_value + 10:
        return value
    else:
        raise ValueError(f"{parameter_name} must be at least 10 units greater than {reference_name}")
