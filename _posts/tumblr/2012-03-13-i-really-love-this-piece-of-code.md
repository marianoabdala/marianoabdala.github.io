---
layout: post
title: I really love this piece of code
date: '2012-03-13T08:53:00-03:00'
tags: []
tumblr_url: http://mariano.zerously.com/post/19232426114/i-really-love-this-piece-of-code
---
It belongs to a class that wraps an ACAccount from the Accounts.framework.

What it does is fetch the profile image for the account. Since the location for that image is not present on the ACAccount it first needs to fetch the location of the image and once that’s received fetch the image itself.

Blocks was the stylish way to achieve this and I’m happy I spent an extra two minutes to polish it. 1

https://gist.github.com/marianoabdala/ec9c75067db9a7f08a65



Is there any piece of code you wrote today that made you proud?



Originally, fetchProfileImageInfo would start a TWRequest to get the information for the account and, on it’s completion handler, it would parse that info and call fetchProfileImage. ↩


