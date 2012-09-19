# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

import datetime
from collections import defaultdict

from utils import parselist, parsestring

class PgArrayWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        if value is not None:
            value = parselist(value)
        return super(PgArrayWidget, self).render(name, value, attrs)

def PgArrayFormField(formfield):
    class FieldArray(forms.CharField):
        
        widget = PgArrayWidget
        
        def to_python(self, value):
            if not value:
                return None
            return [formfield.to_python(v) for v in value]
        
        def clean(self, value):
            value = super(TagField, self).clean(value)
            try:
                return parse_tags(value)
            except ValueError:
                raise forms.ValidationError(_("Please provide a comma-separated list of tags."))
    
    
        


class PgArrayFormField(forms):
    #default_error_messages = {
    #    'invalid':_('Enter a valid time span: e.g. "3 days, 4 hours, 2 minutes"')
    #}
    
    def __init__(self, *args, **kwargs):
        defaults = {'widget':TimedeltaWidget}
        defaults.update(kwargs)
        super(PgArrayFormField, self).__init__(*args, **defaults)
        
    def clean(self, value):
        super(PgArrayFormField, self).clean(value)
        if value == '' and not self.required:
            return u''
        
        data = defaultdict(float)
        try:
            return parse(value)
        except TypeError:
            raise forms.ValidationError(self.error_messages['invalid'])
            
        return datetime.timedelta(**data)

#class PgArrayChoicesField(TimedeltaFormField):
#    def __init__(self, *args, **kwargs):
#        choices = kwargs.pop('choices')
#        defaults = {'widget':forms.Select(choices=choices)}
#        defaults.update(kwargs)
#        super(TimedeltaChoicesField, self).__init__(*args, **defaults)
