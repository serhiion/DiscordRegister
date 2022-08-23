import os
from random import choice
from dotenv import load_dotenv
import requests
import httpx

load_dotenv()

API_KEY = os.environ["API_KEY"]

ROOT_URL = 'https://discord.com/api/v9/auth/'


def generate_password():
    return "".join(choice("abcdefghijklmnopqrstuvwxyz") for i in range(10))


class DiscordClient:

    def __init__(self):
        self.client = requests.Session()
        self.client.cookies.set(name="locale", value="en-US")
        self.client.headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "DNT": "1", "Host": "discord.com",
            "Referer": "https://discord.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
        }

    def post_form_data(self, email_f: str, username_f: str):
        self.client.headers['X-Fingerprint'] = str(self.client.get(
            "https://discord.com/api/v9/experiments",
            timeout=30
        ).json().get("fingerprint"))
        self.client.headers["Origin"] = "https://discord.com"
        "4c672d35-0701-42b2-88c3-78380b0db560"
        task = httpx.post(
            url=f"http://2captcha.com/in.php?key={API_KEY}&method=hcaptcha&sitekey=4c672d35"
                "-0701-42b2-88c3-78380b0db560&pageurl=https://discord.com/register")

        task_id = task.text.split("|")[1]
        password = generate_password()
        self.client.post(ROOT_URL + "register",
                         json={
                             "consent": True,
                             "fingerprint": self.client.headers["X-Fingerprint"],
                             "username": username_f,
                             "email": email_f,
                             "password": password,
                             "captcha_key": task_id,
                             "date_of_birth": "2000-01-01"
                         },
                         timeout=30)
        response = self.client.post(
            ROOT_URL + "login",
            json={
                "captcha_key": None,
                "gift_code_sku_id": None,
                "login": email_f,
                "password": password,
                "undelete": False
            }
        )
        token = response.json().get("token")
        print("Token:", token)
        return token


if __name__ == '__main__':
    email = input("Input email: ")
    username = input("Input username: ")
    discord_client = DiscordClient()
    discord_client.post_form_data(email, username)

