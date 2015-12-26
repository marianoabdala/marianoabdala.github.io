---
layout: post
title: A better UIActivity API
date: '2012-12-04T09:54:00-03:00'
tags: []
tumblr_url: http://mariano.zerously.com/post/37184158920/a-better-uiactivity-api
---
I’m going to be giving a talk soon on how to use and extend UIActivity and I found hard to explain a few of the API decisions made there.

Just as a note, on the regular UIActivity API the programmer has to override the following methods:

https://gist.github.com/marianoabdala/bb876e553bda79330020


Plus one and just one of the following methods:

https://gist.github.com/marianoabdala/d44ebc656472df9be3fb


As I was trying to round up the talk I kept having the feeling that no matter how hard I tried, a few question were still unanswered…

Why having an activityType?

The single purpose of having an activityType is to be able to exclude it from the UIActivityViewController with the excludedActivityTypes. I can’t think of a scenario where I’d want to exclude an activity where I can’t simply not add it to the applicationActivities on UIActivityViewController initialization.
Why having a separated prepeareWithActivityItems?

At first, I thought this would happen on a different time than the actual execution of the activity, so I thought that maybe it was done in this way just for performance’s sake. But no, both prepeareWithActivityItems and the execute method are called practically immediately one after the other.
Why would the programmer have to choose between performActivity and activityViewController?

Specially, why have to choose on implementation time instead of in runtime?

We should be able to decide on runtime. And even if we can decide on implementation time, why having two separate methods, when the programmer could simply be returning nil to the activityViewController if he’d wanted a silent activity?
So what did I do?

At first, I tried using humor on my talk. But still I felt like I was missing something, so I challenged myself into making a better API, one that could be more easily extended and explained to others.

I ended up with a pretty decent API where the programmer only have to override what’s necessary, and in a way, it just that makes more sense.

With ZYActivity all the programmer needs to override is:

https://gist.github.com/marianoabdala/4e3b8b48a767801672de

How did I accomplish that?

I made the activityType return bundle id plus class name.
I overrided the prepeareWithActivityItems: so that the activity items are always copied into the activity itself and are ready to use on execution.
I created a method called performWithActivityItems: that the programmer must override and depending on if he returns an UIViewController or nil, it will display it or just execute. 
The end result is that the user only has to worry about overriding 4 instead of 7 methods and that he can decide on runtime if he wants to do some background work or present the user with an interface to ask for more info or simply display progress.

Full implementation and sample project on GitHub.
UPDATE: I filed a rdar to make sure Apple sees it. Feel free to duplicate it.
http://openradar.appspot.com/radar?id=2419401
