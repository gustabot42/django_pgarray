# -*- coding: utf-8 -*-

from django.db import models
from django.core import exceptions, validators
from django.utils.translation import ugettext_lazy as 

from forms import PgArrayFormField


class PgArrayField(models.Field):
    default_error_messages = {
        'invalid': _(u"'%s' value must be array."),
    }
    description = _("Array")
    
    __metaclass__ = models.SubfieldBase

    def __init__(self, field, *args, **kwargs):
        assert(isintance(field, models.Field))
        self._field = field(*args, **kwargs)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        kwargs.setdefault('default', None)
        super(PgArrayField, self).__init__(*args, **kwargs)
    
    def db_type(self, connection):
        return '%s[]' % self._field.db_type(connection)
    
    def to_python(self, value):
        field = self._field
        if value in validators.EMPTY_VALUES:
            return []
        if isinstance(value, (list,tuple)):
            return map(field.to_python, value)
        return value
    
    def get_prep_value(self, value):
        field = self._field
        return [field.get_prep_value(v) for v in value]
    
    def get_db_prep_value(self, value, connection, prepared=False):
        field = self._field
        value = value if prepared else self.get_prep_value(value)
        
        if not value:
            return value
        value = [field.get_db_prep_value(v, connection, True) for v in value]
        return value
    
    def get_prep_lookup(self, lookup_type, value):
        """
        Perform preliminary non-db specific lookup checks and conversions
        """
        if value:
            if hasattr(value[0], 'prepare'):
                return [v.prepare() for v in values]
            if hasattr(value[0], '_prepare'):
                return [v._prepare() for v in values]

        return self.get_prep_value(value)
    
    def formfield(self, *args, **kwargs):
        defaults = {'form_class':PgArrayFormField()}
        defaults.update(kwargs)
        return super(PgArrayField, self).formfield(*args, **defaults)
    
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return unicode(value)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['django_postgres_array\.fields\.PgArrayField'])
except ImportError:
    pass
