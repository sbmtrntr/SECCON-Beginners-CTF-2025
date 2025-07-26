from urllib.parse import urlparse

print(
    r"""
 _   _ ____  _        ____ _               _             
| | | |  _ \| |      / ___| |__   ___  ___| | _____ _ __ 
| | | | |_) | |     | |   | '_ \ / _ \/ __| |/ / _ \ '__|
| |_| |  _ <| |___  | |___| | | |  __/ (__|   <  __/ |   
 \___/|_| \_\_____|  \____|_| |_|\___|\___|_|\_\___|_|   

allowed_hostname = "example.com"                                                         
>> """,
    end="",
)

allowed_hostname = "example.com"
user_input = input("Enter a URL: ").strip()
parsed = urlparse(user_input)

try:
    if parsed.hostname == allowed_hostname:
        print("You entered the allowed URL :)")
    elif parsed.hostname and parsed.hostname.startswith(allowed_hostname):
        print(f"Valid URL :)")
        print("Flag: ctf4b{dummy_flag}")
    else:
        print(f"Invalid URL x_x, expected hostname {allowed_hostname}, got {parsed.hostname if parsed.hostname else 'None'}")
except Exception as e:
    print("Error happened")