from django import forms


class PgArrayWidget(forms.MultiWidget):
    def __init__(self, field, attrs=None):
        
        widgets = (DateInput(attrs=attrs, format=date_format),
                   TimeInput(attrs=attrs, format=time_format))
        super(SplitDateTimeWidget, self).__init__(widgets, attrs)
    
    def __init__(self, *args, **kwargs):
        return super(PgArrayWidget, self).__init__(*args, **kwargs)
        
    def render(self, name, value, attrs):
        if value is None:
            value = ""
        elif isinstance(value, (str, unicode)):
            pass
        else:
            if isinstance(value, int):
                value = datetime.timedelta(seconds=value)
            value = nice_repr(value)
        return super(TimedeltaWidget, self).render(name, value, attrs)
    
    def _has_changed(self, initial, data):
        """
        We need to make sure the objects are of the canonical form, as a
        string comparison may needlessly fail.
        """
        if initial in ["", None] and data in ["", None]:
            return False
            
        if initial in ["", None] or data in ["", None]:
            return True
        
        if initial:
            if not isinstance(initial, datetime.timedelta):
                initial = parse(initial)

        if not isinstance(data, datetime.timedelta):
            data = parse(data)
        
        return initial != data