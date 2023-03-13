import requests, re

class imgbox(object):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.endpoint = {
            "login": "https://imgbox.com/login",
            "generate": "https://imgbox.com/ajax/token/generate",
            "upload": "https://imgbox.com/upload/process"}
        self.csrf_token = None
        self.login = None
        self.gallery = None
        self.get_login()

    def get_login(self) -> None:
        self.csrf_token = re.search("<meta content=\"(.+?)\" name=\"csrf-token\" />",
            self.session.get(self.endpoint.get("login")).text).group(1)
        self.login = self.session.post(
            self.endpoint.get("login"),
            data={"utf8": "✓", "authenticity_token": self.csrf_token,
                  "user[login]": self.username, "user[password]": self.password})
        self.gallery = self.session.post(
            self.endpoint.get("generate"),
            data={"gallery": "true", "gallery_title": "CMRG Upload Bot",
                  "comments_enabled": "0"}, cookies={"request_method": "POST"},
            headers={"X-CSRF-Token": self.csrf_token, "X-Requested-With": "XMLHttpRequest",
                     "Referer": "https://imgbox.com/"}).json()

        return

    def upload(self, img: str) -> str:
        image = self.session.post(self.endpoint.get("upload"), files={
            "files[]": (img, open(img, "rb"), "image/png")},
            data={"token_id": self.gallery["token_id"],
                  "token_secret": self.gallery["token_secret"], "content_type": "1",
                  "thumbnail_size": "300r", "gallery_id": self.gallery["gallery_id"],
                  "gallery_secret": self.gallery["gallery_secret"],
                  "comments_enabled": "0"}, cookies={"request_method": "POST"},
            headers={"X-CSRF-Token": self.csrf_token, "X-Requested-With": "XMLHttpRequest",
                     "Referer": "https://imgbox.com/"})
        image = image.json()

        return image.get("files")[0].get("original_url")
