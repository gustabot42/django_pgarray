django_pgarray
##############

Django array field support for postgres, using unicode csv to save it in others database and to show it in text widget


usage
=====

the first attribute determines the item type through a field type

        from django_pgarray.fields import PgArrayField
        
        class MyModel(TimeStampedModel):
            tags = PgArrayField(models.CharField, verbose_name = _(u"tags"), max_length=80)


default atributes
-----------------

blank = True
null = True
default = None

blank_item = False    # allow blank items
unique_item = True    # treat array as a set


TODO
====

tests