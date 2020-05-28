class FormManager:
    # kolay olsun diye
    formtypes = {'sarrafiyeadminform': 1, 'moneyadminform': 2}

    @classmethod
    def get_formtypes(cls, form_name):
        return cls.formtypes[form_name]

    @staticmethod
    def return_form_one(request):
        if [k for k, v in request.form.items()].count('sarrafiyeadminform'):
            return FormManager.get_formtypes('sarrafiyeadminform')

        elif [k for k, v in request.form.items()].count('moneyadminform'):
            return FormManager.get_formtypes('moneyadminform')
