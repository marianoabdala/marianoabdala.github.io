---
layout: post
title:  "Dynamic Autolayout + ReactiveCocoa"
date:   2016-08-20 14:43:15 -0300
---

This may not be entirely true, but it feels that way:

> Everything looks better with ReactiveCocoa.

I always try to strip my posts from added complexity. In my [previous post]({% post_url 2016-08-15-dynamic-autolayout %}), I showed an alternative to working with dynamic autolayout without having complex calculations. I didn't thought it was relevant to introduce [ReactiveCocoa or FRP]({% post_url 2016-03-20-introduction-to-frp-pt1 %}) in that mix.

But, as I said before, everything looks better with ReactiveCocoa.

I created a [new branch](https://github.com/marianoabdala/Constraints/tree/RAC) on the [original project](https://github.com/marianoabdala/Constraints) that you can browse, but here's the gist of it, we bind each constraint's priority to the selected position:

```swift
let priorityMap: (Position, Position) -> (UILayoutPriority) = {
  $0 == $1 ? UILayoutPriorityDefaultHigh : UILayoutPriorityDefaultLow
}

self.leftPositionConstraint.rac_priority <~
  self.position.producer.map { priorityMap($0, .Left) }

self.centerPositionConstraint.rac_priority <~
  self.position.producer.map { priorityMap($0, .Center) }

self.rightPositionConstraint.rac_priority <~
  self.position.producer.map { priorityMap($0, .Right) }

self.positionLabel.rac_text <~
  self.position.producer.map { $0.rawValue }

self.position.signal.observeNext { [weak self] _
  
  self?.view.layoutIfNeeded()

  // Animate.
}
```

All your layout code turned into just four lines. **Much better.**