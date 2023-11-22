from django.conf.urls.defaults import patterns, url

from .views import (ListView,
                    CreateView,
                    UpdateView,
                    DeleteView)


def bootstrap_patterns(*forms):
    patterns_ = patterns('')
    for form in forms:
        patterns_ += bootstrap_pattern(form)
    return patterns_


def bootstrap_pattern(form, **kwargs):
    model = form._meta.model
    name = model._meta.object_name.lower()

    urls = []

    if 'list_view' not in kwargs or kwargs.get('list_view') is not None:
        view = kwargs.get('list_view', ListView).as_view(model=model)
        url_ = kwargs.get('list_view_url', r'^%s/$' % name)
        urls.append(bootstrap_list(url_, view=view, name='%s_list' % name))

    if 'create_view' not in kwargs or kwargs.get('create_view') is not None:
        view = kwargs.get('create_view', CreateView).as_view(form_class=form)
        url_ = kwargs.get('create_view_url', r'^%s/add/$' % name)
        urls.append(bootstrap_create(url_, view=view, name='%s_form' % name))

    if 'update_view' not in kwargs or kwargs.get('update_view') is not None:
        view = kwargs.get('update_view', UpdateView).as_view(form_class=form)
        url_ = kwargs.get('update_view_url', r'^%s/(?P<pk>\d+)/$' % name)
        urls.append(bootstrap_update(url_, view=view, name='%s_form' % name))

    if 'delete_view' not in kwargs or kwargs.get('delete_view') is not None:
        view = kwargs.get('delete_view', DeleteView).as_view(model=model)
        url_ = kwargs.get('delete_view_url', r'^%s/(?P<pk>\d+)/delete/$' % name)
        urls.append(bootstrap_delete(url_, view=view, name='%s_delete' % name))

    return patterns('', *urls)


def bootstrap_list(url_, name, view=None, model=None):
    if view is None:
        view = ListView.as_view(model=model)
    return url(url_, view, name=name)


def bootstrap_create(url_, name, view=None, form=None):
    if view is None:
        view = CreateView.as_view(form_class=form)
    return url(url_, view, name=name)


def bootstrap_update(url_, name, view=None, form=None):
    if view is None:
        view = UpdateView.as_view(form_class=form)
    return url(url_, view, name=name)


def bootstrap_delete(url_, name, view=None, model=None):
    if view is None:
        view = DeleteView.as_view(model=model)
    return url(url_, view, name=name)
