# coding=utf-8
import sqlalchemy as sa
from gs.group.messages.topicsdigest.queries import DigestQuery as BaseDigestQuery
from gs.database import getSession

from logging import getLogger
log = getLogger('edem.group.messages.topicsdigest.DigestQuery')

class DigestQuery(BaseDigestQuery):
    
    def __init__(self):
        super(DigestQuery, self).__init__()

    def topics_sinse_yesterday(self, siteId, groupId):
        retval = super(DigestQuery, self).topics_sinse_yesterday(siteId, groupId)

        pt = self.postTable
        s = sa.select((pt.c.post_id, pt.c.body))
        s.append_whereclause(pt.c.post_id.in_([x['last_post_id'] for x in retval]) )

        session = getSession()
        r = session.execute(s)

        post_bodies = dict(r.fetchall())

        for row in retval:
            row['last_post_body'] = post_bodies[row['last_post_id']]

        return retval
        
