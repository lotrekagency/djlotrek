from mock import Mock, patch, call
from django.test import TestCase

from djlotrek import mail_utils


class SendMailTestCase(TestCase):

    def setUp(self):
        """Setup test instance with default data"""
        self.template_txt = 'test template txt',
        self.template_html = '<html><body>test</body></html'
        self.params = {
            'sender': 'me@lotrek.it',
            'receivers': ['they@another.it'],
            'subject': 'subject test',
            'context': {'data': 'testing context'},
            'template_html': self.template_html,
            'template_txt': self.template_txt,
            'plain_message': 'test plain'
        }

        self.render_plain = Mock()
        self.render_plain.render = Mock(return_value='plain body')
        self.render_html = Mock()
        self.render_html.render = Mock(return_value='html body')

    def test_required_functions(self):
        """Test if required functions exists"""
        self.assertIsNotNone(mail_utils.send_mail)

    @patch('djlotrek.mail_utils.EmailMultiAlternatives')
    @patch('djlotrek.mail_utils.loader')
    def test_sender_call(self, mocked_loader, mocked_sender):
        """Test email sender is called with correctly parameters"""
        mocked_loader.get_template = Mock(
            side_effect=[self.render_plain, self.render_html])

        # call the function being tested
        mail_utils.send_mail(**self.params)

        # assert calls
        get_template_calls = [
            call(self.template_txt),
            call(self.template_html)
        ]
        mocked_loader.get_template.assert_has_calls(get_template_calls)
        mocked_sender.assert_called_once_with(
            subject='subject test',
            body='plain body',
            from_email='me@lotrek.it',
            to=['they@another.it'],
            cc=[],
            bcc=[],
            alternatives=(('html body', 'text/html'),),
            headers=None
        )

    @patch('djlotrek.mail_utils.EmailMultiAlternatives')
    @patch('djlotrek.mail_utils.loader')
    def test_sender_multiple_call(self, mocked_loader, mocked_sender):
        """
        Test email sender is called multiple times with corretly parameters
        """
        get_templates_return = [self.render_plain, self.render_html]
        mocked_loader.get_template = Mock(side_effect=get_templates_return)
        cc = ['one@test.it', 'two@test.it']
        self.params.update({'cc': cc})

        # call the function being tested
        mail_utils.send_mail(**self.params)

        # assert calls
        mocked_sender.assert_called_once_with(
            subject='subject test',
            body='plain body',
            from_email='me@lotrek.it',
            to=['they@another.it'],
            cc=cc,
            bcc=[],
            alternatives=(('html body', 'text/html'),),
            headers=None
        )

        mocked_loader.get_template.side_effect = get_templates_return
        mocked_sender.reset_mock()

        del(cc[1])
        self.params.update({
            'sender': 'second_me@lotrek.it',
            'receivers': ['they@another.it', 'more@test.it'],
            'subject': 'subject testing again',
            'template_html': self.template_html,
            'template_txt': self.template_txt,
            'plain_message': 'test plain second time',
            'cc': cc,
            'bcc': ['tests@test.it']
        })

        # call the function being tested
        mail_utils.send_mail(**self.params)

        # assert calls
        mocked_sender.assert_called_once_with(
            subject='subject testing again',
            body='plain body',
            from_email='second_me@lotrek.it',
            to=['they@another.it', 'more@test.it'],
            cc=cc,
            bcc=['tests@test.it'],
            alternatives=(('html body', 'text/html'),),
            headers=None
        )

    @patch('djlotrek.mail_utils.EmailMultiAlternatives')
    @patch('djlotrek.mail_utils.loader')
    def test_sender_call_only_plain_body(self, mocked_loader, mocked_sender):
        """Test sender is called only with plain body"""
        mocked_loader.get_template = Mock(return_value=self.render_plain)
        self.params.pop('template_html', None)

        # call the function being tested
        mail_utils.send_mail(**self.params)

        # assert calls
        mocked_sender.assert_called_once_with(
            subject='subject test',
            body='plain body',
            from_email='me@lotrek.it',
            to=['they@another.it'],
            cc=[],
            bcc=[],
            alternatives=(('plain body', 'text/html'),),
            headers=None
        )

    @patch('djlotrek.mail_utils.EmailMultiAlternatives')
    @patch('djlotrek.mail_utils.loader')
    def test_sender_call_only_html_body(self, mocked_loader, mocked_sender):
        """Test sender is called only with html body"""
        mocked_loader.get_template = Mock(return_value=self.render_html)
        self.params.pop('template_txt', None)

        # call the function being tested
        mail_utils.send_mail(**self.params)

        # assert calls
        mocked_sender.assert_called_once_with(
            subject='subject test',
            body='html body',
            from_email='me@lotrek.it',
            to=['they@another.it'],
            cc=[],
            bcc=[],
            alternatives=(('html body', 'text/html'),),
            headers=None
        )

    @patch('djlotrek.mail_utils.EmailMultiAlternatives')
    @patch('djlotrek.mail_utils.loader')
    def test_sender_call_with_files(self, mocked_loader, mocked_sender):
        """Test sender called with files"""
        mocked_loader.get_template = Mock(
            side_effect=[self.render_plain, self.render_html])

        fake_files = [
            {'path': 'path_test'},
            {'without_path': 'another_path'},
            {'path': 'another_path'},
            {'data': 'data', 'content-type': 'image/png'},
            {'data': 'data2', 'filename': 'testfilename.jpeg', 'content-type': 'image/jpeg'},
        ]
        self.params.update({'files': fake_files})

        # call the function being tested
        mail_utils.send_mail(**self.params)

        # assert calls
        mocked_sender.return_value.attach_file.assert_has_calls([
            call('path_test'),
            call('another_path'),
        ])

        mocked_sender.return_value.attach.assert_has_calls([
            call('file.png', 'data', 'image/png'),
            call('testfilename.jpeg', 'data2', 'image/jpeg')
        ])

    @patch('djlotrek.mail_utils.EmailMultiAlternatives')
    @patch('djlotrek.mail_utils.loader')
    def test_sender_call_send_method(self, mocked_loader, mocked_sender):
        """Test send method called with correctly parameter"""
        get_templates_return = [self.render_plain, self.render_html]
        mocked_loader.get_template = Mock(side_effect=get_templates_return)

        # call the function being tested
        mail_utils.send_mail(**self.params)

        # assert calls
        mocked_sender.return_value.send.assert_called_once_with(False)

        mocked_loader.get_template.side_effect = get_templates_return
        self.params.update({'fail_silently': True})
        mocked_sender.reset_mock()

        # call the function being tested
        mail_utils.send_mail(**self.params)

        # assert calls
        mocked_sender.return_value.send.assert_called_once_with(True)
