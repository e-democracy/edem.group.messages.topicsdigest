# coding=utf-8
import datetime
import sqlalchemy as sa
from gs.group.messages.topicsdigest.queries import DigestQuery as \
                                                    BaseDigestQuery
from gs.database import getSession

from logging import getLogger
log = getLogger('edem.group.messages.topicsdigest.DigestQuery')

class DigestQuery(BaseDigestQuery):
    
    def __init__(self):
        super(DigestQuery, self).__init__()

    def topics_sinse_yesterday(self, siteId, groupId):
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

        # SELECT topic.topic_id, topic.site_id, topic.group_id,
        #       topic.original_subject, topic.num_posts, topic.first_post_id,
        #       last_topic_post.post_id as last_post_id,
        #       last_topic_post.date as last_post_date,
        #       last_topic_post.user_id as last_author_id, 
        #       last_topic_post.body as last_post_body,
        #       (SELECT COUNT(1) 
        #           FROM post as all_new_topic_posts 
        #           WHERE all_new_topic_posts.topic_id = topic.topic_id 
        #               AND all_new_topic_posts.date >= timestamp 'now' -
        #                     interval '1 days') as num_posts_day,
        #       oldest_new_topic_post.post_id as oldest_new_post_id,
        #       topic_keywords.keywords
        #  FROM topic
        #       INNER JOIN topic_keywords 
        #           ON topic_keywords.topic_id = topic.topic_id
        #       INNER JOIN post as last_topic_post 
        #           ON last_topic_post.topic_id = topic.topic_id
        #       INNER JOIN post as oldest_new_topic_post 
        #           ON oldest_new_topic_post.topic_id = topic.topic_id

        tt = self.topicTable            
        tkt = self.topicKeywordsTable         
        pt = self.postTable                   
        ltpt = pt.alias('last_topic_post')
        ontpt = pt.alias('oldest_new_topic_post')

        cols = (tt.c.topic_id, tt.c.site_id, tt.c.group_id,
                tt.c.original_subject, tt.c.num_posts, tt.c.first_post_id,
                ltpt.c.post_id.label('last_post_id'),
                ltpt.c.date.label('last_post_date'),
                ltpt.c.user_id.label('last_author_id'),
                ltpt.c.body.label('last_post_body'),
                sa.func.count(pt.c.post_id)\
                    .append_whereclause(pt.c.topic_id = tt.c.topic_id)\
                    .append_whereclause(pt.c.date >= yesterday)\
                    .label('num_posts_day'),
                ontpt.c.post_id.label('oldest_new_post_id'),
                tkt.c.keywords)

        s = sa.select(cols)

        s.join(tkt, tkt.c.topic_id == tt.c.topic_id)
        s.join(ltpt, ltpt.c.topic_id == tt.c.topic_id)
        s.join(ontpt, optpt.c.topic_id == tt.c.topic_id)

        #  WHERE topic.site_id = 'main'
        #       AND topic.group_id = 'mpls'
        #       AND topic.last_post_date >= timestamp 'now' - interval '1 days'
        #       AND last_topic_post.date = (
        #           SELECT MAX(date)
        #           FROM post
        #           WHERE post.topic_id = topic.topic_id)
        #       AND oldest_new_topic_post.date = (
        #           SELECT MIN(date)
        #           FROM post
        #           WHERE post.topic_id = topic.topic_id
        #               AND post.date >= timestamp 'now' - interval '1 days')

        s.append_whereclause(tt.c.site_id == siteId)
        s.append_whereclause(tt.c.group_id == groupId)
        s.append_whereclause(tt.c.last_post_date >= yesterday)
        s.append_whereclause(ltpt.c.date == sa.func.max(pt.c.date)\
            .append_whereclause(pt.c.topic_id == tt.c.topic_id))
        s.append_whereclause(ontpt.c.date == sa.fun.min(pt.c.date)\
            .append_whereclause(pt.c.topic_id == tt.c.topic_id)\
            .append_whereclause(pt.c.date >= yesterday))
        
        session = getSession()
        r = session.execute(s)
        retval = [{
              'topic_id': x['topic_id'],
              'subject': x['original_subject'],
              'keywords': x['keywords'],
              'first_post_id': x['first_post_id'],
              'last_post_id': x['last_post_id'],
              'last_post_date': x['last_post_date'],
              'last_author_id': x['last_author_id'],
              'last_post_body': x['last_post_body'],
              'oldest_new_post_id': x['oldest_new_post_id'],
              'num_posts': x['num_posts'],
              'num_posts_day': x['num_posts_day'],
              } for x in r]
        return retval

        
