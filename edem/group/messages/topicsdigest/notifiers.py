# coding=utf-8
from zope.cachedescriptors.property import Lazy
from gs.group.messages.topicsdigest.notifiers import DynamicTopicsDigestNotifier as Base
from topicsDigest import DailyTopicsDigest, WeeklyTopicsDigest

class DynamicTopicsDigestNotifier(Base):

    def __init__(self, group, request):
        super(DynamicTopicsDigestNotifier, self).__init__(group, request)
        
    @Lazy
    def topicsDigest(self):
        retval = DailyTopicsDigest(self.context, self.siteInfo)
        if not retval.show_digest:
            retval = WeeklyTopicsDigest(self.context, self.siteInfo)
        return retval
