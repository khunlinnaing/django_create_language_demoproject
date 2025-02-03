from django.http import JsonResponse
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from .models import *

pagename = openapi.Parameter('pagename', openapi.IN_QUERY, description="Enter your Page name", type=openapi.TYPE_STRING)
lang = openapi.Parameter(
    'lang', 
    openapi.IN_QUERY, 
    description="Enter Languages", 
    type=openapi.TYPE_STRING,
    enum=['en', 'my', 'ch', 'jp', 'thai'],
    default='en'
)
@swagger_auto_schema(
    method='GET',
     manual_parameters=[pagename, lang]
)
@api_view(['GET'])
def index(request):
    lang= request.query_params.get('lang', 'en')
    if not request.GET.get('pagename'):
        langerror=ErrorLang(lang, 'req_page_name')
        return JsonResponse({'message': langerror.value}, status=status.HTTP_400_BAD_REQUEST)
    try:
        try:
            pageval= Pages.objects.filter(page_name=request.query_params.get('pagename')).first()
            if not pageval:
                langerror=ErrorLang(lang, 'no_page')
                return JsonResponse({'message': langerror.value}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        langval= Languages.objects.filter(lang_key=lang).first()

        try:
            datas=[]
            images= []
            allkeys= CombinationLanguageAndPage.objects.filter(lang_id=langval.id,page_id=pageval.id)
            imgs= AddImages.objects.filter(page_id=pageval.id)
            for img in imgs:
                images.append({'id': img.id, 'key': img.image_key, 'image': img.image.url})
            for key in allkeys:
                datas.append({'id': key.id, 'lang': key.lang.lang_name, 'page': key.page.page_name, key.key: key.value})
            return JsonResponse({'data': datas, 'images': images}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='GET'
)
@api_view(['GET'])
def GetLanguages(request):
    langs = Languages.objects.all()
    langvals = []
    for lang in langs:
        langvals.append({'id': lang.id, 'key': lang.lang_key, 'name': lang.lang_name})
    return JsonResponse({'data': langvals}, status=status.HTTP_200_OK)

def ErrorLang(lang, key):
    pageval= Pages.objects.filter(page_name='error').first()
    try:
        langval= Languages.objects.filter(lang_key=lang).first()
        if not langval:
            langval= Languages.objects.filter(lang_key='en').first()
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    val= CombinationLanguageAndPage.objects.filter(lang_id=langval.id,page_id=pageval.id, key=key).first()
    return val