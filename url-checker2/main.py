from urllib.parse import urlparse

print(
    r"""
 _   _ ____  _        ____ _               _            ____  
| | | |  _ \| |      / ___| |__   ___  ___| | _____ _ _|___ \ 
| | | | |_) | |     | |   | '_ \ / _ \/ __| |/ / _ \ '__|__) |
| |_| |  _ <| |___  | |___| | | |  __/ (__|   <  __/ |  / __/ 
 \___/|_| \_\_____|  \____|_| |_|\___|\___|_|\_\___|_| |_____|
                                                              
allowed_hostname = "example.com"                                                         
>> """,
    end="",
)

allowed_hostname = "example.com"
user_input = input("Enter a URL: ").strip()
parsed = urlparse(user_input)

# Remove port if present
input_hostname = None
if ':' in parsed.netloc:
    input_hostname = parsed.netloc.split(':')[0]

try:
    if parsed.hostname == allowed_hostname:
        print("You entered the allowed URL :)")
    elif input_hostname and input_hostname == allowed_hostname and parsed.hostname and parsed.hostname.startswith(allowed_hostname):
        print(f"Valid URL :)")
        print("Flag: ctf4b{dummy_flag}")
    else:
        print(f"Invalid URL x_x, expected hostname {allowed_hostname}, got {parsed.hostname if parsed.hostname else 'None'}")
except Exception as e:
    print("Error happened")