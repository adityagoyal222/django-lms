from django.contrib.formtools.wizard.views import SessionWizardView as BaseSessionWizardView


class SessionWizardView(BaseSessionWizardView):
    def get_form_class(self):
        step = self.get_step_index()
        form = self.form_list[str(step)]

        if not hasattr(form, 'management_form'):
            # If isn't a FormSet
            return form

        formset = form
        form = formset.form

        return form

    def get_context_data(self, *args, **kwargs):
        context = super(SessionWizardView, self).get_context_data(*args, **kwargs)

        form_meta = self.get_form_class()._meta
        model_meta = form_meta.model._meta

        context['model_verbose_name'] = model_meta.verbose_name
        context['model_verbose_name_plural'] = model_meta.verbose_name_plural

        context['success_url'] = self.get_success_url()

        return context

    def get_success_url(self):
        form_meta = self.get_form_class()._meta
        model_meta = form_meta.model._meta

        app_label = model_meta.app_label
        name = model_meta.object_name.lower()

        return reverse('%s:%s_list' % (app_label, name))
