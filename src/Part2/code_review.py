############
#
# Code Review
#
# Please do a code review for the following snippet.
# Add your review suggestions inline as python comments
#
############

def get_value(data, key, default, lookup=None, mapper=None):
    """
    Finds the value from data associated with key, or default if the
    key isn't present.
    If a lookup enum is provided, this value is then transformed to its
    enum value.
    If a mapper function is provided, this value is then transformed
    by applying mapper to it.
    """
    # Suggestion: Use dict.get() to avoid KeyError if the key doesn't exist
    """return_value = data.get(key, default)"""
    return_value = data[key]
    if return_value is None or return_value == "":
        return_value = default
    if lookup:
        # Check if the return_value is in the lookup dictionary before attempting the lookup
#         if return_value in lookup:
#             return_value = lookup[return_value]
        return_value = lookup[return_value] 
        
    if mapper:
#         try:
#              Apply the mapper function to the return_value
#             return_value = mapper(return_value)
#         except Exception as e:
#              Handle any exceptions that might occur during the mapping
#             print(f"Error applying mapper function: {e}")
#             return_value = default
        return_value = mapper(return_value)
    return return_value


def ftp_file_prefix(namespace):
    """
    Given a namespace string with dot-separated tokens, returns the
    string withvthe final token replaced by 'ftp'.
    Example: a.b.c => a.b.ftp   

    """
    """
    Consider adding a check to ensure that 'namespace' is a string.
    if not isinstance(namespace, str):
        raise TypeError("Expected a string input")
        
    # Ensure the namespace has at least one dot; otherwise, splitting and slicing could fail.
    if '.' not in namespace:
        raise ValueError("Namespace must contain at least one dot-separated token")    
    """
    return ".".join(namespace.split(".")[:-1]) + '.ftp'

def string_to_bool(string):
    """
    Returns True if the given string is 'true' (case-insensitive),
    False if it is 'false' (case-insensitive).
    Raises ValueError for any other input.
    """

    # Suggestion: It would be more efficient to call string.lower() once and store it in a variable,
    # rather than calling it multiple times. This avoids unnecessary repetition and improves readability.
    lower_string = string.lower()

    if lower_string == 'true':
        return True

    if lower_string == 'false':
        return False

    raise ValueError(f'String "{string}" is neither "true" nor "false" (case-insensitive).')


def config_from_dict(dict):
    """
    Given a dict representing a row from a namespaces csv file,
    returns a DAG configuration as a pair whose first element is the
    DAG name
    and whose second element is a dict describing the DAG's properties
    """
    
    # Suggestion: Before proceeding, check if the 'Namespace' key exists in the dictionary.
    # If the key is not found, raise an informative error to avoid potential issues later on.
    if 'Namespace' not in dict:
        raise KeyError("The 'Namespace' key is missing from the input dictionary.")
    namespace = dict['Namespace']
    # Suggestion: Consider using a more descriptive variable name than 'dict'
    # This will make the function more readable
    config = {
        "earliest_available_delta_days": 0,
        "lif_encoding": 'json',
        "earliest_available_time": get_value(dict, 'Available Start Time', '07:00'),
        "latest_available_time": get_value(dict, 'Available End Time', '08:00'),
        "require_schema_match": get_value(dict, 'Requires Schema Match', 'True', mapper=string_to_bool),
        "schedule_interval": get_value(dict, 'Schedule', '1 7 * * * '),
        "delta_days": get_value(dict, 'Delta Days', 'DAY_BEFORE', lookup=DeltaDays),
        "ftp_file_wildcard": get_value(dict, 'File Naming Pattern', None),
        "ftp_file_prefix": get_value(dict, 'FTP File Prefix', ftp_file_prefix(namespace)),
        "namespace": namespace
    }
    # Hardcoded Values: There are a few hardcoded values, such as "earliest_available_delta_days": 0 
    # and "lif_encoding": 'json'. If these values are subject to change or need to be configured, consider passing them as parameters or defining them as constants.
    return (dict['Airflow DAG'], config)