#!/usr/bin/python
# << CODE BY HUNX04
# << MAU RECODE ??? IZIN DULU LAH,  MINIMAL TAG AKUN GITHUB MIMIN YANG MENGARAH KE AKUN INI, LEBIH GAMPANG SI PAKE FORK
# << KALAU DI ATAS TIDAK DI IKUTI MAKA AKAN MENDAPATKAN DOSA KARENA MIMIN GAK IKHLAS
# “Wahai orang-orang yang beriman! Janganlah kamu saling memakan harta sesamamu dengan jalan yang batil,” (QS. An Nisaa': 29). Rasulullah SAW juga melarang umatnya untuk mengambil hak orang lain tanpa izin.

# IMPORT MODULE

import argparse
import json
import logging
import socket
import requests
import time
import os
import phonenumbers
from phonenumbers import NumberParseException, carrier, geocoder, timezone
from sys import stderr

Bl = '\033[30m'  # VARIABLE BUAT WARNA CUYY
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Mage = '\033[1;35m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'


# utilities

# decorator for attaching run_banner to a function
def is_option(func):
    def wrapper(*args, **kwargs):
        run_banner()
        return func(*args, **kwargs)


    return wrapper


# FUNCTIONS FOR MENU
@is_option
def IP_Track():
    ip = input(f"{Wh}\n Enter IP target : {Gr}")  # INPUT IP ADDRESS
    print()
    print(f' {Wh}============= {Gr}SHOW INFORMATION IP ADDRESS {Wh}=============')
    # allow a hostname to be provided - try to resolve
    try:
        # if the input is a hostname, try resolving to IP
        try:
            socket.inet_aton(ip)
        except OSError:
            # not a plain IPv4 literal; try DNS resolve
            resolved = socket.gethostbyname(ip)
            ip = resolved
    except Exception:
        pass

    try:
        req_api = requests.get(f"http://ipwho.is/{ip}", timeout=10)
        ip_data = req_api.json()
    except requests.RequestException as e:
        print(f"{Re}Network error: {e}")
        return
    except ValueError:
        print(f"{Re}Received invalid response from API")
        return

    time.sleep(0.5)
    print(f"{Wh}\n IP target       :{Gr}", ip)
    # use .get to avoid KeyError and provide graceful fallbacks
    print(f"{Wh} Type IP         :{Gr}", ip_data.get("type", "N/A"))
    print(f"{Wh} Country         :{Gr}", ip_data.get("country", "N/A"))
    print(f"{Wh} Country Code    :{Gr}", ip_data.get("country_code", "N/A"))
    print(f"{Wh} City            :{Gr}", ip_data.get("city", "N/A"))
    print(f"{Wh} Continent       :{Gr}", ip_data.get("continent", "N/A"))
    print(f"{Wh} Continent Code  :{Gr}", ip_data.get("continent_code", "N/A"))
    print(f"{Wh} Region          :{Gr}", ip_data.get("region", "N/A"))
    print(f"{Wh} Region Code     :{Gr}", ip_data.get("region_code", "N/A"))
    lat = ip_data.get('latitude')
    lon = ip_data.get('longitude')
    if lat is not None and lon is not None:
        try:
            lat_f = float(lat)
            lon_f = float(lon)
            print(f"{Wh} Latitude        :{Gr}", lat_f)
            print(f"{Wh} Longitude       :{Gr}", lon_f)
            print(f"{Wh} Maps            :{Gr}", f"https://www.google.com/maps/@{lat_f},{lon_f},8z")
        except (TypeError, ValueError):
            print(f"{Wh} Latitude        :{Gr}", lat)
            print(f"{Wh} Longitude       :{Gr}", lon)
    else:
        print(f"{Wh} Latitude        :{Gr} N/A")
        print(f"{Wh} Longitude       :{Gr} N/A")

    print(f"{Wh} EU              :{Gr}", ip_data.get("is_eu", "N/A"))
    print(f"{Wh} Postal          :{Gr}", ip_data.get("postal", "N/A"))
    print(f"{Wh} Calling Code    :{Gr}", ip_data.get("calling_code", "N/A"))
    print(f"{Wh} Capital         :{Gr}", ip_data.get("capital", "N/A"))
    print(f"{Wh} Borders         :{Gr}", ip_data.get("borders", "N/A"))
    flag = ip_data.get("flag") or {}
    print(f"{Wh} Country Flag    :{Gr}", flag.get("emoji", "N/A"))
    conn = ip_data.get("connection") or {}
    print(f"{Wh} ASN             :{Gr}", conn.get("asn", "N/A"))
    print(f"{Wh} ORG             :{Gr}", conn.get("org", "N/A"))
    print(f"{Wh} ISP             :{Gr}", conn.get("isp", "N/A"))
    print(f"{Wh} Domain          :{Gr}", conn.get("domain", "N/A"))
    tz = ip_data.get("timezone") or {}
    print(f"{Wh} ID              :{Gr}", tz.get("id", "N/A"))
    print(f"{Wh} ABBR            :{Gr}", tz.get("abbr", "N/A"))
    print(f"{Wh} DST             :{Gr}", tz.get("is_dst", "N/A"))
    print(f"{Wh} Offset          :{Gr}", tz.get("offset", "N/A"))
    print(f"{Wh} UTC             :{Gr}", tz.get("utc", "N/A"))
    print(f"{Wh} Current Time    :{Gr}", tz.get("current_time", "N/A"))


@is_option
def phoneGW():
    User_phone = input(
        f"\n {Wh}Enter phone number target {Gr}Ex [+6281xxxxxxxxx] {Wh}: {Gr}")  # INPUT NUMBER PHONE
    default_region = "ID"  # DEFAULT NEGARA INDONESIA
    try:
        parsed_number = phonenumbers.parse(User_phone, default_region)  # VARIABLE PHONENUMBERS
    except NumberParseException as e:
        print(f"{Re}Invalid phone number: {e}")
        return

    region_code = phonenumbers.region_code_for_number(parsed_number)
    jenis_provider = carrier.name_for_number(parsed_number, "en")
    location = geocoder.description_for_number(parsed_number, "id")
    is_valid_number = phonenumbers.is_valid_number(parsed_number)
    is_possible_number = phonenumbers.is_possible_number(parsed_number)
    formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    formatted_number_for_mobile = phonenumbers.format_number_for_mobile_dialing(parsed_number, default_region,
                                                                                with_formatting=True)
    number_type = phonenumbers.number_type(parsed_number)
    timezone1 = timezone.time_zones_for_number(parsed_number)
    timezoneF = ', '.join(timezone1)

    print(f"\n {Wh}========== {Gr}SHOW INFORMATION PHONE NUMBERS {Wh}==========")
    print(f"\n {Wh}Location             :{Gr} {location}")
    print(f" {Wh}Region Code          :{Gr} {region_code}")
    print(f" {Wh}Timezone             :{Gr} {timezoneF}")
    print(f" {Wh}Operator             :{Gr} {jenis_provider}")
    print(f" {Wh}Valid number         :{Gr} {is_valid_number}")
    print(f" {Wh}Possible number      :{Gr} {is_possible_number}")
    print(f" {Wh}International format :{Gr} {formatted_number}")
    print(f" {Wh}Mobile format        :{Gr} {formatted_number_for_mobile}")
    print(f" {Wh}Original number      :{Gr} {parsed_number.national_number}")
    print(
        f" {Wh}E.164 format         :{Gr} {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)}")
    print(f" {Wh}Country code         :{Gr} {parsed_number.country_code}")
    print(f" {Wh}Local number         :{Gr} {parsed_number.national_number}")
    if number_type == phonenumbers.PhoneNumberType.MOBILE:
        print(f" {Wh}Type                 :{Gr} This is a mobile number")
    elif number_type == phonenumbers.PhoneNumberType.FIXED_LINE:
        print(f" {Wh}Type                 :{Gr} This is a fixed-line number")
    else:
        print(f" {Wh}Type                 :{Gr} This is another type of number")


@is_option
def TrackLu():
    try:
        username = input(f"\n {Wh}Enter Username : {Gr}")
        results = {}
        social_media = [
            {"url": "https://www.facebook.com/{}", "name": "Facebook"},
            {"url": "https://www.twitter.com/{}", "name": "Twitter"},
            {"url": "https://www.instagram.com/{}", "name": "Instagram"},
            {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn"},
            {"url": "https://www.github.com/{}", "name": "GitHub"},
            {"url": "https://www.pinterest.com/{}", "name": "Pinterest"},
            {"url": "https://www.tumblr.com/{}", "name": "Tumblr"},
            {"url": "https://www.youtube.com/{}", "name": "Youtube"},
            {"url": "https://soundcloud.com/{}", "name": "SoundCloud"},
            {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
            {"url": "https://www.tiktok.com/@{}", "name": "TikTok"},
            {"url": "https://www.behance.net/{}", "name": "Behance"},
            {"url": "https://www.medium.com/@{}", "name": "Medium"},
            {"url": "https://www.quora.com/profile/{}", "name": "Quora"},
            {"url": "https://www.flickr.com/people/{}", "name": "Flickr"},
            {"url": "https://www.periscope.tv/{}", "name": "Periscope"},
            {"url": "https://www.twitch.tv/{}", "name": "Twitch"},
            {"url": "https://www.dribbble.com/{}", "name": "Dribbble"},
            {"url": "https://www.stumbleupon.com/stumbler/{}", "name": "StumbleUpon"},
            {"url": "https://www.ello.co/{}", "name": "Ello"},
            {"url": "https://www.producthunt.com/@{}", "name": "Product Hunt"},
            {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
            {"url": "https://www.telegram.me/{}", "name": "Telegram"},
            {"url": "https://www.weheartit.com/{}", "name": "We Heart It"}
        ]
        headers = {"User-Agent": "Tilluthe/1.0 (+https://github.com/HunxByts)"}
        for site in social_media:
            url = site['url'].format(username)
            try:
                response = requests.get(url, headers=headers, timeout=8, allow_redirects=True)
                # some sites return 200 for non-existent users with a generic page; basic content checks
                if response.status_code == 200:
                    body = response.text.lower()
                    if any(x in body for x in ("not found", "sorry, this page", "doesn't exist", "404", "page not found")):
                        results[site['name']] = f"{Ye}Username not found{Ye}"
                    else:
                        results[site['name']] = url
                else:
                    results[site['name']] = f"{Ye}Username not found{Ye}"
            except requests.RequestException:
                results[site['name']] = f"{Ye}Could not reach site{Ye}"
    except Exception as e:
        print(f"{Re}Error : {e}")
        return

    print(f"\n {Wh}========== {Gr}SHOW INFORMATION USERNAME {Wh}==========")
    print()
    for site, url in results.items():
        print(f" {Wh}[ {Gr}+ {Wh}] {site} : {Gr}{url}")


@is_option
def showIP():
    try:
        respone = requests.get('https://api.ipify.org?format=json', timeout=6)
        data = respone.json()
        Show_IP = data.get('ip', respone.text)
    except requests.RequestException:
        print(f"{Re}Could not determine external IP")
        return

    print(f"\n {Wh}========== {Gr}SHOW INFORMATION YOUR IP {Wh}==========")
    print(f"\n {Wh}[{Gr} + {Wh}] Your IP Adrress : {Gr}{Show_IP}")
    print(f"\n {Wh}==============================================")


# OPTIONS
options = [
    {
        'num': 1,
        'text': 'IP Tracker',
        'func': IP_Track
    },
    {
        'num': 2,
        'text': 'Show Your IP',
        'func': showIP

    },
    {
        'num': 3,
        'text': 'Phone Number Tracker',
        'func': phoneGW
    },
    {
        'num': 4,
        'text': 'Username Tracker',
        'func': TrackLu
    },
    {
        'num': 0,
        'text': 'Exit',
        'func': exit
    }
]


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux
    else:
        _ = os.system('clear')


def call_option(opt):
    if not is_in_options(opt):
        raise ValueError('Option not found')
    for option in options:
        if option['num'] == opt:
            if 'func' in option:
                option['func']()
            else:
                print('No function detected')


def execute_option(opt):
    try:
        call_option(opt)
        input(f'\n{Wh}[ {Gr}+ {Wh}] {Gr}Press enter to continue')
        main()
    except ValueError as e:
        print(e)
        time.sleep(2)
        execute_option(opt)
    except KeyboardInterrupt:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}Exit')
        time.sleep(2)
        exit()


def option_text():
    text = ''
    for opt in options:
        text += f'{Wh}[ {opt["num"]} ] {Gr}{opt["text"]}\n'
    return text


def is_in_options(num):
    for opt in options:
        if opt['num'] == num:
            return True
    return False


def option():
    # BANNER TOOLS
    clear()
    stderr.writelines(f"""
       ________  __  __  __    __    __              ___________                      __           
   /_  __/ / / / / / / /   / /   / /____  _____  /_  __/ ___/__  _________  ____  / /____  _____
    / / / /_/ / / / / /   / /   / __/ _ \/ ___/   / /  \__ \/ / / / ___/ / / / / / __/ _ \/ ___/
   / / / __  / / /_/ /   / /___/ /_/  __/ /      / /  ___/ / /_/ / /  / /_/ / /_/ /_/  __/ /    
  /_/ /_/ /_/  \____/   /_____/\__/\___/_/      /_/  /____/\__,_/_/   \__, /\____/\__/\___/_/     
                                                                    /____/                        
                      ______        __      ______           __    __          
                     /_  __/__  ___/ /__   /_  __/__  ____ _/ /_  / /____  ____ 
                      / / / _ \/ _  / -_)   / / / _ \/ __ `/ __ \/ __/ _ \/ __ \
                     /_/  \___/\_,_/\__/   /_/  \___/\__,_/_.__/\__/\___/_/ /_/


              {Wh}[ + ]  C O D E   B Y  TEJA  [ + ]
    """)

    stderr.writelines(f"\n\n\n{option_text()}")


def run_banner():
    clear()
    time.sleep(1)
    stderr.writelines(f"""{Wh}
             .-.
         /   `.
        |  o  |
         \   /
          `-'
           ||
          (  )
           `'
            ||        {Wh}---------------------------------------
            ||        {Wh}| {Gr}TILLU — THE TRACER & IDENTIFIER {Wh}|
            ||        {Wh}|             {Gr}@CODE BY TEJA          {Wh}|
            ||       {Wh}---------------------------------------
        """)
    time.sleep(0.5)


def main():
    clear()
    option()
    time.sleep(1)
    try:
        opt = int(input(f"{Wh}\n [ + ] {Gr}Select Option : {Wh}"))
        execute_option(opt)
    except ValueError:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}Please input number')
        time.sleep(2)
        main()


def require_consent():
    """
    Ask user to confirm they have authorization to run OSINT queries against targets.
    This tool can be used for legitimate security testing only with permission.
    """
    print(f"{Ye}\nBy using this tool you confirm you have permission to query targets and will not use it for unlawful activity.")
    c = input(f"{Wh}Do you confirm? [y/N]: {Gr}")
    if c.strip().lower() not in ('y', 'yes'):
        print(f"{Re}Consent not given. Exiting.")
        time.sleep(1)
        exit()


def cli_entry():
    parser = argparse.ArgumentParser(prog='Tilluthe', description='Tilluthe Tracker and Identifier - IP/Phone/Username OSINT helper')
    parser.add_argument('--ip', help='Lookup information for an IP or hostname')
    parser.add_argument('--phone', help='Lookup information for a phone number (international format suggested)')
    parser.add_argument('--user', help='Lookup username across common social sites')
    parser.add_argument('--show-ip', action='store_true', help='Show your public IP')
    args = parser.parse_args()

    # if no args provided, run interactive mode
    if not any((args.ip, args.phone, args.user, args.show_ip)):
        main()
        return

    # non-interactive mode: require consent as well
    require_consent()
    if args.ip:
        # run IP_Track but pass input via injection
        print(f"{Wh}Running IP lookup for: {Gr}{args.ip}")
        # monkeypatch input for IP_Track
        _in = __builtins__['input']
        __builtins__['input'] = lambda prompt='': args.ip
        try:
            IP_Track()
        finally:
            __builtins__['input'] = _in
    if args.phone:
        _in = __builtins__['input']
        __builtins__['input'] = lambda prompt='': args.phone
        try:
            phoneGW()
        finally:
            __builtins__['input'] = _in
    if args.user:
        _in = __builtins__['input']
        __builtins__['input'] = lambda prompt='': args.user
        try:
            TrackLu()
        finally:
            __builtins__['input'] = _in
    if args.show_ip:
        showIP()


if __name__ == '__main__':
    try:
        require_consent()
        cli_entry()
    except KeyboardInterrupt:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}Exit')
        time.sleep(2)
        exit()
