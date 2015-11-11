# coding=utf-8
from __future__ import absolute_import, unicode_literals, print_function
from zope.cachedescriptors.property import Lazy
from gs.group.messages.text import HTMLBody
from gs.group.messages.topic.digest.daily.topicsdigest import \
    DailyTopicsDigest as BaseDailyTopicsDigest
from edem.group.messages.topic.digest.weekly.topicsdigest import \
    WeeklyTopicsDigest as BaseWeeklyTopicsDigest
from .queries import DigestQuery

CLIP_LENGTH = 500


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

    def format_topic(self, topic):
        topic = super(DailyTopicsDigest, self).format_topic(topic)

        if len(topic['last_post_body']) > CLIP_LENGTH:
            topic['last_post_more_available'] = True
            topic['last_post_clip'] = topic['last_post_body'][:CLIP_LENGTH]

            # Remove cutoff words
            if not topic['last_post_clip'][-1].isspace():
                topic['last_post_clip'] = \
                    topic['last_post_clip'].rsplit(None, 1)[0]
        else:  # len(topic['last_post_body']) <= CLIP_LENGTH:
            topic['last_post_more_available'] = False
            topic['last_post_clip'] = topic['last_post_body']

        # --=mpj17=-- Use the standard *email* formatting for the
        # post-clip
        assert len(topic['last_post_clip']) <= CLIP_LENGTH, 'Clip too long'
        htmlBody = HTMLBody(topic['last_post_clip'])
        markedUpClip = unicode(htmlBody)
        # --=mpj17=-- I do not know why this fails for
        # http://forums.e-democracy.org/groups/frambors/gs-group-messages-topic-digest-daily.html
        # assert len(markedUpClip) >= len(topic['last_post_clip']), 'Markup destroyed info'
        topic['last_post_clip'] = markedUpClip
        return topic


class ReminderTopicsDigest(BaseWeeklyTopicsDigest):

    def __init__(self, context, siteInfo):
        super(ReminderTopicsDigest, self).__init__(context, siteInfo)
        self.frequency = 30

    @Lazy
    def messageQuery(self):
        retval = DigestQuery()
        return retval
