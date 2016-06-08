# -*- coding: utf-8 -*-
def widget(**kwargs):
    return lambda field, value, kwargs=kwargs: SQLFORM.widgets[field.type].widget(field, value, **kwargs)
