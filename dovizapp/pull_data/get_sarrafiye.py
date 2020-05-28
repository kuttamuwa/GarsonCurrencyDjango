import datetime


class SarrafiyeInfo:
    tarih_format = '%d.%m.%Y %H:%M:%S'
    tarih = datetime.datetime.now().strftime(tarih_format)
    _infos = {'Çeyrek': {'title': 'Çeyrek', 'alis': None, 'satis': None},
              'Yarım': {'title': 'Yarım', 'alis': None, 'satis': None},
              'Ziynet_Lira': {'title': 'Ziynet_Lira', 'alis': None, 'satis': None},
              'Ata_Lira': {'title': 'Ata_Lira', 'alis': None, 'satis': None},
              'Hurda_24': {'title': 'Hurda_24', 'alis': None, 'satis': None},
              'Hurda_22': {'title': 'Hurda_22', 'alis': None, 'satis': None}}

    _makasvalues = {'Çeyrek': {'title': 'Çeyrek', 'artis': 1, 'azalis': 1},
                    'Yarım': {'title': 'Yarım', 'artis': 1, 'azalis': 1},
                    'Ziynet_Lira': {'title': 'Ziynet_Lira', 'artis': 1, 'azalis': 1},
                    'Ata_Lira': {'title': 'Ata_Lira', 'artis': 1, 'azalis': 1},
                    'Hurda_24': {'title': 'Hurda_24', 'artis': 1, 'azalis': 1},
                    'Hurda_22': {'title': 'Hurda_22', 'artis': 1, 'azalis': 1}}

    represent_values = {'Çeyrek': True, 'Yarım': True, 'Ziynet_Lira': True,
                        'Ata_Lira': True, 'Hurda_24': True, 'Hurda_22': True}
    __KGRTRY = {'alis': 0, 'satis': 0}

    @classmethod
    def format_currency_data(cls, data):
        for i in data:
            i['alis'] = format(round(float(i['alis']), 4), ",")
            i['satis'] = format(round(float(i['satis']), 4), ",")

        return data

    @classmethod
    def add_data_state_info(cls, sarrafiye_data):
        for i in sarrafiye_data:
            i['state'] = cls.get_state_value(i['title'])

        return sarrafiye_data

    @classmethod
    def add_data_makas_value_info(cls, sarrafiye_data):
        for i in sarrafiye_data:
            i['artis'] = cls.get_makas_value(i['title'])
            i['azalis'] = cls.get_makas_value(i['title'], _type='azalis')

        return sarrafiye_data

    @classmethod
    def get_tarih(cls):
        return cls.tarih

    @classmethod
    def get_state_value(cls, key):
        return cls.represent_values.get(key)

    @classmethod
    def turn_off_all_represent_values(cls):
        cls.represent_values = {x: False for x in cls.represent_values}

    @classmethod
    def turn_on_all_represent_values(cls):
        cls.represent_values = {x: True for x in cls.represent_values}

    @classmethod
    def turn_on_represent_value(cls, sarrafiye):
        cls.represent_values[sarrafiye] = True

    @classmethod
    def turn_off_represent_value(cls, sarrafiye):
        cls.represent_values[sarrafiye] = False

    @classmethod
    def get_on_represent_values(cls):
        return [k for k, v in cls.represent_values.items() if v]

    @classmethod
    def get_off_represent_values(cls):
        return [k for k, v in cls.represent_values.items() if not v]

    @classmethod
    def set_makas_value(cls, sarrafiye, value, _type='artis'):
        """

        :param sarrafiye:
        :param value:
        :param _type: artis, azalis
        :return:
        """
        cls._makasvalues[sarrafiye][_type] = value
        cls.update_info_values()

    @classmethod
    def get_makas_value(cls, sarrafiye, _type='artis'):
        """

        :param sarrafiye:
        :param _type: artis, azalis
        :return:
        """
        return cls._makasvalues[sarrafiye][_type]

    @classmethod
    def get_all_makas_values(cls):
        return cls._makasvalues

    @classmethod
    def update_info_values(cls):
        """
        KGRTRY'nin alisi * ziynetin satis milyemi
        KGRTRY'nin satisi * ziynetin alis milyemi
        :return:
        """
        cls.check_kgrtry()

        for key in cls._infos.keys():
            cls._infos[key]['alis'] = float(cls.get_kgrtry('alis')) * float(cls._makasvalues[key]['artis'])
            cls._infos[key]['satis'] = float(cls.get_kgrtry('alis')) * float(cls._makasvalues[key]['azalis'])

    @classmethod
    def reset_all_makas_values(cls):
        for key in cls._makasvalues.keys():
            cls._makasvalues[key]['artis'] = 1
            cls._makasvalues[key]['azalis'] = 1

    @classmethod
    def get_sarrafiye_info(cls):
        return cls._infos

    @classmethod
    def set_sarrafiye_info(cls, sarrafiye, value, _type='alis'):
        cls._infos[sarrafiye][_type] = value

    @classmethod
    def get_kgrtry(cls, _type='alis'):
        return cls.__KGRTRY[_type]

    @classmethod
    def set_kgrtry(cls, alisvalue, satisvalue):
        cls.__KGRTRY['alis'] = alisvalue
        cls.__KGRTRY['satis'] = satisvalue
        # update sarrafiye infos
        cls.update_info_values()

    @classmethod
    def check_kgrtry(cls):
        if cls.get_kgrtry(_type='alis') is None:
            raise ValueError('KGRTRY ALIS DEGERİ BOS !')
        elif cls.get_kgrtry(_type='satis') is None:
            raise ValueError('KGRTRY SATIS DEGERİ BOS !')

    @classmethod
    def get_data(cls):
        data = [v for k, v in cls._infos.items()]
        return data
