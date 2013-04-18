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
    	#	    last_topic_post.date as last_post_date,  
    	#	    last_topic_post.user_id as last_author_id, 
    	#	    last_topic_post.body as last_post_body, 
    	#	    COUNT(all_new_topic_posts.*) as num_posts_day,
    	#	    oldest_new_topic_post.post_id as oldest_new_post_id,
        #       topic_keywords_table.keywords
    	#   FROM topic, post as last_topic_post, 
    	#    	post as all_new_topic_posts, 
    	#   	post as oldest_new_topic_post

        tt = self.topicTable            
        tkt = self.topicKeywordsTable         
        pt = self.postTable                   
        ltpt = pt.alias('last_topic_post')
        antpt = pt.alias('all_new_topic_posts')
        ontpt = pt.alias('oldest_new_topic_post')

        cols = (tt.c.topic_id, tt.c.site_id, tt.c.group_id,
                tt.c.original_subject, tt.c.num_posts, tt.c.first_post_id,
                ltpt.c.post_id.label('last_post_id'),
                ltpt.c.date.label('last_post_date'),
                ltpt.c.user_id.label('last_author_id'),
                ltpt.c.body.label('last_post_body'),
                sa.func.count(antpt.c.post_id).label('num_posts_day'),
                ontpt.c.post_id.label('oldest_new_post_id'),
                tkt.c.keywords)

        s = sa.select(cols)

        #   WHERE topic.site_id = 'initial_site'
        #    	AND topic.group_id = 'example_group'
        #    	AND topic.last_post_date >= timestamp 'yesterday'
        s.append_whereclause(tt.c.site_id == siteId)
        s.append_whereclause(tt.c.group_id == groupId)
        s.append_whereclause(tt.c.last_post_date >= yesterday)
	    
        #	    AND last_topic_post.date in (SELECT MAX(date)
	    #					FROM post
	    #					WHERE post.topic_id = topic.topic_id
	    #					GROUP BY topic.topic_id)
        s.append_whereclause(ltpt.c.date.in_(sa.select(
                            sa.func.max(pt.c.date)\
                        .where(pt.c.topic_id == tt.c.topic_id)\
                        .group_by(tt.c.topic_id)
                        )))

        #     	AND all_new_topic_posts.topic_id = topic.topic_id
	    #   	AND all_new_topic_posts.date >= timestamp 'yesterday'
	    #   	AND oldest_new_topic_post.topic_id = topic.topic_id
        s.append_whereclause(antp.c.topic_id == tt.c.topic_id)
        s.append_whereclause(antp.c.date >= yesterday)
        s.append_whereclause(ontp.c.topic_id == tt.c.topic_id)

	    #   	AND oldest_new_topic_post.date in ( SELECT MIN(date)
	    #						FROM post
	    #						WHERE post.topic_id = topic.topic_id
	    #							AND post.date >= 'yesterday'
	    #						GROUP BY topic.topic_id)
        s.append_whereclause(ontpt.c.date.in_(sa.select(
                            sa.func.min(pt.c.date)\
                        .where(pt.c.topic_id == tt.c.topic_id)\
                        .group_by(tt.c.topic_id)
                        )))

        #       AND topic.topic_id = topic_keyword_table.topic_id
        s.append_whereclause(tt.c.topic_id == tkt.c.topic_id)

	    #    GROUP BY topic.topic_id, last_topic_post.user_id,
        #       last_topic_post.body, last_topic_post.post_id, 
        #       oldest_new_topic_post.post_id
        s.group_by((tt.c.topic_id, ltpt.c.user_id, ltpt.c.body, ltpt.c.post_id,
                    ontpt.c.post_id))

        #DEBUG
        log.info('The daily html query: %s' % str(s))

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
