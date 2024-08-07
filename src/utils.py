def strIsEmpty(string: str) -> bool:
    """
    Check if a string is empty
    """
    # Check if the string is really
    # empty
    if string == "":
        return True

    # Check if the string is only spaces
    if string.isspace():
        return True

    return False
