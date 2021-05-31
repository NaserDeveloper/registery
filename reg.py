import os
import requests
import random
import uuid
import socket
import smtplib
from threading import Thread
from time import sleep

hostname = socket.gethostname()

dir_path = os.path.dirname(os.path.realpath(__file__))

proxies = [i.strip() for i in open(dir_path + "/proxies.txt", "r") if i]

usernames = [i.strip() for i in open(dir_path + "/list.txt", "r") if i]

email = ("".join(random.choice("qwertyuiopasdfghjklzxcvbnm1234567890+") for i in range(18)))


class Instagram():
    def __init__(self):
        super(Instagram, self).__init__()
        self.running = True
        self.claimed = False
        self.nick = ''
        self.password = ''
        self.attempts = 0
        self.req = requests.Session()

    def claim_username(self, username):
        proxing = []
        for i in proxies:
            proxing.append(i)
            random_proxies = str(random.choice(proxing))
            random_proxy = {
                'http': 'http://{}'.format(random_proxies),
                'https': 'https://{}'.format(random_proxies),
            }
            self.req.proxies = random_proxy
        curl = 'https://i.instagram.com/api/v1/accounts/create_business/'
        cdata = {
            'email': email + "@gmail.com",
            'password': self.password,
            'username': username,
            'first_name': 'Nasser Reg',
            'phone_id': str(uuid.uuid1()),
            'device_id': str(uuid.uuid1())}
        cheaders = {
            'User-Agent': 'Instagram 135.0.0.34.124 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)',
            "Accept": "/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US",
            "X-IG-Capabilities": "3brTvw==",
            "X-IG-Connection-Type": "WIFI",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            'Host': 'i.instagram.com'
        }
        response = self.req.post(curl, data=cdata, headers=cheaders).text

        if "\"error_type\": \"username_is_taken\"" in response:
            self.attempts += 1
            print(f'{self.attempts} : {username}')

        elif "\"error_type\": \"username_held_by_others\"" in response:
            self.attempts += 1
            print(f'{self.attempts} : {username}')

        elif f"\"email\": [\"Another account is using {email}.\"" in response:
            with open(f'@{username}.txt', 'a') as file3:
                file3.write(
                    'Username:' + username + '\n' + 'Email:' + email + '\n' + 'password:' + self.password + '\n')
            print(f'Claimed >> {username}, Add Phone Number')
            return True

        elif "\"message\": \"challenge_required\", \"challenge\"" in response:
            with open(f'@{username}.txt', 'a') as file3:
                file3.write(
                    'Username:' + username + '\n' + 'Email:' + email + '\n' + 'password:' + self.password + '\n')
            print(f'Claimed >> {username}, Add Phone Number')
            return True

        elif "\"message\": \"checkpoint_required\", \"checkpoint_url\"" in response:
            with open(f'@{username}.txt', 'a') as file3:
                file3.write(
                    'Username:' + username + '\n' + 'Email:' + email + '\n' + 'password:' + self.password + '\n')
            print(f'Claimed >> {username}, Add Phone Number')
            return True


xnum = 0


class Turbo(Thread):
    def __init__(self, instagram):
        super(Turbo, self).__init__()
        self.instagram = instagram

    def run(self):
        global xnum
        while self.instagram.running:
            try:
                if xnum >= len(usernames):
                    xnum = 0
                    username = usernames[xnum]
                    xnum += 1
                else:
                    username = usernames[xnum]
                    xnum += 1
                if self.instagram.claim_username(username):
                    self.instagram.claimed = True
                sleep(0.001)
            except:
                pass


if __name__ == "__main__":
    try:
        instagram = Instagram()
    except Exception as ex:
        print(ex)
        exit(1)
    instagram.password = input('Enter Password: ')
    threads = int(input('Enter Thread: '))
    for _ in range(threads):
        thread = Turbo(instagram)
        thread.setDaemon(True)
        thread.start()
        try:
            while instagram.running:
                sleep(0.15)

        except KeyboardInterrupt:
            instagram.running = False
            pass

        sleep(5)
        input("Press Enter To Close");
        os._exit(0)
