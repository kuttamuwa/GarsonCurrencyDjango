import datetime
import json
import locale
import os
import pickle

import requests

from dovizapp.auth.config_reader import ConfiguresReader

locale.setlocale(locale.LC_ALL, "tr_TR.utf8")


class MoneyData:
    static_titles = {'title': 'title', 'alis': 'alis', 'satis': 'satis', 'dusuk': 'dusuk', 'yuksek': 'yuksek'}
    tarih_field = 'son_guncelleme'
    tarih_format = '%d.%m.%Y %H:%M:%S'
    url = "http://www.ozbeyfiziki.com/mobil/data2.txt"

    makasvalues = {}
    money_states = {}
    money_config = None

    output_file = os.path.join(os.path.dirname(__file__), 'currency_serialized.pkl')

    def __init__(self):
        self.tarih = None

    @classmethod
    def format_currency_data(cls, data):
        for i in data:
            i['alis'] = round(float(i['alis']), 4)
            i['satis'] = round(float(i['satis']), 4)

        return data

    @classmethod
    def set_money_config(cls, money_config_path):
        config = ConfiguresReader(money_config_path)
        cls.money_config = config.read_section('moneyconfig')

    @classmethod
    def get_money_config(cls):
        return cls.money_config

    @classmethod
    def add_data_state_info(cls, data):
        for i in data:
            i['state'] = cls.get_money_state(i['title'])

        return data

    @classmethod
    def add_data_makas_value_info(cls, data):
        for i in data:
            i['artis'] = cls.get_makas_value(i['title'], 'artis')
            i['azalis'] = cls.get_makas_value(i['title'], 'azalis')

        return data

    @classmethod
    def get_money_state(cls, money_term):
        return cls.money_states.get(money_term)

    @classmethod
    def get_para_birimleri_on(cls):
        return {k: v for k, v in cls.money_states.items() if v}  # on ise yani admin panelinde goster denilmisse

    @classmethod
    def get_para_birimleri_off(cls):
        return {k: v for k, v in cls.money_states.items() if not v}  # on ise yani admin panelinde goster denilmisse

    @classmethod
    def set_para_birimi_on(cls, birim):
        cls.money_states[birim] = True

    @classmethod
    def set_para_birimi_off(cls, birim):
        cls.money_states[birim] = False

    @classmethod
    def get_para_birimleri_all_liste(cls):
        if not cls.money_states:
            return None
        else:
            return [k for k, v in cls.money_states.items()]

    @classmethod
    def set_para_birimleri_all(cls, value):
        cls.money_states = value

    @classmethod
    def get_makas_value(cls, key, choice='artis'):
        if choice not in ('artis', 'azalis'):
            raise ValueError("Programmer error")

        value = cls.makasvalues.get(key).get(choice, 0.0)
        if value == '':  # belki formdan doner
            value = 0.0

        return value

    @classmethod
    def set_makas_value(cls, key, artisvalue, azalisvalue):
        cls.makasvalues[key] = {'artis': artisvalue, 'azalis': azalisvalue}

    @classmethod
    def set_makas_artis_value(cls, key, artisvalue):
        cls.makasvalues.get(key)['artis'] = artisvalue

    @classmethod
    def set_makas_azalis_value(cls, key, azalisvalue):
        cls.makasvalues.get(key)['azalis'] = azalisvalue

    @classmethod
    def automatic_fill_makasvalues(cls, initvalue=0):
        para_birimleri = cls.get_para_birimleri_all_liste()
        if para_birimleri is None:
            raise ValueError("Para birimleri doldurulamamis !")
        else:
            for para in para_birimleri:
                cls.set_makas_value(para, initvalue, initvalue)

    def get_tarih(self):
        return self.tarih

    def set_tarih(self, value):
        self.tarih = value

    def check_replace_ozbey_alis_satis(self, data):
        _dict_list = []

        data_list = list(data.items())

        compatible_ones = 0
        uncompatible_ones = 0

        for _, i in data_list:
            if isinstance(i, dict):
                alis, satis = float(i['alis'].replace(",", ".")), float(i['satis'].replace(",", "."))
                dusuk, yuksek = float(i['dusuk'].replace(",", ".")), float(i['yuksek'].replace(",", "."))
                if alis > satis:
                    _dict_list.append((i['title'], i))
                    compatible_ones += 1

                else:
                    _d = {'title': i['title'],
                          'alis': satis,
                          'satis': alis,
                          'dusuk': dusuk,
                          'yuksek': yuksek}
                    _dict_list.append((i['title'], _d))
                    uncompatible_ones += 1

        # we're passing time value due to deal with it before
        # check step
        for _, i in _dict_list:
            if i['alis'] > i['satis']:
                pass
                # raise SatisAlisException("Donusturmemize ragmen alis degeri satistan yuksek cikiyor !")

        # old style
        data = dict(_dict_list)
        return data

    def runforme(self):
        decoded_data = self.istek_yap()

        # tarih ayari
        tarih = datetime.datetime.strptime(decoded_data[self.tarih_field], self.tarih_format)
        self.set_tarih(tarih)

        # ozbey fiyat check
        decoded_data = self.check_replace_ozbey_alis_satis(decoded_data)

        # Para Birimi ayari
        if self.get_para_birimleri_all_liste() is None:
            # sayfa ilk acildiysa
            # para birimleri doldurulur
            _dict = {k: True for k in decoded_data.keys()}
            self.set_para_birimleri_all(_dict)

            # makas degerleri doldurulur
            self.automatic_fill_makasvalues()

        data = self.data_filtering(decoded_data)

        # makas
        data = self.makas_processing(data)

        # ordering money
        data = self.order_money(data)

        return data

    @classmethod
    def order_money(cls, data):
        """
        it orders list via config
        :param data: dictionary in list contains title, alis, satis
        :return: dictionary in list
        """
        order_list = cls.get_money_config()['dovizorder'].split(",")

        data_with_confs = [i for i in data if i['title'] in order_list]
        data_without_confs = [i for i in data if i['title'] not in order_list]

        data_with_confs.sort(
            key=lambda x: order_list.index(x['title']) if x['title'] in order_list else data.index(x['title']))

        return data_with_confs + data_without_confs

    def runforsarrafiye(self):
        decoded_data = self.istek_yap()

        # tarih ayari
        tarih = datetime.datetime.strptime(decoded_data[self.tarih_field], self.tarih_format)
        self.set_tarih(tarih)

        # makas
        data = self.makas_processing(decoded_data)

        return data['KGRTRY']

    @classmethod
    def _set_para_birimleri_init_with_turned(cls, decoded_data):
        _dict = {k: True for k in decoded_data.keys()}
        cls.set_para_birimleri_all(_dict)

    @classmethod
    def set_para_birimleri_turn_on_all(cls):
        # para birimleri doldurulur
        _dict = {k: True for k in cls.get_para_birimleri_all_liste()}
        cls.set_para_birimleri_all(_dict)

    @classmethod
    def set_para_birimleri_turn_off_all(cls):
        # para birimleri doldurulur
        _dict = {k: False for k in cls.get_para_birimleri_all_liste()}
        cls.set_para_birimleri_all(_dict)

    def istek_yap(self):
        try:
            response = requests.get(self.url)

        except ConnectionError:
            raise ConnectionError('Baglanti hatasi olustu. '
                                  'Lutfen internet baglantinizi kontrol ediniz !')
        if response.status_code != 200:
            raise requests.RequestException("Istek basarili donmuyor ! \n"
                                            f"{response}")

        print("Istek basarili gorunuyor")
        decoded_data = response.content.decode('utf-8-sig')

        decoded_data = json.loads(decoded_data)

        return decoded_data

    def makas_processing(self, data):
        for d in data:
            # if isinstance(d, dict):
            # alis - azalis
            # satis + artis
            # mantik: ucuz olani eksi, pahali olani arti
            alis_value = d[self.static_titles['alis']]
            if str(alis_value).count(','):
                alis_value = alis_value.replace(',', '.')

            alis_value = float(alis_value) - float(self.get_makas_value(d[self.static_titles['title']], 'azalis'))

            # satis
            satis_value = d[self.static_titles['satis']]
            if str(satis_value).count(','):
                satis_value = satis_value.replace(',', '.')

            satis_value = float(satis_value) + float(self.get_makas_value(d[self.static_titles['title']], 'artis'))

            d[self.static_titles['alis']] = alis_value
            d[self.static_titles['satis']] = satis_value

        return data

    def data_filtering(self, decoded_data, filter_with_selected_currencies=False):
        if filter_with_selected_currencies:
            alinacak_paralar = self.get_para_birimleri_on()

        else:
            alinacak_paralar = self.get_para_birimleri_all_liste()

        data = [i[1] for i in decoded_data.items() if i[0] in alinacak_paralar]
        data = self._data_changing(data)

        # sadece alis satis
        data = [{k: v for k, v in d.items() if k in ('title', 'alis', 'satis',)} for d in data if isinstance(d, dict)]
        return data

    def _data_changing(self, data):
        """
        ozbey alis ve satis degerlerini ters getiriyor
        :param data:
        :return:
        """
        new_data = []
        for d in data:
            if isinstance(d, dict):
                new_data.append(
                    {'title': d['title'], 'alis': d['satis'], 'satis': d['alis'], d['yuksek']: d['yuksek'],
                     d['dusuk']: d['dusuk']}
                )

        return new_data

    @classmethod
    def serialize(cls):
        if os.path.exists(cls.output_file):
            os.remove(cls.output_file)

        _dict = {
            'makasvalues': cls.makasvalues
        }

        outfile = open(cls.output_file, 'wb')
        pickle.dump(_dict, outfile, pickle.HIGHEST_PROTOCOL)
        outfile.close()
        print("serialized")

    @classmethod
    def get_pickled(cls):
        infile = open(cls.output_file, 'rb')
        obj = pickle.load(infile)
        infile.close()

        return obj

    @classmethod
    def reserialize(cls):
        if not os.path.exists(cls.output_file):
            print("uygulama ilk defa ayaga kalkiyor ..")

        else:
            obj = cls.get_pickled()
            cls.load_from_pickled(obj)

    @classmethod
    def load_from_pickled(cls, pickled_object):
        cls.makasvalues = pickled_object['makasvalues']
        print("doviz makas degerleri son oturumdan yuklendi")


class SatisAlisException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
