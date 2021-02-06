from django.shortcuts import render,get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from stock.models import StockInfo
from django.http  import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

#template
class StockModelView(TemplateView):
    template_name = 'stock/stockinfo_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_list"] = ['StockInfo',]
        return context

#favor stock list view
from stock import django_crawler
def StockInfo_List_View(request):
    stockinfo_list = StockInfo.objects.all().order_by('id')
    context_list = []

    for stockinfo in stockinfo_list:
        temp_list = django_crawler.get_listinfo(stockinfo.code)
        context_list.append((temp_list))

    context = {
        'object_info_list' : context_list,
    }
    print('list')
    return render(request, 'stock/stockinfo_list.html', context)


#
def StockInfo_Detail_View(request,code_number):

    stockinfo = get_object_or_404(StockInfo,code=code_number)

    
    detailinfo = django_crawler.get_all_detail_info(code_number)

    context = {
        'stockinfo' : stockinfo,
        'detailinfo' : detailinfo,
    }
    print('detail')
    return render(request,'stock/stockinfo_detail.html',context)


from stock.forms import SearchKeywordForm


#
def Search_Info(request):
    search_keyword_form = SearchKeywordForm(request.GET)
    kw_valid = False
    temp_list = []

    if search_keyword_form.is_valid():
        skw = search_keyword_form.cleaned_data['search_keyword']
        if len(skw) == 6 and skw.isdigit():
            kw_valid = True
            temp_list = django_crawler.get_listinfo(skw)
    else:
        skw = 'form_invalid'

    context = {
        'search_keyword' : skw,
        'keyword_valid' : kw_valid,
        'searched_stockinfo': temp_list,
    }
    print('search')
    return render(request, 'stock/stockinfo_search_result.html', context)

#
def Save_Favor(request,stock_name,code_number):
    print('save')
    StockInfo.objects.create(name=stock_name, code=code_number)
    return HttpResponseRedirect(reverse('stock:stockinfo_detail', args=[code_number,]))

#
def Delete_Favor(request,pk):
    print('delete')
    StockInfo.objects.filter(pk=pk).delete()
    return HttpResponseRedirect(reverse('stock:stockinfo_list'))
