---
layout: post
title:  "viewWithTag:"
date:   2016-07-20 21:03:42 -0300
---

There's been lots of debate on whether you should use a `UIView`'s `tag` or not. The truth is you don't always have the chance to decice and you've got to use it.

One good example of not being able to make a choice would be when using an extension, specially a protocol extension. Extensions can't hold stored properties, so you can't really have a reference to the view like this:

```swift
protocol LoadingViewController {
    
    var isLoading: Bool { get set }
}

extension LoadingViewController where Self: UIViewController {
    
    let activityIndicatorView: UIActivityIndicatorView
}
```

In such cases you may want to build and refer to your view hierarchy by using tags.

It's unfortunate that in `UIView`'s `tag` property is an `Int`, because numbers are so easy to be repeated and so unexpresive. Say you tag a view `10`, does that say _anything_ about the view? What if someone else already used `10` for another subview of that view?

Wouldn't it be better to be able to tag that with a `String`?

That's when this extension may come in handy:

```swift
extension UIView {
    
    func view(with key: String) -> UIView? {
        
        return self.viewWithTag(key.hashValue)
    }
    
    func setKey(_ key: String?) {
        
        self.tag = key?.hashValue ?? 0 // Default for view.tag.
    }
}
```

It introduces the concept of `key` which is a `String` and it's actually just a wrapper for the tag, so you get the exact same behavoir.

Now you can go from something like this:

```swift
let childViewKey = 12345

let parentView = UIView()
let childView = UIView()

childView.tag = childViewKey
parentView.addSubview(childView)

let viewWithKey = parentView.viewWithTag(childViewKey)
```

to something like:

```swift
let childViewKey = "com.myApp.notificationsPane.optionSwitch"

let parentView = UIView()
let childView = UIView()

childView.setKey(childViewKey)
parentView.addSubview(childView)

let viewWithKey = parentView.view(with: childViewKey)
```