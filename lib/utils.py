import os


def strIsEmpty(string: str) -> bool:
    """
    Check if a string is empty

    :param string: The string to check
    :return: True if the string is empty, False otherwise
    """

    # Check if the string is really
    # empty
    if string == "":
        return True

    # Check if the string is only spaces
    if string.isspace():
        return True

    return False


def createDir(path: str) -> None:
    """
    Create the directory if it does not exist

    :param path: The path of the directory
    :return: None
    """

    # Check if the directory exists
    if not os.path.exists(path):
        os.makedirs(path)


def removeExtension(fileName: str) -> str:
    """
    Remove the extension from the file name

    :param fileName: The file name
    :return: The file name without the extension
    """

    return fileName[: fileName.index(".")]


def getFileCount(pathWithoutFileName: str, fileNameWithoutExt: str) -> int:
    """
    Get the number of files with the same name

    :param: pathWithoutFileName: The path without the file name
    :param: fileNameWithoutExt: The file name without the extension
    :return: The number of files contains the same name
    """

    return len(
        [
            file
            for file in os.listdir(pathWithoutFileName)
            if file.startswith(fileNameWithoutExt)
        ]
    )
