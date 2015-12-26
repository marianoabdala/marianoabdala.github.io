---
layout: post
title: A note on Matt Gemmell's article on 'API Design'
date: '2012-05-26T14:14:00-03:00'
tags: []
tumblr_url: http://mariano.zerously.com/post/23805163411/a-note-on-matt-gemmells-article-on-api-design
---
I’ll start by saying I really enjoyed Matt’s article on API Design, learnt a lot from it, agreed on most of the principles presented there and, of course, recommend you all to go read it.

Note: I’ll assume you’ve read the article and know about the MGTileMenu, if not you are in time to do it.


I’d like to take a note on a particular line of this sample code I’m not so sure about:

https://gist.github.com/marianoabdala/eb5b04512d32dd02844a

Binary vs. Boolean
There will always be things that look invariably binary. In this case, one could say that a user can either be right or left handed, but that doesn’t make by itself that attribute boolean.

What Matt’s doing here is turning the binary left/right into boolean by asking “Is the user right handed?”1. Which is fine if the intention is to indicate what the default is on the method call itself. But such an intention wasn’t mentioned on the article.

Attribute core
One might also argue that the user left or right-handness is secondary to that attribute. What’s central is knowing which hand will he be using more often. A user could be using his most agile hand to keep the phone steady to take a picture, and use the less agile hand to tap on the app. Even more, that property is about from which direction then hand is coming when tapping whatever makes the menu to be displayed… that’s hardly binary or boolean.

Future proofing
For this version on the component, the hand can come from the left or the right (actually bottom left or bottom right) but in the future that might change for multiple reasons:

A multiplayer game have a player on each side of the device
Changes to the hardware (3D, holographics, both sides of the device being tappable)
Stuff we can’t even imagine
The third I’d say it’s the most important, for that reason, even with attributes that may seem invariably boolean I’d try to use enums.

A different approach
Enums are great because they can grow and include new -unexpected or unsupported originally- options without changing the API.

For this particular case I’d rather have:

https://gist.github.com/marianoabdala/78f38b8685954e603ac9


In this example, regardless of how many new options the future might bring, the API remains unchanged, saving some trouble to adopters.

In short
I’m not discussing this choice in the component context. I just thought the API Design article deserved a note in this regard. The fact that it’s either raining or not raining outside is generally not enough reason to model such condition as a boolean (raining). Instead, I’d suggest using a weatherState enum.



To which there are only two valid answers, yes or no. Even an ambidextrous user is not right-handed. ↩


