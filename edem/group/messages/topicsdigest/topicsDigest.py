# coding=utf-8

from queries import DigestQuery
from zope.cachedescriptors.property import Lazy
from gs.group.messages.topicsdigest.topicsDigest import \
    DailyTopicsDigest as BaseDailyTopicsDigest, \
    WeeklyTopicsDigest as BaseWeeklyTopicsDigest

from logging import getLogger
log = getLogger('edem.group.messages.topicsdigest.TopicsDigest')

clip_length = 250

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
        else:
            topic['last_post_more_available'] = False
            topic['last_post_clip'] = topic['last_post_body']

        topic['last_post_clip'] = topic['last_post_clip'].replace('\n', '<br/>')
        topic['topic_url'] = topic['topic_url'] + '?rb=topicsdigest-daily'
        return topic

class WeeklyTopicsDigest(BaseWeeklyTopicsDigest):
    pass
