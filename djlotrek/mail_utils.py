
from mimetypes import guess_extension
from django.core.mail import EmailMultiAlternatives

from django.template import loader


def send_mail(
    sender, receivers, subject, context={},
    template_html=None, template_txt=None,
    plain_message='', fail_silently=False,
    cc=[], bcc=[], files=[], headers=None, reply_to=None
):

    plain_message = ''
    html_text = ''

    if template_txt:
        template_txt = loader.get_template(template_txt)
        plain_message = template_txt.render(context)

    if template_html:
        template_html = loader.get_template(template_html)
        html_text = template_html.render(context)

    mail = EmailMultiAlternatives(
        subject=subject,
        body=plain_message or html_text,
        from_email=sender,
        to=receivers,
        cc=cc,
        bcc=bcc,
        alternatives=((html_text or plain_message, 'text/html'),),
        headers=headers,
        reply_to=reply_to
    )

    for file_item in files:
        if file_item.get('path'):
            mail.attach_file(file_item['path'])
        elif file_item.get('data') and file_item.get('content-type'):
            mail.attach(
                file_item.get('filename', 'file' + guess_extension(file_item['content-type'])),
                file_item['data'], file_item['content-type']
            )
    mail.send(fail_silently)
