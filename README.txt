edem.group.messages.topicsdigest
================================

E-Democracy Customization of GroupServer's Topics Digest

The styling borrows a little bit from 
https://github.com/mailchimp/Email-Blueprints/blob/master/templates/mobile-basicmobile.html. 
Thanks Mail Chimp! 

Mockups
=======

HTML and text mockups can be found in docs/mockups. Unfortunately, the final 
look and markup differs a fair amount from the mockups.

ZMI Files and Properties
========================

The digests **requires** two files to exist in a group's context:

* digest_news.xml
* digest_news.txt

These allow a site administrator to edit the content of the E-Democracy News 
section of the digests.

The digests also makes use of one property in a group's context - 
**digest_news_title** - to set the title for the News section of the digest. 
However, this property is not required, and the egg will use the default name
'E-Democracy News' if this property does not exist.

To be available for all group digests, these files and properties should be
placed in a site folder. While this has not been verified, it should be
possible to overwrite the values of these files and properties for specific
groups.

Digest Pages
===========

The following pages are overridden by this egg:

* Daily Digests

  * gs-group-messages-topicsdigest-daily.html
  * gs-group-messages-topicsdigest-daily.txt

* Reminder Digests

  * gs-group-messages-topicsdigest-weekly.html
  * gs-group-messages-topicsdigest-weekly.txt

In the case of html pages, the templates (dailyTopicsDigest-* and 
weeklyTopicsDigest-*) are where the embedded CSS for the digest is defined, 
including the responsive design CSS. Aside from this, not much else of interest
happens in the digest page templates.

Digest Viewlets
==============

The Daily HTML digest use 5 viewlets:

* A **header** viewlet that displays the group name, membership size, and 
  social media links
* A **list** viewlet that displays the list of active topics
* A **news** viewlet that displays organizational news from E-Democracy
* A **clips** viewlet that displays clips from active topics
* A **footer** viewlet that displays standard help/footer text

The Reminder HTML Digest uses a similar set of viewlets, but does not use a clips viewlet.

Reminder Digests Differences
============================

The Weekly Digest of gs.group.messages.topicsdigest has been renamed slightly
to be the Reminder Digest. While the reminder digest is still accessed via
gs-group-messages-topicsdigest-weekly.html/txt, all associated templates,
classes, viewlets, and viewlet managers use the term Reminder instead of
Weekly.

In addition, the Reminder Digest goes out 30 days after the last post to a
group instead of 7 days.

Finally, while the Reminder digest is based on E-Democracy';s Daily Digest ,
it does not include the clips section.

Text Digest Differences
=======================

This egg mostly reuses the text digests that are defined by 
gs.group.messages.topicsdigest. The one significant difference is that a News
viewlet is inserted by this egg.
