from pydantic import BaseModel

class VysionItem:
    pass


class Network(VysionItem):
    pass


class Email(VysionItem):

    __tax_refs__ = [
        taxonomy.Email
    ]


class Paste(VysionItem):

    __tax_refs__ = [
        taxonomy.Paste,
        taxonomy.Pastebin,
        taxonomy.JustPaste
    ]


class Skype(VysionItem):
    pass


class Telegram(VysionItem):
    pass


class WhatsApp(VysionItem):
    pass


class URL(VysionItem):
    
    def __init__(self, protocol, domain, port, path, signature, network):
        self.protocol = protocol
        self.domain = domain
        self.port = port
        self.path = path
        self.signature = signature
        self.network = network


class Page(VysionItem):
    
    def __init__(self, url:URL, parent, title, language, html, sha1sum, ssdeep, date):
        self.url = url
        self.parent = parent
        self.title = title
        self.language = language
        self.html = html
        self.sha1sum = sha1sum
        self.ssdeep = ssdeep
        self.date = date


