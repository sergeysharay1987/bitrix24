from django.shortcuts import render, redirect, reverse
from .forms import CreateLead
from fast_bitrix24 import Bitrix
from dadata import Dadata

token = "68de34222a74a59793cfd9d431a771fd79816581"
secret = "f3da9bf600d9b2386a43d7146fab10d88f83f222"
dadata = Dadata(token, secret)
API_URL = "https://dadata.ru/api/clean/name/"
URL_WEB_HOOK_TO_CALL_REST_API = 'https://b24-tc3mws.bitrix24.ru/rest/1/27b28um0db36ab7r'
bx24 = Bitrix(URL_WEB_HOOK_TO_CALL_REST_API)


def check_empty_key_values(fio, telephone, address):
    for dictionary in fio, telephone, address:
        for key in dictionary:
            if not dictionary[key]:
                dictionary[key] = ''
    print(fio, telephone, address, )
    return fio, telephone, address


def make_data_to_call_rest_api(fio_from_form, telephone_from_form, address_from_form):
    fio_from_form = dadata.clean('name', fio_from_form)
    telephone_from_form = dadata.clean('phone', telephone_from_form)
    address_from_form = dadata.clean('address', address_from_form)
    address_from_form__by_fias = dadata.find_by_id('address', address_from_form['fias_id'])
    fio, telephone, address = check_empty_key_values(fio_from_form, telephone_from_form, address_from_form__by_fias[0])
    print(fio, telephone, address)
    return fio, telephone, address


def call_web_hook(fio_from_dadata, telephone_from_dadata, address_from_dadata_by_fias):
    # print(fio_from_dadata, telephone_from_dadata, telephone_from_dadata, sep = '\n')
    return bx24.call('crm.lead.add', items={
        'fields':
            {
                "NAME": fio_from_dadata['name'],
                "SECOND_NAME": fio_from_dadata['patronymic'],
                "LAST_NAME": fio_from_dadata['surname'],
                "ADDRESS": address_from_dadata_by_fias['unrestricted_value'],
                # "ADDRESS": address_from_dadata["result"],
                "PHONE": [
                    {"VALUE": telephone_from_dadata['phone'], "VALUE_TYPE": telephone_from_dadata['type']}]
            }
    })


def hello_user(request):
    a_href = reverse(viewname='create_lead')
    return render(request, 'create_lead/hello_user.html', {'a_href': a_href})


def create_lead(request):
    if request.method == 'GET':
        form = CreateLead()
        return render(request, 'create_lead/index.html', {'form': form})
    if request.method == 'POST':

        bound_form = CreateLead(request.POST)
        if bound_form.is_valid():

            fio_from_dadata, telephone_from_dadata, address_from_dadata_by_fias = make_data_to_call_rest_api(
                bound_form.cleaned_data['fio'],
                bound_form.cleaned_data['telephone'],
                bound_form.cleaned_data['address_of_lead'])
            fio, telephone, address = check_empty_key_values(fio_from_dadata, telephone_from_dadata,
                                                             address_from_dadata_by_fias)
            #print(fio, telephone, address, sep = '\n')
            #print()
            #call_web_hook(fio_from_dadata, telephone_from_dadata, address_from_dadata_by_fias)
            call_web_hook(fio, telephone, address)
            return redirect(reverse('lead_have_created'))
        else:
            form = CreateLead(request.POST)
            return render(request, 'create_lead/index.html', {'form': form})


def show_result_of_creation(request):
    return render(request, 'create_lead/lead_have_created.html')
