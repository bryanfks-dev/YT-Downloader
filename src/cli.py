import lib
import sys
import os
from src import api

# List of menus
menus: list[str] = [
    "Download as video",
    "Download audio only",
    f"{lib.colors.FAIL}Exit{lib.colors.ENDC}",
]


def printMenus() -> None:
    """
    Function to print the menus

    :return None
    """

    # Print the header
    print(
        f"{lib.colors.BOLD}{lib.colors.OKGREEN}YT Downloader by {lib.colors.UNDERLINE}{lib.colors.OKCYAN}github@bryanfks-dev{lib.colors.ENDC}\n"
    )

    for i, menu in enumerate(menus):
        print(f"{i + 1}. {menu}")


def getChoice() -> tuple[int, list[str] | None]:
    """
    Function to get the choice from the user

    :return: The menu choice and the URLs
    """

    choiceIsValid: bool = False

    while not choiceIsValid:
        try:
            # Get the choice
            choice: int = int(
                input(f"\n{lib.colors.OKCYAN}Enter your choice: {lib.colors.ENDC}")
            )

            # Check if the choice is valid
            if choice < 1 or choice > len(menus):
                print(
                    f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} Invalid choice. Please enter a number between 1 and {len(menus)}"
                )

                continue

            # Return the choice
            menuChoice: int = choice

            choiceIsValid = True

        except:
            # Print the error message when user not inputting a number
            print(
                f"\n{lib.colors.FAIL}Invalid input. Please enter a number{lib.colors.ENDC}"
            )

            sys.exit(1)

    if menuChoice == 3:
        return menuChoice, None

    try:
        URLs: list[str] = input(
            "\nEnter URLs (Multiple URL seperated by space): "
        ).split(" ")
    except:
        sys.exit(1)

    return menuChoice, URLs


def handleChoice(choice: int, URLs: list[str]) -> None:
    """
    Function to handle the choice

    :param choice: The choice
    :param URLs: The URLs
    :return: None
    """

    match (choice):
        # Download as video
        case 1:
            for URL in URLs:
                api.downloadVideo(URL)

        # Download audio only
        case 2:
            for URL in URLs:
                api.downloadAudio(URL)

        # Exit
        case 3:
            sys.exit(0)


def run() -> None:
    """
    Function to run the CLI

    :return: None
    """
    # Clear the screen
    os.system("cls" if os.name == "nt" else "clear")

    printMenus()

    choice, URLs = getChoice()

    handleChoice(choice, URLs)
