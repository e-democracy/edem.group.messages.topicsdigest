edem.group.messages.topicsdigest
================================

E-Democracy Customization of GroupServer's Topics Digest

The styling borrows a little bit from https://github.com/mailchimp/Email-Blueprints/blob/master/templates/mobile-basicmobile.html. 
Thanks Mail Chimp! 

Workflow
========

When making changes to the style or layout of digests, the following workflow is encouraged:

1. Change the appropriate mockup in docus/mockups
2. View the changed mockup in your browser
3. git commit your changes
4. Use http://premailer.dialect.ca/ to test your changes using inlined CSS
5. Using the results of Premailer, make changes to the appropriate templates/classes
6. git commit and deploy your changes

Mockups
=======

HTML and text mockups can be found in docs/mockups.

Digest Pages
===========

The following pages are overridden by this egg:

* Daily Digests

  * gs-group-messages-topicsdigest-daily.html

In the case of html pages, the templates (dailyTopicsDigest-* and weeklyTopicsDigest-*) 
are where the CSS for the digest is defined. Aside from this, not much else of 
interest happens in the digest page templates.
