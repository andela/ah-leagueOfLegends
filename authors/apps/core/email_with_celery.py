from django.template.loader import render_to_string
# This File Contains celery tasks,
# Also the celery file we created in the root will collect all tasks defined
# accros django setting in the installed app


class SendEmail:
    ''' Responsible for sending email to registered users'''

    def __init__(self, subject='Authors Haven', e_from=None,
                 e_to=None, template=None, context=None):
        '''Intitializes mails content '''
        self.subject = subject
        self.e_from = e_from
        self.e_to = e_to
        self.template = template
        self.context = context
        if self.template:
            self.message = render_to_string(
                self.template, context=self.context)
        else:
            self.message = None

    def send(self):
        payload = {
                'subject': self.subject,
                'message': self.message,
                'to': self.e_to,
                'from_email': self.e_from
                }
        from authors.celery import task
        task.delay(payload)
