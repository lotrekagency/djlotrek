def wrap_widget(form, related_wrapper, model, field):
    form.fields[field].widget = related_wrapper(
        form.fields[field].widget,
        model._meta.get_field(field).rel,
        form.admin_site
    )
