edem.group.messages.topicsdigest
================================

E-Democracy Customization of GroupServer's Topics Digest

The styling borrows a little bit from https://github.com/mailchimp/Email-Blueprints/blob/master/templates/mobile-basicmobile.html. 
Thanks Mail Chimp! 

Mockups
=======

HTML and text mockups can be found in docs/mockups. Unfortunately, the final look and markup differs a fair amount from the mockups.

Digest Pages
===========

The following pages are overridden by this egg:

* Daily Digests

  * gs-group-messages-topicsdigest-daily.html
  * gs-group-messages-topicsdigest-daily.txt

* Reminder Digests

  * gs-group-messages-topicsdigest-weekly.html
  * gs-group-messages-topicsdigest-weekly.txt

In the case of html pages, the templates (dailyTopicsDigest-* and weeklyTopicsDigest-*) 
are where the CSS for the digest is defined. Aside from this, not much else of 
interest happens in the digest page templates.

Digest Viewlets
==============

The HTML digests use 5 viewlets:

* A 'header' viewlet that displays the group name, membership size, and social media links
* A 'list' viewlet that displays the list of topics
* A 'news' viewlet that displays organizational news from E-Democracy
* A 'clips' viewlet that displays clips from topics
* A 'footer' viewlet that displays standard help/footer text
