from django.core.mail import send_mail as old_send_mail
from django.template import loader


def send_mail(
    sender, receivers, subject, context={},
    template_html=None, template_txt=None,
    plain_message='', fail_silently=False
):

    extras = {}

    if template_txt:
        template_txt = loader.get_template(template_txt)
        plain_message = template_txt.render(context)

    if template_html:
        template_html = loader.get_template(template_html)
        extras['html_message'] = template_html.render(context)

    old_send_mail(
        subject, plain_message, sender,
        receivers, fail_silently=fail_silently,
        **extras
    )
