from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('pages', views.pages, name='page'),
    path('deletepage/<int:pk>', views.deletepage, name='deletepage'),
    path('updatepages/<int:pk>', views.updatepages, name='updatepage'),
    path('detailpages/<int:pk>', views.detailpages, name='detailpage'),
    path('addnewkey', views.AddNewKey, name='addnewkey'),
    path('deletekey/<str:keyname>', views.DeleteKeyOnPageDetail, name='deletekey'),
    path('lang', views.LanguagesPage, name='lang'),
    path('langupdate/<int:pk>', views.LanguagesUpdatePage, name='langupdate'),
    path('deletelang/<int:pk>', views.LanguageDelete, name='deletelang'),
    path('updatepageimage/<int:pk>', views.UpdatePageImage, name='updatepageimage'),
    path('deletepageimage/<int:pk>', views.DeletePageImage, name='deletepageimage')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)