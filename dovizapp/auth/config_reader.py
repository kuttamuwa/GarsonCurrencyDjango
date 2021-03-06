# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Author : Umut Ucok, Universal

import configparser
from os.path import split
from os.path import exists


class ConfiguresReader:
    __modulepath__, _ = split(__file__)

    def __init__(self, config_path):
        if not exists(config_path):
            raise FileNotFoundError(f"{config_path} dizininde config dosyası bulunamamıştır")
        self.config_path = config_path

        self.sections = self.list_sections()
        self.configures = [self.read_section(sec) for sec in self.sections]

    def read_section(self, section):
        sec_dict = {}
        configure = configparser.ConfigParser()
        configure.read(self.config_path, 'utf-8')
        options = configure.options(section)
        for opt in options:
            sec_dict[opt] = configure.get(section, opt)

        return sec_dict

    def list_sections(self):
        configure = configparser.ConfigParser()
        configure.read(self.config_path, 'utf-8')

        return configure.sections()

    def ordered_list_sections(self, sectionlist):
        return [self.read_section(sec) for sec in sectionlist]
