from html.parser import HTMLParser
from html.entities import name2codepoint


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        for attr in attrs:
            if tag == "img":
                self.imgInfo[attr[0]] = [attr[1]]
            else:
                self.imgInfo["src"] = [None]
        print(self.imgInfo)

    def handle_endtag(self, tag):
        print("End tag  :", tag)

    def handle_data(self, data):
        self.data = data
        print("Data     :", data)

    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)

    def handle_decl(self, data):
        print("Decl     :", data)

    def __init__(self):
        super().__init__()
        self.imgInfo = {}
        self.data = ""



