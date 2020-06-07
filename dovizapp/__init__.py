from dovizapp.auth.auth_onpremise import Auth
from dovizapp.pull_data.get_currency import MoneyData
import os
from pathlib import Path
from dovizapp import MoneyData
from dovizapp.pull_data.get_sarrafiye import SarrafiyeInfo

appconfig_path = os.path.join(Path(__file__).parent, "pull_data", "config.ini")

# config
MoneyData.set_money_config(appconfig_path)
SarrafiyeInfo.set_money_config(appconfig_path)

auth = Auth(appconfig_path)

if MoneyData.get_para_birimleri_all_liste() is None:
    MoneyData().runforme()

# reserializing
MoneyData.reserialize()

SarrafiyeInfo.reserialize()
