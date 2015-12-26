---
layout: post
title: Playing with the UIScrollView, a concept for how many rows remain undisplayed
date: '2012-03-06T19:46:00-03:00'
tags: []
tumblr_url: http://mariano.zerously.com/post/18866876304/playing-with-the-uiscrollview-a-concept-for-how
---
One of the projects I’m working on display a list of items, each in full screen. To achieve that I used a UITableView with rows as high as the screen and paging enabled.

On a regular table with many rows per screen and paging disabled the scroll indicator is enough for the user to know with a good degree of accuracy where they are on the table. In this app’s case, knowing the exact remaining items would be really useful.

Here are a couple example of how this looks like in retina:



This is easy to achieve and customize, all the code you’ll needed is:


  Warning: The scroll indicator view isn’t part of the iOS’s documented API, so don’t try this with apps that aim for the AppStore!


https://gist.github.com/marianoabdala/cc75c39153af4990edf2


You can test this by downloading Apple’s TableViewSuite and adding it at the end of the RootViewController.m file from the SimpleTableView project.

Note: In the SimpleTableView project, timeZoneNames is an array of strings with all time zone names. You should replace the timeZoneNames.count with the total number of rows in your datasource.
