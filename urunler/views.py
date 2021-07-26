from django.shortcuts import render, redirect
from django.views import generic
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from rest_framework import generics

from .forms import IslemlerForm
from .models import Urunler, Islemler
from .serializers import UrunlerSerializer

def home(request):
    return render(request, 'urunler/home.html/', {})


class UrunlerListCreate(generics.ListCreateAPIView):
    queryset = Urunler.objects.all()
    serializer_class = UrunlerSerializer


class UrunlerUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Urunler.objects.all()
    serializer_class = UrunlerSerializer


class UrunlerListView(generic.ListView):

    model = Urunler
    # paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context ['now'] = timezone.now()
        return context


class UrunlerDetailView(generic.DetailView):
    model = Urunler

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UrunlerUpdateView(generic.UpdateView):
    model = Urunler
    fields = ['stok']
    template_name_suffix = '_update_form'
    
    def get_success_url(self):
        return reverse_lazy('urunler-list')
    

# class UrunlerSearchListView(generic.ListView):

#     model = Urunler
#     fields = '__all__'
#     template_name_suffix = '_search'

#     def get_context_data(self, **kwargs):
#         if self.request.method == 'POST':
#             context = super().get_context_data(**kwargs)
#             context['search_txt'] = self.request.POST['search_txt']
#             return context
#         else:
#             return reverse('urunler-list')

def urunlerSearchView(request):
    def clear_txt(txt:str) -> str:
        txt = txt.upper()
        txt = txt.strip()
        txt = txt.replace('Ü', 'U')
        txt = txt.replace('Ğ', 'G')
        txt = txt.replace('Ş', 'S')
        txt = txt.replace('İ', 'I')
        txt = txt.replace('Ö', 'O')
        txt = txt.replace('Ç', 'C')
        return txt

    urunler = Urunler.objects.all()

    if request.method == 'POST':
        search_txt = request.POST['search_txt']
        search_txt = clear_txt(search_txt)
        searches = search_txt.split(' ')
        copy_src = searches.copy()
        for s in searches:
            if s == '':
                copy_src.pop(copy_src.index(s))

        for i in range(0,len(copy_src)):
            urunler = urunler.filter(aciklama__icontains=copy_src[i])
        # urunler = urunler.exclude(stok=0)
        return render(request, 'urunler/urunler_search.html', {'search_txt': search_txt, 'urunler': urunler,})

    if request.method == 'GET':
        src_slug = request.GET.get('item', '')
        if not src_slug == '':
            urunler = urunler.filter(kod=src_slug)
            return render(request, 'urunler/urunler_search.html', {'urunler': urunler,})        

        if src_slug == '':
            # return render(request, 'urunler/urunler_list.html', {})
            return reverse('urunler-list')


def urunlerBuy(request, urun_id):
    initial_data = {
        'urun' : urun_id,
        'islem_turu' : 'AL',
    }
    
    form = IslemlerForm(request.POST or None, initial=initial_data)
    
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'Alış işlemi tamamlandı.')
                urun = Urunler.objects.get(id=urun_id)    
                urun.stok = urun.stok + int(request.POST['miktar'])
                try:
                    urun.save()
                    messages.success(request, f'Alınan ürün(ler) stoğa eklendi.')
                except Exception as e:
                    print(e)
                    messages.warning(request, f'DİKKAT! Alınan ürün(ler) stoğa eklenemedi!')
                return redirect(reverse('urunler-search') + f"?item={urun.kod}")
            except Exception as e:
                print(e)
                messages.warning(request, f'Alış işlemi başarısız!')
                return redirect('urunler-buy', urun_id)

    context = {'form': form}
    
    return render(request, 'urunler/urunler_buy.html', context)
    
    # if request.method == 'POST':
    #     return reverse('urunler-list')

def urunlerSell(request, urun_id: int):
    initial_data = {
        'urun' : urun_id,
        'islem_turu' : 'ST',
    }
    
    form = IslemlerForm(request.POST or None, initial=initial_data)
    
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'Satış işlemi tamamlandı.')
                urun = Urunler.objects.get(id=urun_id)    
                urun.stok = urun.stok - int(request.POST['miktar'])
                try:
                    urun.save()
                    messages.success(request, f'Satılan ürün(ler) stoktan düşüldü.')
                except Exception as e:
                    print(e)
                    messages.warning(request, f'DİKKAT: Satılan ürün(ler) stoktan düşülemedi!.')
                return redirect(reverse('urunler-search') + f"?item={urun.kod}")
            except Exception as e:
                print(e)
                messages.warning(request, f'Satış işlemi başarısız!')
                return redirect('urunler-sell', urun_id)

    context = {'form': form}
    
    return render(request, 'urunler/urunler_sell.html', context)


class IslemlerListView(generic.ListView):
    model = Islemler

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
