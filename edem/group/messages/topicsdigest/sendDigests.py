# coding=utf-8
from zope.formlib import form
from notifiers import DynamicTopicsDigestNotifier
from gs.group.messages.topicsdigest.sendDigests import SendAllDigests as Base

from logging import getLogger
log = getLogger('edem.group.messages.topicsdigest.sendDigests')

class SendAllDigests(Base):

    @form.action(label=u'Send', failure='handle_send_all_digests_failure')
    def handle_send_all_digests(self, action, data):
        log.info('Processing the digests')

        for site in self.sites:
            for group in self.groups_for_site(site):
                tdn = DynamicTopicsDigestNotifier(group, self.request)
                tdn.notify()

        log.info('All digests sent')
        self.status = u'<p>All digests sent.</p>'

    def handle_send_all_digests_failure(self, action, data, errors):
        super(SendAllDigests, self).handle_send_all_digests_failure(action,
                                    date, errors)
