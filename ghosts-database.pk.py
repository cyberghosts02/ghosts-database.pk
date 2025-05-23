import argparse
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

banner = f"""{Fore.CYAN}<============================================================================>|
{Fore.RED}+------------------------------------------------------------------------+ ||
|+|                                                                                                                           |+|
|+|                                                                                                                           |+|
|+|           {Fore.RED}                        {Fore.MAGENTA}                                                                |+|
|+|   ******  **    ** ******   ******** *******           ********  **      **   *******    ******** **********  ********    |+|
|+|  **////**//**  ** /*////** /**///// /**////**         **//////**/**     /**  **/////**  **////// /////**///  **//////     |+|
|+| **    //  //****  /*   /** /**      /**   /**        **      // /**     /** **     //**/**           /**    /**           |+|
|+|/**         //**   /******  /******* /*******        /**         /**********/**      /**/*********    /**    /*********    |+|
|+|/**          /**   /*//// **/**////  /**///**        /**    *****/**//////**/**      /**////////**    /**    ////////**    |+|
|+|//**    **   /**   /*    /**/**      /**  //**       //**  ////**/**     /**//**     **        /**    /**           /**    |+|
|+| //******    /**   /******* /********/**   //**       //******** /**     /** //*******   ********     /**     ********     |+|
|+|  //////     //    ///////  //////// //     //         ////////  //      //   ///////   ////////      //     ////////|     |+|
|+|                                                                   v1.1 |+|
|+|                                                                        |+|
|+|{Fore.WHITE}  "CYBER GHOSTS DON'T ATTACK TWICE -- ONCE IS ENOUGH TO MAKE THE SYSTEM FORGET IT EVER LIVED."           |+|
{Fore.YELLOW}+------------------------------------------------------------------------+ |
{Fore.CYAN}<============================================================================>|
>GitHub    : https://github.com/cyberghosts02/                                        ||
>LinkedIn  : https://www.linkedin.com/SOON                                 ||
>Instagram : https://www.instagram.com/SOON                               ||
<============================================================================>|
Crafted by [AWAN] -
<============================================================================>"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_phone_number(number):
    if number.startswith("0") and len(number) == 11 and number.isdigit():
        return True
    else:
        print(f"{Fore.RED}Error: The phone number must start with 0 and be 11 digits long.")
        return False

def validate_cnic(cnic):
    if len(cnic) == 13 and cnic.isdigit():
        return True
    else:
        print(f"{Fore.RED}Error: CNIC should be 13 digits long and without dashes.")
        return False

def fetch_cnic_from_sim_owner(number):
    url = "https://sim-owner-details.info/wp-admin/admin-ajax.php"
    data = {"action": "handle_sim_owner_search", "mobileNumber": number}
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            json_response = response.json()
            if json_response.get('success') and 'results' in json_response:
                return json_response['results'].get('CNIC')
    except requests.exceptions.RequestException:
        print(f"{Fore.RED}Connection error with sim-owner-details.info")
    return None

def fetch_details_from_numberdetails(cnic):
    url = "https://numberdetails.xyz/"
    headers = {
        "Host": "numberdetails.xyz",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://numberdetails.xyz/"
    }
    data = {"searchinfo": cnic}
    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.find_all('div', class_='result-card')
            table = []
            for card in cards:
                name = card.find('label', string='FULL NAME').find_next('div').text.strip()
                phone = card.find('label', string='PHONE #').find_next('div').text.strip()
                address = card.find('label', string='ADDRESS').find_next('div').text.strip()
                table.append([name, phone, cnic, address])
            return table
    except requests.exceptions.RequestException:
        print(f"{Fore.RED}Connection error with numberdetails.xyz")
    return None

def main():
    clear_screen()
    print(banner)
    while True:
        user_input = input(f"{Fore.CYAN}\nEnter Phone Number or CNIC (or type 'exit'): ").strip()
        if user_input.lower() == 'exit':
            print(f"{Fore.GREEN}Goodbye [FOR ANY HELP OR PAID SERVICES alpha-0.2-pk@proton.me ]!")
            break
        if validate_phone_number(user_input):
            cnic = fetch_cnic_from_sim_owner(user_input)
            if cnic:
                details = fetch_details_from_numberdetails(cnic)
                if details:
                    print(tabulate(details, headers=["Name", "Phone", "CNIC", "Address"], tablefmt="grid"))
                else:
                    print(f"{Fore.RED}No data found.")
        elif validate_cnic(user_input):
            details = fetch_details_from_numberdetails(user_input)
            if details:
                print(tabulate(details, headers=["Name", "Phone", "CNIC", "Address"], tablefmt="grid"))
            else:
                print(f"{Fore.RED}No data found.")
        else:
            print(f"{Fore.RED}Invalid input. Enter 11-digit phone number or 13-digit CNIC.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}User interrupted the program. Exiting gracefully.")
