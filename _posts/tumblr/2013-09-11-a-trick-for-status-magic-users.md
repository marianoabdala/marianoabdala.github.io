---
layout: post
title: A trick for Status Magic users
date: '2013-09-11T21:16:00-03:00'
tags: []
tumblr_url: http://mariano.zerously.com/post/60977674124/a-trick-for-status-magic-users
---
Just a few days ago, I was lucky enough as to be part of the beta testing group of the latest version of Status Magic.

Status Magic turned my pity, lame, little screenshots into clean, gorgeous, Apple-class ones. All this in a matter of minutes, with an automatic process that gets it right every time.

The only catch to Status Magic is that for it to work correctly with translucent status bars -and you’ll get a lot of those in iOS 7- you need to remove them from the screenshot yourself. To achieve this the users are provided with a really simple code to insert in their apps.

https://gist.github.com/marianoabdala/6531378

This is great since you can call this from wherever you prefer.What would be the best action to trigger saving a screenshot?
Right, taking a screenshot… by pressing the lock and home buttons.

The UIApplicationUserDidTakeScreenshotNotification was introduced to iOS 7, which allows us to get notified when the user takes a screenshot on the UIApplication.

So that’s how we are going to trigger the provided code, but there’s one extra change I’d like to propose: to allow the user to decide what to do with the image (via UIActivityViewController), instead of forcibly saving it to the disk.

Here’s how I handle it:

https://gist.github.com/marianoabdala/03cb1b27214ce533d573


If you were to choose to “Save Image” you’ll end up with two copies on your Photos app per screenshot, one with the status bar and one without it, which is great since you can easily verify that everything worked fine. You will probably then want to import them all together with Image Capture or iPhoto.

NOTE: This will not work on the simulator, pressing +s will not trigger the notification.
