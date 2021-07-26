from django.db import models
from django.utils import timezone


class Urunler(models.Model):
    id = models.IntegerField(primary_key=True)
    kod = models.CharField(max_length=250)
    aciklama = models.TextField()
    uretici = models.CharField(max_length=250)
    birim = models.CharField(max_length=250)
    fiyat = models.FloatField()
    stok = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.kod} {self.aciklama}'


class Islemler(models.Model):
    ISLEM_TURU_CHOICES = [
    ('AL', 'Alış'),
    ('ST', 'Satış'),
    ]

    id = models.BigAutoField(primary_key=True)
    urun = models.ForeignKey(Urunler, on_delete=models.CASCADE)
    miktar = models.IntegerField()
    islem_turu = models.CharField(max_length=2, choices=ISLEM_TURU_CHOICES)
    islem_tutari = models.FloatField(blank=True, null=True)
    islem_zamani = models.DateTimeField(auto_now=True)

    def __str__(self):
        return super().__str__()