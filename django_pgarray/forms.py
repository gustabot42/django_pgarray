# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from utils import csv_to_list, list_to_csv, csv


class PgArrayWidget(forms.Textarea):
    def render(self, name, value, attrs=None):
        if value is not None:
            value = list_to_csv(value)
        return super(PgArrayWidget, self).render(name, value, attrs)


def PgArrayFormField(formfield):
    class FieldArray(forms.CharField):  # Class inside a function, smell like hack
        widget = PgArrayWidget
        
        def to_python(self, value):
            if value is None:
                return value
            return [formfield.to_python(v) for v in value]
        
        def clean(self, value):
            try:
                value = csv_to_list(value)
            except csv.csv.Error:
                e = _(u"Please provide a comma separated value list.")
                raise forms.ValidationError(e)
            
            
            return super(FieldArray, self).clean(value)
    
    return FieldArray
