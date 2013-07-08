# coding=utf-8
from zope.component import createObject
from gs.viewlet.manager import WeightOrderedViewletManager
from topicsDigest import DailyTopicsDigest


class DailyTopicsDigestViewletManager(WeightOrderedViewletManager):
    """Provides the TopicsDigest for viewlets in the Daily TopicsDigest"""

    def __init__(self, context, request, view):
        super(WeightOrderedViewletManager, self).__init__(
            context, request, view)
        self.siteInfo = createObject('groupserver.SiteInfo', self.context)
        self.__topicsDigest__ = DailyTopicsDigest(self.context, self.siteInfo)

    @property
    def topicsDigest(self):
        """Provides the list of topic models in the current digest."""
        assert hasattr(self, '__topicsDigest__')
        retval = self.__topicsDigest__
        assert isinstance(retval, DailyTopicsDigest)
        return retval
