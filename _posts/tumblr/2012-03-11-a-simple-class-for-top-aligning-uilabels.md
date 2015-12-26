---
layout: post
title: A simple class for top-aligning UILabels
date: '2012-03-11T16:31:00-03:00'
tags: []
tumblr_url: http://mariano.zerously.com/post/19133640748/a-simple-class-for-top-aligning-uilabels
---
As you well may know, the iOS UILabel doesn’t have a vertical alignment property. As I needed that feature more and more on some of the apps I worked on, I created the ZYTopAlignedLabel.

It’s easy to use and it showed to be such a time saver on my projects… and it’s so simple!

When the UILabel is init’d or awake’dFromNib I store its original frame. Later, every time the text is changed, I trim it and update it to be left and top aligned.

https://gist.github.com/marianoabdala/d84dae3ca6a68954befa


Here are the full files:


Note: In the ZYTopAlignedLabel.m file you may notice that I use #pragma marks to achieve the following structure.

https://gist.github.com/marianoabdala/c868a32fa8399581e220

As you can see I have 3 main structures, Hierarchy with whatever methods are overridden from super classes, Self with the actual class’ public and private methods and Protocols with all methods for each adopted protocol.
