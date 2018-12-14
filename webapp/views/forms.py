# -*- coding: utf-8 -*-

from wtforms.fields.html5 import DateField
import datetime


class CzechDateField(DateField):
    """
    Overrides the process_formdata() method definition in a standard DateField
    """
    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist)
            try:
                self.data = datetime.datetime.strptime(date_str, self.format).date()
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Neplatný formát data!'))