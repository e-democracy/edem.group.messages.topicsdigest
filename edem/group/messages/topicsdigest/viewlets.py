# coding=utf-8
from __future__ import absolute_import, unicode_literals
import datetime as dt
from gs.group.messages.topic.digest.base.viewlets import HeaderFooterViewlet as \
    HeaderFooterBase, DailyTopicsDigestViewlet, WeeklyTopicsDigestViewlet
from Products.GSGroupMember.groupMembersInfo import GSGroupMembersInfo
from .topicsDigest import ReminderTopicsDigest


class HeaderFooterViewlet(HeaderFooterBase):
    """Provides properties needed for the E-Dem Digest header """

    def __init__(self, context, request, view, manager):
        super(HeaderFooterBase, self).__init__(context, request, view, manager)
        self.groupMembersInfo = GSGroupMembersInfo(context)

    @property
    def groupMembersCount(self):
        return self.groupMembersInfo.fullMemberCount

    @property
    def groupFacebookPage(self):
        facebookId = self.groupInfo.get_property('facebookId', '')
        if not facebookId:
            return None
        else:
            return 'https://www.facebook.com/%s' % facebookId

    @property
    def groupTwitterPage(self):
        twitterId = self.groupInfo.get_property('twitterId', '')
        if not twitterId:
            return None
        else:
            return 'https://twitter.com/%s' % twitterId

    @property
    def groupEmail(self):
        config = getattr(self.context, 'GlobalConfiguration')
        self.emailDomain = config.getProperty('emailDomain')
        return '%s@%s' % (self.groupInfo.get_id(), self.emailDomain)

    @property
    def supportEmail(self):
        config = getattr(self.context, 'GlobalConfiguration')
        retval = config.getProperty('supportEmail', '')

        assert retval
        return retval

    @property
    def today(self):
        return dt.date.today().isoformat()



class EDemDailyTopicsDigestViewlet(DailyTopicsDigestViewlet):

    def __init__(self, context, request, view, manager):
        super(EDemDailyTopicsDigestViewlet, self).\
            __init__(context, request, view, manager)

    @property
    def topicsDigest(self):
        retval = self.manager.topicsDigest
        assert retval
        return retval
###
### List Viewlets###
###


class DailyTopicsDigestListViewlet(EDemDailyTopicsDigestViewlet):

    def __init__(self, context, request, view, manager):
        super(DailyTopicsDigestListViewlet, self).\
            __init__(context, request, view, manager)
        self.groupMembersInfo = GSGroupMembersInfo(context)

    @property
    def groupEmail(self):
        config = getattr(self.context, 'GlobalConfiguration')
        emailDomain = config.getProperty('emailDomain')
        return '%s@%s' % (self.groupInfo.get_id(), emailDomain)

    @property
    def groupMembersCount(self):
        return self.groupMembersInfo.fullMemberCount

    @property
    def groupFacebookPage(self):
        facebookId = self.groupInfo.get_property('facebookId', '')
        if not facebookId:
            return None
        else:
            return 'https://www.facebook.com/%s' % facebookId

    @property
    def groupTwitterPage(self):
        twitterId = self.groupInfo.get_property('twitterId', '')
        if not twitterId:
            return None
        else:
            return 'https://twitter.com/%s' % twitterId



class ReminderTopicsDigestListViewlet(WeeklyTopicsDigestViewlet):

    def __init__(self, context, request, view, manager):
        super(ReminderTopicsDigestListViewlet, self).\
            __init__(context, request, view, manager)
        self.__topicsDigest__ = \
            ReminderTopicsDigest(self.context, self.siteInfo)
        self.groupMembersInfo = GSGroupMembersInfo(context)

    @property
    def groupEmail(self):
        config = getattr(self.context, 'GlobalConfiguration')
        emailDomain = config.getProperty('emailDomain')
        return '%s@%s' % (self.groupInfo.get_id(), emailDomain)

    @property
    def groupMembersCount(self):
        return self.groupMembersInfo.fullMemberCount

    @property
    def groupFacebookPage(self):
        facebookId = self.groupInfo.get_property('facebookId', '')
        if not facebookId:
            return None
        else:
            return 'https://www.facebook.com/%s' % facebookId

    @property
    def groupTwitterPage(self):
        twitterId = self.groupInfo.get_property('twitterId', '')
        if not twitterId:
            return None
        else:
            return 'https://twitter.com/%s' % twitterId


###
### Clip Viewlets ###
###


class DailyTopicsDigestClipsViewlet(EDemDailyTopicsDigestViewlet):

    def __init__(self, context, request, view, manager):
        super(DailyTopicsDigestClipsViewlet, self).\
            __init__(context, request, view, manager)
