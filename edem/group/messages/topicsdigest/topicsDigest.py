# coding=utf-8

from queries import DigestQuery
from zope.cachedescriptors.property import Lazy
from gs.group.messages.topicsdigest.topicsDigest import \
    DailyTopicsDigest as BaseDailyTopicsDigest, \
    WeeklyTopicsDigest as BaseWeeklyTopicsDigest

from logging import getLogger
log = getLogger('edem.group.messages.topicsdigest.TopicsDigest')

clip_length = 500 


class DailyTopicsDigest(BaseDailyTopicsDigest):
    """ Represents the content of an E-Democracy daily digest.

       Dicts in the list provided by topics include the following attributes,
       in addition to the attributes provided by
       gs.group.messages.topicsdigest.DailyTopicsDigest:
           last_post_body - The full text content of the last post in a topic
           last_post_clip - A string of the first X characters of the last post
                            in a topic
           last_post_more_available - A boolean indicating if there is more
                                      text available from the last post than
                                      is present in the clip
           oldest_new_post_id = ID of the oldest post made since yesterday
        """

    def __init__(self, context, siteInfo):
        super(DailyTopicsDigest, self).__init__(context, siteInfo)

    @Lazy
    def messageQuery(self):
        retval = DigestQuery()
        return retval

    def __formatTopic__(self, topic):
        topic = super(DailyTopicsDigest, self).__formatTopic__(topic)

        if len(topic['last_post_body']) > clip_length:
            topic['last_post_more_available'] = True
            topic['last_post_clip'] = topic['last_post_body'][:clip_length]
            
            # Remove cutoff words
            if not topic['last_post_clip'][-1].isspace():
                topic['last_post_clip'] = \
                    topic['last_post_clip'].rsplit(None, 1)[0]
        else:
            topic['last_post_more_available'] = False
            topic['last_post_clip'] = topic['last_post_body']

        topic['last_post_clip'] = topic['last_post_clip']\
            .replace('\n', '<br/>')
        return topic


class ReminderTopicsDigest(BaseWeeklyTopicsDigest):

    def __init__(self, context, siteInfo):
        super(ReminderTopicsDigest, self).__init__(context, siteInfo)
        self.frequency = 30

    @Lazy
    def messageQuery(self):
        retval = DigestQuery()
        return retval
