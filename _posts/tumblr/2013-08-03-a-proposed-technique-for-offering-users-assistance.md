---
layout: post
title: A proposed technique for offering users assistance in the event of a crash
date: '2013-08-03T10:49:00-03:00'
tags: []
tumblr_url: http://mariano.zerously.com/post/57244969720/a-proposed-technique-for-offering-users-assistance
---
All apps crash.
We all know that and we all know that all we can do about it is try to collect information as to why the crash happened and prevent it from happening again.

But we are not our users -we should all also know that-, and sometimes, in the event of a crash, our users don’t understand what happened or why. Let alone, are they aware of the kind of care we placed into making the app as stable as possible. Sometimes they get confused or even, really upset.

What are we exactly doing right now to help our users in the event of a crash? What’s stopping a user from going straight into the AppStore to trash our app? Well, nothing. What can we do?

What we can do is give the user quick access, using local push notifications, to information about what have just happened and means to contact us for help.

Here’s a video of how this could look like on your app.




The technique is really simple,
1. Schedule a local push notification
2. Cancel it right before it’s due
3. Repeat.

If the app crashes, the notification will not be cancelled and thus will be presented to the user. This whole mechanism happens locally, there’s no need for a remote notifications service.

Here’s the full project on Github.

As a side effect, you’ll get your bug reporter to collect more info on your crashes. Remember that most crash reporters can report bugs only if the app is re-opened after a crash occurred.
