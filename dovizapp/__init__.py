from dovizapp.auth.auth_onpremise import Auth
from dovizapp.pull_data.get_currency import MoneyData
import os
from pathlib import Path
from dovizapp import MoneyData

appconfig_path = os.path.join(Path(__file__).parent, "pull_data", "config.ini")
MoneyData.set_money_config(appconfig_path)
auth = Auth(appconfig_path)

if MoneyData.get_para_birimleri_all_liste() is None:
    MoneyData().runforme()
