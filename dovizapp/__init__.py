from dovizapp.pull_data.get_and_save import MoneyData
import os
from pathlib import Path

appconfig_path = os.path.join(Path(__file__).parent, "pull_data", "config.ini")
MoneyData.set_money_config(appconfig_path)