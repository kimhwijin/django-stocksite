from django.urls import path
from stock import views

app_name = 'stock'
urlpatterns = [
    #/stock/
    path('',views.StockModelView.as_view(), name='index'),
    #/stock/stockinfo/
    path('stockinfo/',views.StockInfo_List_View, name='stockinfo_list'),
    #/stock/stockinfo/<str:code>
    path('stockinfo/detail/<str:code_number>/',views.StockInfo_Detail_View, name='stockinfo_detail'),


    path('search/',views.Search_Info, name='search_info'),
    path('search/<str:stock_name>/<str:code_number>',views.Save_Favor, name='save_favor'),
    path('favor_detail/favor/<int:pk>',views.Delete_Favor, name='delete_favor'),

]