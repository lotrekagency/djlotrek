from django.core.mail import send_mail as old_send_mail
from django.core.mail import EmailMultiAlternatives

from django.template import loader


def send_mail(
    sender, receivers, subject, context={},
    template_html=None, template_txt=None,
    plain_message='', fail_silently=False,
    cc=[], bcc=[],files=[]
):

    extras = {}
    plain_message = ''
    html_text = ''

    if template_txt:
        template_txt = loader.get_template(template_txt)
        plain_message = template_txt.render(context)

    if template_html:
        template_html = loader.get_template(template_html)
        html_text = template_html.render(context)

    mail = EmailMultiAlternatives(
        subject=subject, body=plain_message or html_text, 
        from_email=sender, to=receivers,
        cc=cc, bcc=bcc,
        alternatives=((html_text or plain_message, 'text/html'),)
    )

    for file in files:
        if file['path']:
            mail.attach_file(file['path'])
    mail.send(fail_silently)
