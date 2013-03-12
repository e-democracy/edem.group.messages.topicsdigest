# coding=utf-8
from zope.cachedescriptors.property import Lazy
from gs.group.messages.topicsdigest.notifiers import DynamicTopicsDigestNotifier as Base
from topicsDigest import DailyTopicsDigest, ReminderTopicsDigest

class DynamicTopicsDigestNotifier(Base):

    def __init__(self, group, request):
        super(DynamicTopicsDigestNotifier, self).__init__(group, request)

    @Lazy
    def subject(self):
        m = '[{groupShortName}] Digest: {new_posts} New, '\
            '{new_topics} Topics - {a_subject}'
        shortName = self.groupInfo.get_property('short_name',
                                                self.groupInfo.name)
        digestStats = self.topicsDigest.post_stats
        a_subject = self.topicsDigest.topics[0]['topic_subject']
        retval = m.format(groupShortName=shortName,
                          new_posts=digestStats['new_posts'],
                          new_topics=digestStats['new_topics'],
                          a_subject=a_subject)
        assert retval
        return retval

    @Lazy
    def topicsDigest(self):
        retval = DailyTopicsDigest(self.context, self.siteInfo)
        if not retval.show_digest:
            retval = ReminderTopicsDigest(self.context, self.siteInfo)
        return retval
