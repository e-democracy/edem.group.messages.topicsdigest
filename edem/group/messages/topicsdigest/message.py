# -*- coding: utf-8 -*-
from gs.group.messages.topicsdigest.message import Message as Base


class Message(Base):

    def add_headers(self, container, subject):
        container = super(Message, self).add_headers(container, subject)
        container['Reply-To'] = self.h('noreply@e-democracy.org')
        return container
