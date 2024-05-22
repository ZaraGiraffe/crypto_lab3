import argparse
import json
from src.settings import *
import random
from src.utils import send_message, get_message, encrypt_message, decrypt_message


def config():
    from_name = input("type your name: ")
    to_name = input("type the name of your friend: ")
    data = {
        "from": from_name,
        "to": to_name,
        "key_temp": -1,
        "key": -1
    }
    json.dump(data, open(".config.json", "w"))
    print("The data is configured")


def send_key():
    data = json.load(open(".config.json", "r"))
    rnd = random.randint(2, 2**80)
    msg = str(pow(G, rnd, PRIME))
    data["key_temp"] = rnd
    json.dump(data, open(".config.json", "w"))
    response = send_message(
        from_name=data["from"],
        to_name=data["to"],
        message=msg,
        hash_data="hash"
    )
    print(response)


def get_key():
    data = json.load(open(".config.json", "r"))
    response = get_message(
        from_name=data["to"],
        to_name=data["from"],
    )
    friend_key = int(response["message"])
    data["key"] = pow(friend_key, data["key_temp"], PRIME)
    json.dump(data, open(".config.json", "w"))
    print("the key {} has been created".format(data["key"]))


def send():
    message = input("type your message: ")
    data = json.load(open(".config.json", "r"))
    response = send_message(
        from_name=data["from"],
        to_name=data["to"],
        message=encrypt_message(data["key"], message),
        hash_data="hash"
    )
    print(response)


def get():
    data = json.load(open(".config.json", "r"))
    response = get_message(
        from_name=data["to"],
        to_name=data["from"],
    )
    message = decrypt_message(data["key"], response["message"])
    print("Message: {}".format(message))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help="choose your action: [config, send_key, get_key, send, get]")

    args = parser.parse_args()
    if args.action == "send_key":
        send_key()
    elif args.action == "get_key":
        get_key()
    elif args.action == "config":
        config()
    elif args.action == "send":
        send()
    elif args.action == "get":
        get()
    else:
        print("there is no such action")


if __name__ == "__main__":
    main()

