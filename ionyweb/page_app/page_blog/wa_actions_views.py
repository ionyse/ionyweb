# -*- coding: utf-8 -*-
from ionyweb.administration.actions.views import ActionAdminDetailView

class EntryActionAdminDetailView(ActionAdminDetailView):
    def get_new_form(self, *args, **kwargs):
        entry_kwargs = self._get_entry_form_kwargs(*args, **kwargs)
        entry_kwargs.update(kwargs)
        return super(EntryActionAdminDetailView, self).get_new_form(*args, **entry_kwargs)


    def get_edit_form(self, *args, **kwargs):
        entry_kwargs = self._get_entry_form_kwargs(*args, **kwargs)
        entry_kwargs.update(kwargs)
        return super(EntryActionAdminDetailView, self).get_edit_form(*args, **entry_kwargs)


    def _get_entry_form_kwargs(self, *args, **kwargs):
        try:
            app_obj = kwargs.pop('app_obj')
            categories_set = app_obj.categories.all()
        except KeyError:
            categories_set = None

        website = self.request.website
        
        if self.request.is_superuser:
            authors_set = website.owners.all()
            authors_choices = [(author.id, author.email) for author in authors_set]        
        else:
            authors_choices = [(self.request.user.pk, self.request.user.email)]

        return {'categories_set': categories_set,
                'authors_choices': authors_choices}

        
