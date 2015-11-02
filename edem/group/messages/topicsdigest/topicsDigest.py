# coding=utf-8
from __future__ import absolute_import, unicode_literals, print_function
from zope.cachedescriptors.property import Lazy
from gs.group.messages.post.text.postbody import escape_word, markup_uri, markup_www
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

    @staticmethod
    def markup_word(curr_word):
        curr_word = escape_word(curr_word)
        mu_word = markup_uri(None, curr_word, False, [])
        if mu_word == curr_word:
            mu_word = markup_www(None, curr_word, False, [])
        return mu_word

    def format_topic(self, topic):
        topic = super(DailyTopicsDigest, self).format_topic(topic)

        if len(topic['last_post_body']) > CLIP_LENGTH:
            topic['last_post_more_available'] = True
            topic['last_post_clip'] = topic['last_post_body'][:CLIP_LENGTH]

            # Remove cutoff words
            if not topic['last_post_clip'][-1].isspace():
                topic['last_post_clip'] = \
                    topic['last_post_clip'].rsplit(None, 1)[0]

        else:
            topic['last_post_more_available'] = False
            topic['last_post_clip'] = topic['last_post_body']

        # Markup Links with a loop inspired by
        # gs.group.messages.post.postbody.markup_email.
        # HACK: The markup functions in gs.group.messages.post take a
        # ContentProvider as an argument, but most do not actually reference
        # it. Since we don't have a ContentProvider here, we'll just exploit
        # the non-use of the argument.
        marked_up_clip = ''
        curr_word = ''

        for char in topic['last_post_clip']:
            if char.isspace():
                if curr_word:
                    mu_word = self.markup_word(curr_word)
                    curr_word = ''
                    marked_up_clip += mu_word
                if char == '\n':
                    char = '<br/>'
                marked_up_clip += char
            else:
                curr_word += char
        if curr_word:
            mu_word = self.markup_word(curr_word)
            marked_up_clip += mu_word

        topic['last_post_clip'] = marked_up_clip
        return topic


class ReminderTopicsDigest(BaseWeeklyTopicsDigest):

    def __init__(self, context, siteInfo):
        super(ReminderTopicsDigest, self).__init__(context, siteInfo)
        self.frequency = 30

    @Lazy
    def messageQuery(self):
        retval = DigestQuery()
        return retval
