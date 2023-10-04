import hashlib
import requests
import sys

show_hash = sys.argv[1] if len(sys.argv) > 1 else ""

while True:
    password = input("Enter your password: ")
    if password != "exit":
        password = hashlib.sha1(password.encode()).hexdigest()
        request_in_api = f"https://api.pwnedpasswords.com/range/{password[:5]}"
        hashed_password = f"Your hashed password is: {password}\n" if show_hash == "--show-hash" else ""
        print(hashed_password + "Checking...")
        checking = requests.get(request_in_api, headers={"Add-Padding": "true"}).text.split("\r")

        n = 0
        for i in checking:
            hash_sum, times = i.split(":")
            if password[5:].casefold() in hash_sum.casefold():
                n += int(times)

        print(f'Your password has been pwned! This password appears {n} times in data breaches.' if n!= 0 else "Good news! Your password hasn't been pwned.")
    else:
        print("Goodbye!")
        break