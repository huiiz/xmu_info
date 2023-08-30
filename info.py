from utils import calc_md5


class Info:
    def __init__(self, title, link, date):
        self.title = title
        self.link = link
        self.date = date
        self.md5_path = calc_md5(f"{self.title}_{self.date}")
        self.local_temp = False

    @property
    def path(self):
        return f"data/{self.md5_path}.html"

    def set_have_local_temp(self):
        self.local_temp = True

    def save_content(self, content):
        if not content:
            content = f'<p>请点击链接查看原文</p><p><a href={self.link} target="_blank">{self.title}</a> {self.date}</p><p>原文链接：<b>{self.link}</b></p>'
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(content)
        self.set_have_local_temp()

    # def get_content(self):
    #     if self.local_temp:
    #         with open(self.path, 'r') as f:
    #             return f.read()
    #     else:
    #         return get_content(self.link)

    def __str__(self):
        path_info = f"path: {self.path}" if self.local_temp else "no local temp"
        return f"""{'-' * 30}
title: {self.title}
link: {self.link}
date: {self.date}
have local temp: {self.local_temp}
{path_info}"""

    def json(self):
        return {
            "title": self.title,
            "link": self.link,
            "date": self.date,
            "md5_path": self.md5_path,
            "local_temp": self.local_temp
        }