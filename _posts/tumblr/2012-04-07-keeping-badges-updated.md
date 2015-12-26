---
layout: post
title: Keeping badges updated
date: '2012-04-07T17:46:00-03:00'
tags: []
tumblr_url: http://mariano.zerously.com/post/20670689934/keeping-badges-updated
---
Users pay a lot of attention to badges. They were designed to drive attention toward them, and they do.

A badge that’s out of date hurts usability and your reputation. Good citizens keep their app’s badges updated. Most apps make a good job in this regard when a new message or invitation is received or a new task is created or assigned; but for some reason most app’s don’t update the badge when a message is read, an invitation is accepted or a task is completed.1

If you’ve just realized that your app is not updating badges in these cases, there’s really no reason to resign or be ashamed… Big apps like Twitter and Facebook still don’t update their badges when a message is read either.

Want to give it a try?

Ask a friend to send you a private message on Facebook or a direct message on Twitter
Wait until you receive a push notification on your device
Without opening the notification or the app, check the app’s badge, it should be updated
Mark that message as read on the web, another device or in any way but not with the device you are trying to reproduce this misbehavior
Sit
Make sure you aren’t holding your breath
Wait.
Spoiler: The badge will not really update, no matter how long you wait.

Want to fix this on your app?

It’s easy, just send a silent push notification to each of your user’s devices with the updated badge:

https://gist.github.com/marianoabdala/c3fb6d46143a43663fc4



Since there’s no message or sound specified the user will not be notified, but his badge will be cleared (if 0) or updated to whatever necessary number.



At least remotely. Most will work correctly when the message is read, the invitation accepted or the task completed locally. ↩


