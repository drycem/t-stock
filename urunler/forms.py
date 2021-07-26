from django.forms import ModelForm
from .models import Islemler


class IslemlerForm(ModelForm):
    class Meta:
        model = Islemler
        # fields = '__all__'
        fields = ['urun', 'islem_turu', 'miktar', 'islem_tutari']

    def __init__(self, *args, **kwargs):
        super(IslemlerForm, self).__init__(*args, **kwargs)
        self.fields['urun'].disabled = True
        self.fields['islem_turu'].disabled = True
