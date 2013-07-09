# -*- coding: utf-8 -*-
from gs.group.messages.topicsdigest.message import Message as Base


class Message(Base):

    def add_headers(self, container, subject):
        # A NOTE TO THE FUTURE:
        # Do not set a Reply-To header. Bounces need to go back to the group,
        # so that GroupServer can track bounces and adjust delivery as
        # neccessary. 
        container = super(Message, self).add_headers(container, subject)
        return container
