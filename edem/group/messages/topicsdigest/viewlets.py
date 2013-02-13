# coding=utf-8
from topicsDigest import DailyTopicsDigest
from gs.group.messages.topicsdigest.viewlets import HeaderFooterViewlet as HeaderFooterBase, DailyTopicsDigestViewlet 
from Products.GSGroupMember.groupMembersInfo import GSGroupMembersInfo

class HeaderFooterViewlet(HeaderFooterBase):
    """Provides properties needed for the E-Dem Digest header """

    def __init__(self, context, request, view, manager):
        super(HeaderFooterBase, self).__init__(context, request, view, manager)
        self.groupMembersInfo = GSGroupMembersInfo(self.groupInfo)

    @property
    def groupMembersCount(self):
        return self.groupInfo.group_members_info.fullMemberCount
    
    @property
    def groupFacebookPage(self):
        facebookId = self.groupInfo.get_property('facebookId', '') 
        if not facebookId: return None
        else: return 'https://www.facebook.com/%s' % facebookId

    @property
    def groupTwitterPage(self):
        twitterId = self.groupInfo.get_property('twitterId', '')
        if not twitterId: return None
        else: return 'https://twitter.com/%s' % twitterId
###
### List Viewlets###
###

class DailyTopicsDigestListViewlet(DailyTopicsDigestViewlet):

    def __init__(self, context, request, view, manager):
        super(DailyTopicsDigestListViewlet, self).__init__(context, request,
                                                    view, manager)

    @property
    def groupEmail(self):
        config = getattr(self.context, 'GlobalConfiguration')
        emailDomain = config.getProperty('emailDomain') 
        return '%s@%s' % (self.groupInfo.get_id(), emailDomain)

###
### Clip Viewlets ###
###

class DailyTopicsDigestClipsViewlet(DailyTopicsDigestViewlet):

    def __init__(self, context, request, view, manager):
        super(DailyTopicsDigestClipsViewlet, self).__init__(context, request,
                                                    view, manager)
        self.__topicsDigest__ = DailyTopicsDigest(self.context, self.siteInfo)


