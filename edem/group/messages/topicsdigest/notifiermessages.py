# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from gs.content.base import SitePage
from gs.group.messages.topic.digest.daily.notifiermessages import (
    DailyMessage as GSDailyMessage)
from gs.group.messages.topic.digest.weekly.notifiermessages import (
    WeeklyMessage as GSWeeklyMessage)


class DailyMessage(GSDailyMessage):
    def __call__(self, *args, **kw):
        '''Over-ride the call, so we do not freak out premailer'''
        retval = super(SitePage, self).__call__(*args, **kw)
        return retval


class WeeklyMessage(GSWeeklyMessage):
    def __call__(self, *args, **kw):
        retval = super(SitePage, self).__call__(*args, **kw)
        return retval
