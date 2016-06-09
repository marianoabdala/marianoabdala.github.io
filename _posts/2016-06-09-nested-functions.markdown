---
layout: post
title:  "Nested Functions"
date:   2016-06-09 16:18:06 -0300
---

I came across a neat Swift feature today that I wasn't aware of: you can nest functions.

Nesting functions work great for typically large functions that you want to split into smaller chunks but that make no sense if called from anywhere else, not even from `self`.

A good example of this kind of functions would be one that serves to configure some views in a view controller. In a very common scenario, each of said views would required some 4 or 5 lines of code.

#### The comment approach
One aproach is to have comments signaling the beginning of each section, like this:

```
// Username label
self.usernameLabel.accessibilityHint = "User name"
self.usernameLabel.shadowColor = UIColor.cyanColor()
self.usernameLabel.textAlignment = .Justified

// Next button
self.nextButton.layer.cornerRadius = 4
...
```

But you may end up with a hundred lines long method. **Nobody wants that.**

#### The private function approach
A different approach (the one I used up until now) was to wrap those little sections into functions and call them one at a time, so that my function would like somewhat like this:

```
private func configureViews() {
    
  self.configureAvatarImageView()
  self.configureUsernameLabel()
  self.configureNextButton()
}

private func configureAvatarImageView() {

  ...
}
```

The downside with this approach is that we could call `configureAvatarImageView` from any other part of our view controller, when, in most cases, it doesn't make any sense. Given that having it accessible means polluting our auto-completion and allowing us to mistakingly call it from somewhere we aren't supposed to... **Nobody wants that.**

#### The nested function approach

Nested functions allows us to define functions inside other functions. Those inner functions are only accessible from whithin the outer function. Making our code much more organised and tidy. Inner functions also have access to variables defined in the outer function.

Let's see how our `configureViews` would look like using nested functions:

```
private func configureViews() {
	
  func configureAvatarImageView() {

    ...
  }

  func configureUsernameLabel() {

    ...
  }

  configureNextButton() {
  
    ...
  }

  configureAvatarImageView()
  configureUsernameLabel()
  configureNextButton()
}
```

This is how you'd probably want to do it. Simple, tidy and thanks to nested functions **contained**.

  Note: Ideally, you'd be able to call the inner functions on top of the function, to serve as a sort of summary, but today that's not available. For that matter, I created a [bug report](https://bugs.swift.org/browse/SR-1721).
