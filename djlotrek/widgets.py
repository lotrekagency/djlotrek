from django.contrib.admin import widgets
from django.contrib.admin.views.main import IS_POPUP_VAR, TO_FIELD_VAR
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.urls import reverse


def wrap_widget(form, related_wrapper, model, field):
    widget = related_wrapper(
        form.fields[field].widget,
        model._meta.get_field(field).rel,
        form.admin_site
    )
    form.fields[field].widget = widget
    return widget


class RelatedOneToOneWidgetWrapper(widgets.RelatedFieldWidgetWrapper):

    template_name = 'djlotrek/widgets/related_one_to_one_widget_wrapper.html'

    def add_model_choices(self, model_choices):
        self._model_choices = model_choices

    def get_context(self, name, value, attrs):

        context = {}

        context['name'] = name

        context['widget'] = self.widget.render(name, value, attrs)

        context['model_choices'] = []

        for template_model in self._model_choices:
            info = (
                self.rel.to._meta.app_label,
                template_model['class']._meta.object_name.lower()
            )

            # if self.can_add_related:
            related_url = reverse(
                'admin:%s_%s_add'
                % info, current_app=self.admin_site.name
            )
            url_params = '&'.join("%s=%s" % param for param in [
                (TO_FIELD_VAR, self.rel.get_related_field().name),
                (IS_POPUP_VAR, 1),
            ])
            related_url = related_url + '?' + url_params

            context['model_choices'].append(
                {
                    'related_url': related_url,
                    'label':  template_model['label'],
                    'extras': template_model.get('extras', '')
                }
            )

        return context

    def render(self, name, value, attrs):

        self.widget.choices = self.choices

        context = self.get_context(name, value, attrs)

        html = render_to_string(
            self.template_name,
            context
        )
        return mark_safe(html)
