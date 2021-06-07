from django.shortcuts import render, redirect, reverse
from .forms import CreateLead
from fast_bitrix24 import Bitrix
from dadata import Dadata


token = "153e032b2e5fc2f0283305f6bcd1bd05364c1b8a"
secret = "967b17ecea33bb4ccd6bfdc62c081b56010c18c0"
dadata = Dadata(token, secret)
API_URL = "https://dadata.ru/api/clean/name/"
URL_WEB_HOOK_TO_CALL_REST_API = 'https://b24-tc3mws.bitrix24.ru/rest/1/27b28um0db36ab7r'


def make_data_to_call_rest_api(fio, telephone, address):
    fio = dadata.clean('name', fio)
    telephone = dadata.clean('phone', telephone)
    address = dadata.clean('address', address)
    address_by_fias = dadata.find_by_id('address', address['fias_id'])
    return fio, telephone, address_by_fias





def find_address_by_fias(address_from_dadata):
    return dadata.find_by_id('address', address_from_dadata['fias_id'])


def call_web_hook(name, second_name, last_name, address_from_dadata, telephone_from_dadata):
    # address = dadata.find_by_id('address', address_from_dadata['fias_id'])
    # print(type(address))
    return bx24.call('crm.lead.add', items={
        'fields':
            {
                "NAME": name,
                "SECOND_NAME": second_name,
                "LAST_NAME": last_name,
                "ADDRESS": address_from_dadata['result'],
                "PHONE": [{"VALUE": telephone_from_dadata['phone'], "VALUE_TYPE": telephone_from_dadata['type']}]
            }
    })

bx24 = Bitrix(URL_WEB_HOOK_TO_CALL_REST_API)


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
            print(fio_from_dadata, address_from_dadata_by_fias)
            #fio_from_dadata = dadata.clean('name', source=request.POST['fio'])
            #if not fio_from_dadata['patronymic']:

                #fio_from_dadata['patronymic'] = ''
            #telepone_from_dadata = dadata.clean('phone', source=request.POST['telephone'])
            #address_from_dadata = dadata.clean("address", request.POST['address_of_lead'])
            #address_from_dadata_by_fias_ = dadata.find_by_id('address', address_from_dadata['fias_id'])
            bx24.call('crm.lead.add', items={
                'fields':
                    {
                        "NAME": fio_from_dadata['name'],
                        "SECOND_NAME": fio_from_dadata['patronymic'],
                        "LAST_NAME": fio_from_dadata['surname'],
                        "ADDRESS": address_from_dadata_by_fias[0]['unrestricted_value'],
                        # "ADDRESS": address_from_dadata["result"],
                        "PHONE": [{"VALUE": telephone_from_dadata['phone'], "VALUE_TYPE": telephone_from_dadata['type']}]
                    }
            })
            return redirect('https://b24-tc3mws.bitrix24.ru/stream/')
        else:
            form = CreateLead(request.POST)
            return render(request, 'create_lead/index.html', {'form': form})
