---
layout: post
title:  "Introduction to FRP (part 1)"
date:   2016-03-20 11:33:20 -0300
---

Not long ago, I started working on a project that is built around _Functional Reactive Programming_. Even with a strong programming background I found it hard at first to even grasp its most fundamental concepts. To make things worst, just as I was starting, [ReactiveCocoa](https://github.com/ReactiveCocoa/ReactiveCocoa) 4 -the FRP framework of choice for said project- was launched with **major** changes, making it really hard to find good reference material. The ones I found were mostly about making a transition from `2.5` to `4.0`.

Here goes some key lessons I learnt the hard way, in the hope that someone in a similar situation as me will find it useful or someone who knows more will correct me if I'm wrong in my understanding of FRP under ReactiveCocoa.

## FRP
Funcional Reactive Programming is a programming paradigm like many others. The main result of its adoption is more readable code via the sustitution of state by higher level instructions.

The most common example for state is a register button that will be enabled when both the username and the password are valid, as long as the register button hasn't been pressed already and we are registering the user via API.

What imperative programming will normally do is:  
1. Hook into the textfields' `shouldChangeCharactersInRange:replacementString:` delegate method.  
2. Every time the text changes, check whether it's valid or not.  
3. Check if the counterpart textfield's text is valid.  
4. Check the `isRegistering` property is `false`.  
5. Enable the register button.  
6. Hook into the register button `UIControlEventTouchUpInside` event.  
7. When the register button is tapped collect the username and password values, call the register API and set the `isRegistering` property to `true`.

Now, this is what FRP programming will normally do:  
1. Bind the register button's enabled property to _when both the username and the password are valid, as long as the register button hasn't been pressed already and we aren't registering the user via API_.  

It sounds like I'm just repeating myself but that's exactly what FRP lets you do, define each component's behaviour in a very similar way to which you think about behaviour.

A different way to think about this is a spreadsheet. All a spreadsheet needs from the user is that each cell has either values or formulas. If a cell's formula is `=A1+(AVG(B1:B10))` you don't care about how or when you get the result. You can focus on _the formula_.

This has two main benefits:  
1. You write code in the same way as you think of it, as previously mentioned.  
2. Once the code is written, the behaviour is contained and complete in a few lines of code. Could be more -much more-, but it'll be all at one place.

Let's go over the components in FRP that will enable us to do such a thing.

# Stream
A _cell_ in FRP is called a "Stream".

You can think of a stream as the history, past, present and future of a property in the sense that they are self contained and inmutable in time; like a river with all it's water, but you are seeing just one part of it.

What triggers the river to move? Events.

Those events are mostly changes, like temperature was 21º and now it's 25º but could also be something like finishing serving a customer and wanting the next to come to the counter.

_NOTE: Streams are often called or represented by Signals, which is a terrible name since they get easily confused with events. You could think of a signal as a semaphore's light changing[^1] from green to red, but in FRP a signal is the semaphore itself._

# Bindings
What's the use of a stream if we can't bind it somewhere?

What can we bind to a stream? Almost any property, and you know what's cool? FRP Properties have streams themselves. So you can bind a stream into a property and another property to the first property's stream.

# Tranformations
A big component of FRP is transformations, they are the _formula_ in our cell.

We may have a stream of `string`s but need to bind them to a `bool` property, for instance, enabling a button if a property's text is larger than 4 chars.

Transformations transform streams into streams, not into values.

# Chaining
This is the _Functional_ part in Functional Reactive Programming. And it's available all accorss frameworks that you can chain as many streams, streams transformations and streams combinations (which is a kind of transformation) as you want.

If you are comfortable with Functional Programming there's not much more explanation needed.

# Hot and Cold signals
This is a fairly important difference, ignoring it could trigger lots of issues.

You'll find many _fancy_ and more correct definitions than this one, but the key part is what happens when you bind a stream to a property:  
If you get the current value (which was set in the past) alongside with whichever new values are set in the future binded into your property then you are using a **cold signal**.  
If you only start getting the new values (whichever are set in the future) binded into your property then you are using a **hot signal**.

This also applies to _events_. A cold signal could be a bank queue that opens up and right away gets a new customer, if any. Whereas a hot signal could be a catastrophe prevention system, you only want to start the siren when the next warning comes in, regardless of whether there was one in the past.

# Next
[Part 2]({% post_url 2016-03-24-introduction-to-frp-pt2 %}): How to implement these concepts in ReactiveCocoa 4.

[^1]: New Oxford American Dictionary: **signal** \|ˈsiɡnəl\| (noun) • an event or statement that provides the impulse or occasion for something specified to happen: the champion's announcement that he was retiring was the signal for scores of journalists to gather at his last match.




