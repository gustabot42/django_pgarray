# -*- coding: utf-8 -*-

from django.core.exceptions import  ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from forms import PgArrayFormField
from utils import csv_to_list, list_to_csv


PG_ENGINES = [
    "django.db.backends.postgresql_psycopg2",
    "django.contrib.gis.db.backends.postgis"
]


class PgArrayField(models.Field):
    default_error_messages = {
        'invalid': _(u"'%s' array must be comma separeted values."),
    }
    description = _("Array")
    
    __metaclass__ = models.SubfieldBase

    def __init__(self, fieldtype, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        kwargs.setdefault('default', None)
        
        field_kwargs = kwargs.copy()
        field_kwargs['blank'] = kwargs.pop('blank_item', False)
        field_kwargs['unique'] = kwargs.pop('unique_item', True)
        
        self._fieldtype = fieldtype(*args, **field_kwargs)
        self._textfield = models.TextField(*args, **kwargs)
        super(PgArrayField, self).__init__(*args, **kwargs)
    
    def db_type(self, connection):
        if not connection.settings_dict['ENGINE'] in PG_ENGINES:
            return self._textfield.db_type(connection)
        return '%s[]' % self._fieldtype.db_type(connection)
    
    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, basestring):
            value = csv_to_list(value)
        if isinstance(value, (list,tuple)):
            if not self._fieldtype.blank:
                value = [v for v in value if v]
            if self._fieldtype.unique:
                value = list(set(value))
            to_python = self._fieldtype.to_python
            value = [to_python(v) for v in value]
            return value
        
        e = default_error_messages('invalid')
        raise ValidationError(e)
    
    def get_prep_value(self, value):
        if value is None:
            return value
        
        get_prep_value = self._fieldtype.get_prep_value
        
        if isinstance(value, (list, tuple)):
            return [get_prep_value(v) for v in value]
        else:
            return get_prep_value(value)
    
    def get_db_prep_value(self, value, connection, prepared=False):
        value = value if prepared else self.get_prep_value(value)
        
        if not value:
            return value
        if not connection.settings_dict['ENGINE'] in PG_ENGINES:
            value = list_to_csv(value)
            return self._textfield.get_db_prep_value(value)
        
        get_db_prep_value = self._fieldtype.get_db_prep_value
        
        if isinstance(value, (list, tuple)):
            return [get_db_prep_value(v, connection, True) for v in value]
        else:
            return get_db_prep_value(value)
    
    def get_prep_lookup(self, lookup_type, value):
        """
        Perform preliminary non-db specific lookup checks and conversions
        """
        
        if value:
            if isinstance(value, (list, tuple)):
                if hasattr(value[0], 'prepare'):
                    return [v.prepare() for v in values]
                if hasattr(value[0], '_prepare'):
                    return [v._prepare() for v in values]
            else:
                if hasattr(value, 'prepare'):
                    return [v.prepare() for v in values]
                if hasattr(value, '_prepare'):
                    return [v._prepare() for v in values]
                
        
        # TODO clean valid lookups
        #if lookup_type in (
        #        'regex', 'iregex', 'month', 'day', 'week_day', 'search',
        #        'contains', 'icontains', 'iexact', 'startswith', 'istartswith',
        #        'endswith', 'iendswith', 'isnull',
        #        'exact', 'gt', 'gte', 'lt', 'lte',
        #        'range', 'in',
        #        'year'
        #    ):
        #    return value
        #else:
        #    e = _(u"%s is not a valid lookup for array field" % lookup_type)
        #    raise ValueError(e)
        
        return self.get_prep_value(value)
    
    def formfield(self, *args, **kwargs):
        defaults = {'form_class':PgArrayFormField(self._fieldtype)}
        defaults.update(kwargs)
        return super(PgArrayField, self).formfield(*args, **defaults)
    
    #def value_to_string(self, obj):
    #    value = self._get_val_from_obj(obj)
    #    if isinstance(value, (list, tuple)):
    #        value = list_to_csv(value)
    #    return value


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['django_postgres_array\.fields\.PgArrayField'])
except ImportError:
    pass
