# coding=utf-8
from __future__ import absolute_import, unicode_literals
from zope.formlib import form
from gs.group.messages.topic.digest.base.sendDigests import SendDigest \
    as Base
#from .notifiers import DynamicTopicsDigestNotifier

from logging import getLogger
log = getLogger('edem.group.messages.topicsdigest.sendDigests')


class SendAllDigests(Base):

    @form.action(label='Send', failure='handle_send_all_digests_failure')
    def handle_send_all_digests(self, action, data):
        log.info('Processing the digests')

        for site in self.sites:
            for group in self.groups_for_site(site):
                pass
#                tdn = DynamicTopicsDigestNotifier(group, self.request)
#                tdn.notify()

        log.info('All digests sent')
        self.status = '<p>All digests sent.</p>'

    def handle_send_all_digests_failure(self, action, data, errors):
        super(SendAllDigests, self)\
            .handle_send_all_digests_failure(action, data, errors)
