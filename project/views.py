from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import *
# For Image CRUD
def index(request):
    if request.method == 'POST':
        pageimage = AddImages.objects.filter(page_id=int(request.POST.get('page')),image_key=request.POST.get('image_key')).first()
        if pageimage:
            messages.error(request, f'{pageimage.image_key} for {pageimage.page} page is already exit')
            return redirect('index')
        AddImages.objects.create(page_id=int(request.POST.get('page')), image_key=request.POST.get('image_key'), image=request.FILES.get('image'))
        messages.success(request, f'Create is success')
        return redirect('index')
    else:
        pagesval = Pages.objects.all()
        pages_list = AddImages.objects.all()
        paginator = Paginator(pages_list, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        forloop_start_index = (page_obj.number - 1) * page_obj.paginator.per_page
        return render(request, 'index.html', {'pages': page_obj, 'forloop_start_index': forloop_start_index, 'pagesval':pagesval})
    
def DeletePageImage(request, pk):
    image= AddImages.objects.filter(pk=pk).first()
    if image:
        image.delete()
        messages.success(request, 'Delete is successful')
        return redirect('index')
    else:
        messages.error(request, 'ID not found')
        return redirect('index')
    
def UpdatePageImage(request, pk):
    if request.method == 'POST':
        pageimage = AddImages.objects.exclude(pk=pk).filter(image_key=request.POST.get('image_key'),page_id=int(request.POST.get('page'))).first()
        updatepageimage = AddImages.objects.filter(pk=pk).first()
        if pageimage:
            messages.error(request, f'{pageimage.image_key} for {pageimage.page} page is already exit')
            return redirect(f'/updatepageimage/{pk}')
        else:
            updatepageimage.image_key = request.POST.get('image_key')
            if request.FILES.get('image'):
                updatepageimage.image = request.FILES.get('image')
            updatepageimage.save()
            messages.success(request, 'Update is successful')
            return redirect('index')
    else:
        pagesval = Pages.objects.all()
        image = AddImages.objects.filter(pk=pk).first()
        return render(request, 'updatepageimage.html', {'image': image, 'pagesval':pagesval, 'page_id': image.page.id})
    
# end For Image CRUD
# For Page CRUD
def pages(request):
    if request.method =='POST':
        pagename = request.POST.get('pagename').lower()
        if Pages.objects.filter(page_name= pagename).first():
            messages.error(request, f'{pagename}  is already exit')
            return redirect('page')
        Pages.objects.create(page_name=pagename)
        messages.success(request, 'Create is successful')
        return redirect('page')
    else:
        pages_list = Pages.objects.all()
        if request.GET.get('search'):
            pages =pages_list.filter(page_name__icontains=request.GET.get('search'))
        else: 
            pages = pages_list
        paginator = Paginator(pages, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        forloop_start_index = (page_obj.number - 1) * page_obj.paginator.per_page
        return render(request, './pages/pages.html', {'pages': page_obj, 'forloop_start_index': forloop_start_index})

def deletepage(request, pk):
    page = Pages.objects.filter(pk=pk).first()
    if page:
        page.delete()
        messages.success(request, 'Delete is successful')
        return redirect('page')
    else:
        messages.error(request, 'ID is not found.')
        return redirect('page')
    
def updatepages(request, pk):
    if request.method == 'POST':
        page = Pages.objects.filter(pk=pk).first()
        checkpage = Pages.objects.exclude(pk=pk).filter(page_name=request.POST.get('pagename')).filter()
        if checkpage:
            messages.error(request, 'Page is already exit.')
            return redirect(f'/updatepages/{pk}')
        if page:
            page.page_name = request.POST.get('pagename')
            page.save()
            messages.success(request, 'Update is Success.')
            return redirect('page')
        else:
            messages.error(request, 'Page is not found.')
            return redirect(f'/updatepages/{pk}')
    else:
        page = Pages.objects.filter(pk=pk).first()
        return render(request, './pages/updatepage.html', {'page': page})
# end For Page CRUD
# For key CRUD
def detailpages(request, pk):
    if request.method =='POST':
        id=request.POST.get('languagekeyid')
        combinationlanguageandpage= CombinationLanguageAndPage.objects.filter(pk=id).first()
        if combinationlanguageandpage:
            combinationlanguageandpage.value = request.POST.get('languagevalue')
            combinationlanguageandpage.save()
            messages.success(request, 'Create is success.')
            return redirect(f'/detailpages/{pk}')
        else:
            messages.error(request, 'ID is not found.')
            return redirect(f'/detailpages/{pk}')
    else:
        page= Pages.objects.filter(pk=pk).first()
        pagekeys = CombinationLanguageAndPage.objects.filter(page_id=pk)
        if request.GET.get('search'):
            pagekeyvalues = pagekeys.filter(key__icontains=request.GET.get('search')) | pagekeys.filter(value__icontains=request.GET.get('search'))
        else: 
            pagekeyvalues = pagekeys
        paginator = Paginator(pagekeyvalues, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        forloop_start_index = (page_obj.number - 1) * page_obj.paginator.per_page
        return render(request, './pages/detailpage.html', {'pagekeys': page_obj, 'forloop_start_index': forloop_start_index, 'page': page.page_name, 'pageid': pk })
    
def AddNewKey(request):
    if request.method =='POST':
        languages= Languages.objects.all()
        entries = []
        check = []
        for language in languages:
            combine = CombinationLanguageAndPage.objects.filter(lang_id=language.id, key = request.POST.get('pagedetailkey'))
            if not combine:
                entries.append(CombinationLanguageAndPage(lang=language, page_id=int(request.POST.get('pageidvalue')), key=request.POST.get('pagedetailkey'), value= request.POST.get('pagedetailvalue')))
            else:
                check.append('true')
        if entries:
            CombinationLanguageAndPage.objects.bulk_create(entries)

        if check:
            messages.error(request, f'this key already exist.')
            return redirect(f'/detailpages/{request.POST.get("pageidvalue")}')
        else:
            messages.success(request, 'Create is success.')
            return redirect(f'/detailpages/{request.POST.get("pageidvalue")}')
        
def DeleteKeyOnPageDetail(request, keyname):
    deletekey= CombinationLanguageAndPage.objects.filter(key=keyname, page_id= request.GET.get('pageid'))
    if deletekey:
        deletekey.delete()
        messages.success(request, 'Delete is success.')
        return redirect(f'/detailpages/{deletekey.page_key}')
    else:
        messages.success(request, 'ID is not found.')
        return redirect(f'/detailpages/1')
# end For key CRUD   
def LanguagesPage(request):
    if request.method == 'POST':
        checklang = Languages.objects.filter(lang_key=request.POST.get('langkey'))
        checklangname = Languages.objects.filter(lang_name=request.POST.get('langname'))
        if checklang:
            messages.error(request, f'{checklang.lang_key} Key already exist')
            return redirect('lang')
        elif checklangname:
            messages.error(request, f'{checklangname.lang_name} Name already exist')
            return redirect('lang')
        else:
            lang = Languages.objects.create(lang_key=request.POST.get('langkey'), lang_name=request.POST.get('langname'))
            lang.save()
            autoAddKeyForPageLanguage(lang)
            messages.success(request, 'Create is success.')
            return redirect('lang')
    else:
        languages_list = Languages.objects.all()
        if request.GET.get('search'):
            lans = languages_list.filter(lang_key__icontains=request.GET.get('search')) | languages_list.filter(lang_name__icontains=request.GET.get('search'))
        else: 
            lans = languages_list
        paginator = Paginator(lans, 10) 
        languages_number = request.GET.get('page')
        lang_obj = paginator.get_page(languages_number)
        forloop_start_index = (lang_obj.number - 1) * lang_obj.paginator.per_page
        return render(request, './languagepages/languages.html', {'pages': lang_obj, 'forloop_start_index': forloop_start_index})

def LanguagesUpdatePage(request, pk):
    language = Languages.objects.filter(pk= pk).first()
    if request.method == 'POST':
        languages = Languages.objects.exclude(pk=pk).filter(lang_name=request.POST.get('langname')).first()
        languageskey = Languages.objects.exclude(pk=pk).filter(lang_key=request.POST.get('langkey')).first()
        if languages:
            messages.error(request, f'{languageskey.lang_key} Key already exist')
            return redirect(f'../langupdate/{pk}')
        elif languageskey:
            messages.error(request, f'{languageskey.lang_key} Key was used in {languageskey.lang_name}.')
            return redirect(f'../langupdate/{pk}')
        else:
            language.lang_key = request.POST.get('langkey')
            language.lang_name = request.POST.get('langname')
            language.save()
            messages.success(request, 'Update is success.')
            return redirect('lang')
    else:
        return render(request, './languagepages/languageupdate.html', {'language': language})

def LanguageDelete(request, pk):
    language = Languages.objects.filter(pk= pk).first()
    if language:
        language.delete()
        messages.success(request, 'Delete is success.')
        return redirect('lang')
    else:
        messages.success(request, 'Id is not found.')
        return redirect('lang')


def autoAddKeyForPageLanguage(language):
    combin = CombinationLanguageAndPage.objects.filter(lang_id=language.id)
    pages = Pages.objects.all()
    check_key = ''
    if not combin:
        for page in pages:
            combin_ones = CombinationLanguageAndPage.objects.filter(page_id=page.id)
            if combin_ones.exists():
                for combin_one in combin_ones:
                    if check_key != combin_one.key:
                        CombinationLanguageAndPage.objects.create(lang_id=language.id, page_id=combin_one.page.id, key=combin_one.key, value=combin_one.value)
                        check_key = combin_one.key
    return 'true'