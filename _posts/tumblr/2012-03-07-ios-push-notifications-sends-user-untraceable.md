---
layout: post
title: iOS push notifications sends user-untraceable sounds
date: '2012-03-07T14:46:00-03:00'
tags: []
tumblr_url: http://mariano.zerously.com/post/18906826372/ios-push-notifications-sends-user-untraceable
---
While iOS push notifications are awesome in many ways, one of their most important features is that they can be selectively disabled. If one app sends too many push notifications, you can simply turn off push notifications for that app (or delete it outright).

But what if you coulnd’t? And by that I mean, what if you simply didn’t know which application sent the notification? Then you’d lose that ability, that power.

To date, it is possible for apps to send push notifications that will play a sound on the user’s device without the user knowing who sent it.

What’s the structure of a push notification?

A push notification occurs when a server sends some data to Apple Push Notification Service (APNS), who is in charge of forwarding that data to the indicated device. Here’s an example of how that data could look like: 1

https://gist.github.com/marianoabdala/d5fccef1b17213afbbb3

Now, on the alert, 2


  If you specify a string, it becomes the message text of an alert with two buttons: Close and View.


…and of course the sender app’s name. If you don’t specify a string and the app is opened, the app could get some interesting metadata the server is sending, for instance, that the person on the other side of the chat is typing. If you don’t specify a string and the app is closed, nothing happens… unless the badge or the sound were specified.

If the badge is specified, the push notification will update the number on the top right corner of the sender’s app. If the sound is specified (and included in the sender’s app), a sound will play on the device.

A silent badge update makes sense, but what about a sound with no alert or badge update? I wonder if this is intentional or just a bug.

I’m a developer, is there an easy way to reproduce this?

Yes, if your app has any sound and you are already sending push notifications, just fetch your own device push id and send a push notification with a blank alert and the name of a bundled sound file.

It doesn’t sound that bad to me…

Well, if one of your apps decided to start triggering sounds in the middle of the night and you couldn’t identify it to delete it or report it, it would.

How bad can it get if exploited?
Scary sounds in the night.
Fart sounds at noon.
<paranoid>Submilinal messages asking you to buy the pro version of an app.</paranoid>
Sound ads all day long.

One last thing

When this kind of notification is received the sound starts playing and the screen doesn’t turn on, so you might not even know it’s your phone making the noise.



According to the Local and Push Notification Programming Guide, example 3. ↩



According to Table 3-1 in Local and Push Notification Programming Guide. ↩


