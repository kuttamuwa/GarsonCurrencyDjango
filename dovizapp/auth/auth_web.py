"""
It will authenticate with another web server
"""
import requests


class AuthPhone:
    url = "http://www.ozteksms.com/panel/smsgonder1Npost.php"
    headers = {'Content-Type': "application/xml"}
    _phone_sifre = {}

    @classmethod
    def get_sifre(cls, phone_number):
        return cls._phone_sifre[phone_number]

    @classmethod
    def set_sifre(cls, phone_number, sifre):
        cls._phone_sifre[phone_number] = sifre

    @classmethod
    def reset_sifre(cls, username):
        cls._phone_sifre[username] = None

    @staticmethod
    def fix_phone_number(phone_number):
        number = phone_number.replace(" ", "")
        return number

    @classmethod
    def get_url(cls):
        return cls.url

    @classmethod
    def reset_all(cls):
        cls._phone_sifre = None

    @classmethod
    def send_msg(cls, phone_number):
        istek = requests.post(cls.get_url(), data={'data': cls._create_send_msg(phone_number)})
        if istek.status_code == 200:
            return True
        else:
            print("Numara doğrulaması yapılamadı !")
            return False

    @classmethod
    def _create_send_msg(cls, phone_number):
        sifre = cls.get_sifre(phone_number)
        msg = f"<sms><kno>1007268</kno><kulad>905323028251</kulad><sifre>568SYR</sifre><tur>Normal</tur><gonderen>" \
            f"AVIMAYDNLTM</gonderen><mesaj>Sizin kodunuz: {sifre}</mesaj><numaralar>{phone_number}</numaralar>" \
            f"<zaman>2020-01-14 10:56:00</zaman><zamanasimi>2020-01-14 11:56:00</zamanasimi></sms>"

        return msg
