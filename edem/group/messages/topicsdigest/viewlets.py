# coding=utf-8
from gs.group.messages.topicsdigest.viewlets import HeaderFooterViewlet as HeaderFooterBase
from Products.GSGroupMember.groupMembersInfo import GSGroupMembersInfo

class HeaderFooterViewlet(HeaderFooterBase):
    """Provides properties needed for the E-Dem Digest header """

    def __init__(self, context, request, view, manager):
        super(HeaderFooterBase, self).__init__(context, request, view, manager)
        self.groupMembersInfo = GSGroupMembersInfo(self.groupInfo)

    @property
    def groupMembersCount(self):
        return self.groupMembersInfo.fullMemberCount
    
    @property
    def groupFacebookPage(self):
        facebookId = self.groupInfo.get_property('facebookId', '') 
        if facebookId is None: return None
        else: return 'https://www.facebook.com/%s' % facebookId

    @property
    def groupTwitterPage(self):
        twitterId = self.groupInfo.get_property('twitterId', '')
        if twitterId is None: return None
        else: return 'https://twitter.com/%s' % twitterId
