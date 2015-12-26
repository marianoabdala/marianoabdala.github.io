---
layout: post
title: Push notifications and mail composing
date: '2012-04-21T20:38:00-03:00'
tags: []
tumblr_url: http://mariano.zerously.com/post/21532205835/push-notifications-and-mail-composing
---
Continuing with a series of posts around push notifications1, I present into this dilemma:

Sometimes you want to give the user the ability to compose an mail from inside your app with the MFMailComposeViewController and sometimes a notification arrives or is due when he is.

If the user chooses to view the notification you’ll need to, among other things, dismiss the view controller, usually with:

https://gist.github.com/marianoabdala/a00f3f7cecb3afc49d37

The result to that action is that the view controller is dismissed silently and the message is lost, it won’t appear on the user’s drafts.

A solution

A way of preventing unexpected deletions would be to notify the user about this behavior in the very push notification alert view. But users rarely read the detailed text on alert views. See how little attention such a warning would drive in this case:



A better solution

Keep the alert view simple, just ditch that hard to understand and little visible text and have the app show the user a UIActionSheet with a big red button, but only if he decides to view the notification’s detail.

This is how it’d look like (very similar to what the user gets when canceling the composition of an email):



Here’s some sample code on github to show this in a simple app.



iOS push notifications sends user-untraceable sounds and Keeping badges updated. ↩


