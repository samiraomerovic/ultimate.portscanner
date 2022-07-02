"""
Samira Omerovic
CYBR-260-40
Week 7: Final Project
July 1, 2022

This class is the main class of the program.
This class contains the port scanning functionality as well as the menu printing and formatting
"""

import Account
import Connect
import socket
import Email

# Localhost will always be used, as it is illegal to perform this on other networks
target = "localhost"
email = ""


def format_results(open_ports: [int]) -> str:
    """
    This function formats the open ports into a string and returns it
    :param open_ports: The open ports as an array of integers to be formatted
    :return: The formatted string
    """
    format_string = "The following ports are open on your network: {}".format(open_ports)
    return format_string


def portscan(port: int) -> bool:
    """
    This function scans the given port by trying to make a connection with it.
    :param port: Port number to be checked
    :return: True if port is open, False otherwise
    """
    global target

    try:
        # Try to make a connection to the port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        sock.close()
        return True
    except:
        return False


def do_scan() -> None:
    """
    This function executes the portscan function with values from 1-1000.
    This function then proceeds to call the formatting function and the emailing function.
    This function returns to the logged in menu afterwards.
    :return: None
    """
    global email

    print('\nSCANNING')
    print('Scanning ports 1-1000...')
    open_ports = []

    # Scan ports 1 till 1000 and append open ports to array
    for i in range(1, 1000):
        if portscan(i):
            open_ports.append(i)

    msg = format_results(open_ports)
    Account.store_results(email, msg)
    Email.sendemail(msg, email)
    print('Results of the port scan sent to {}!'.format(email))
    print_logged_in()


def print_past_results() -> None:
    """
    This function prints the past records for the logged in user.
    :return: None
    """
    global email

    results = Account.get_results(email)
    str_format = "{:<20} {:8}"
    print('\n' + str_format.format('DATE', 'RESULT'))

    for result in results:
        print(str_format.format(result[1], result[0]))

    print_logged_in()


def print_logged_in() -> None:
    """
    This function prints the logged in screen, after which the user can make a choice.
    :return: None
    """
    print('\nMAIN MENU')
    valid = False
    option = 0
    while not valid:
        try:
            option = int(input('Choose 1 to SCAN or 2 to see RECORDS:\n'))
            if option < 1 or option > 2:
                print('Invalid choice, try again!')
            else:
                valid = True
        except:
            print('Invalid choice, try again!')

    if option == 1:
        do_scan()
    else:
        print_past_results()


def login() -> None:
    """
    This function prints the login menu, after which the user can enter their credentials.
    The login function in Account is used to log in.
    :return: None
    """
    global email

    print('\nLOGIN')
    valid = False
    while not valid:
        email = input('Please enter your email:\n')
        password = input('Please enter your password:\n')
        valid = Account.login(email, password)
        if not valid:
            print('Invalid credentials. Try again!')

    print_logged_in()


def register() -> None:
    """
    This function prints the register menu, after which the user can enter their credentials.
    The register function in Account is used to check and register.
    The email function is used to check whether a valid email has been provided.
    :return: None
    """
    print('\nREGISTER')
    valid = False
    while not valid:
        email = input('Please enter your email:\n')
        password = input('Please enter your password:\n')
        valid = check_email(email) and Account.register(email, password)
        if not valid:
            print('Error: Try again!')

    print('Account created!')
    login()


def check_email(input: str) -> bool:
    """
    This function checks whether a given inputted string is a valid email-address.
    :param input: String to be checked
    :return: True if input is a valid email-address, False otherwise
    """
    if ' ' in input:
        return False
    if "@" not in input:
         return False
    name, domain = input.split('@', 1)
    if '.' not in domain[1:]:
        return False
    return True


def print_menus() -> None:
    """
    This function prints the main menu upon starting the program, after which the user can decide to login or register.
    :return: None
    """
    valid = False
    option = 0
    while not valid:
        try:
            option = int(input('Choose 1 to LOGIN or 2 to REGISTER:\n'))
            if option < 1 or option > 2:
                print('Invalid choice, try again!')
            else:
                valid = True
        except:
            print('Invalid choice, try again!')

    if option == 1:
        login()
    else:
        register()


def main() -> None:
    """
    This function is used as an entry point to the program. The connection to the database and email server are made
    prior to starting the actual program.
    :return: None
    """
    try:
        Connect.connect()
        Connect.drop_database()
        Connect.setup_database()
        Email.connect()
        print('Welcome to Samira\'s Ultimate Port Scanner!\n')
        print_menus()
    except Exception as e:
        print(e)
        Connect.close()


# Entry point of the program
main()
