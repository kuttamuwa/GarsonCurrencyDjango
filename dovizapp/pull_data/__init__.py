from dovizapp import MoneyData

if MoneyData.get_para_birimleri_all_liste() is None:
    MoneyData().runforme()