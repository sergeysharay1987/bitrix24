#!/usr/bin/env python


from django import forms
from .models import Lead


class CreateLead(forms.ModelForm):

    class Meta:
        model = Lead
        fields = ['fio', 'telephone', 'address_of_lead']