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
        tt = self.topicTable            
        tkt = self.topicKeywordsTable         
        pt = self.postTable                   
        yesterday = datetime.datetime.now() - datetime.timedelta(day=1)
                                              
        #SELECT topic.topic_id, topic.original_subject, topic.last_post_id
        #  topic.last_post_date, topic.num_posts,
        cols = (tt.c.topic_id, tt.c.site_id, tt.c.group_id,
                tt.c.original_subject, tt.c.first_post_id,
                tt.c.last_post_id, tt.c.num_posts, tt.c.last_post_date,
                tkt.c.keywords,
        #  (SELECT COUNT(*)
        #    FROM post
        #    WHERE (post.topic_id = topic.topic_id)
        #      AND post.date >= timestamp 'yesterday')
        #  AS num_posts_day
                sa.select([sa.func.count(pt.c.post_id)],
                          sa.and_(pt.c.date >= yesterday,
                          pt.c.topic_id == tt.c.topic_id)
                          ).as_scalar().label('num_posts_day'),
        #  (SELECT post.user_id
        #    FROM post
        #    WHERE post.post_id = topic.last_post_id)
        #  AS last_author_id
                sa.select([pt.c.user_id],
                          pt.c.post_id == tt.c.last_post_id
                          ).as_scalar().label('last_author_id'),
        #  (SELECT post.body
        #    FROM post
        #    WHERE post.post_id = topic.last_post_id)
        #  AS last_post_body
                sa.select([pt.c.body],
                          pt.c.post_id == tt.c.last_post_id
                          ).as_scalar().label('last_post_body'))

        s = sa.select(cols, order_by=sa.desc(tt.c.last_post_date))
        #  FROM topic
        #  WHERE topic.site_id = 'main'
        #    AND topic.group_id = 'mpls'
        s.append_whereclause(tt.c.site_id == siteId)
        s.append_whereclause(tt.c.group_id == groupId)
        #    AND topic.last_post_date >= timestamp 'yesterday'
        s.append_whereclause(tt.c.last_post_date >= yesterday)
        s.append_whereclause(tt.c.topic_id == tkt.c.topic_id)

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
                  'num_posts': x['num_posts'],
                  'num_posts_day': x['num_posts_day'],
                  } for x in r]
        return retval
