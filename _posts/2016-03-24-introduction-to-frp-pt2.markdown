---
layout: post
title:  "Introduction to FRP (part 2)"
date:   2016-03-24 21:26:45 -0300
---

This is the second part of the Introduction to FRP series. Here's the [first]({% post_url 2016-03-20-introduction-to-frp-pt1 %}) part.

As mentioned on the first part of this series, we are going to focus on ReactiveCocoa 4 for showing examples on how to implement FRP concepts. I'll assume you already installed it on your project. If you haven't you may want to read [this](https://github.com/ReactiveCocoa/ReactiveCocoa#getting-started).

Let's use the example of the register button that will be enabled when both the username and the password are valid, as long as the register button hasn’t been pressed already and we are registering the user via API.

If you recall, this is what we've said:

> Now, this is what FRP programming will normally do:  
1. **Bind** the register button’s enabled property to when both the username and the password are valid, as long as the register button hasn’t been pressed already and we aren’t registering the user via API.

So let start with the bind.

# Bindings

ReactiveCocoa has a really cool, smart and practical way of binding things via the use of the `<~` operator. Let's see an example.

Let's assume we have a `UserViewModel` that looks more less like this:

    class UserViewModel {
    
    	var name = MutableProperty<String?>(nil)
	}

Then, this test would pass without issues:

	class ReactiveTests: XCTestCase {
	    
	    func testSimpleBind() {
	        
	        let newName = "Mariano Abdala"
	        let userViewModel = UserViewModel()
	        let nameBindedProperty = MutableProperty<String?>(nil)
	        
	        nameBindedProperty <~ userViewModel.name

	        userViewModel.name.value = newName

	        XCTAssertEqual(userViewModel.name.value, newName)
	        XCTAssertEqual(nameBindedProperty.value, newName)
	    }
	}

We will, of course, want to bind a `ViewModel` to a `UIView`'s property. In this case, the user's name would probably end up being bounded to a `userNameLabel`'s `text`.

In the past you'd do something like[^1]:

	RAC(self.userNameLabel, text) = userViewModel.name;

But that won't work in RAC 4. In RAC 4 you can only bind, using the `<~` operator, to a `MutableProperty<T>`. But worry not, because [Colin Eberhardt](http://blog.scottlogic.com/ceberhardt/) came up with an [easy way](https://github.com/ColinEberhardt/ReactiveTwitterSearch/blob/master/ReactiveTwitterSearch/Util/UIKitExtensions.swift) to turn almost any property (including `UIKit`'s) into a RAC 4 `MutableProperty<T>`. You'll most likely want to add that file[^2] to any project that uses RAC 4.

Let's see how this looks like with a `UILabel`:

	class ReactiveTests: XCTestCase {
	    
	    func testLabelBind() {
	        
	        let newName = "Mariano Abdala"
	        let userViewModel = UserViewModel()
	        let userNameLabel = UILabel()
	        
	        userNameLabel.rac_text <~ userViewModel.name

	        userViewModel.name.value = newName

	        XCTAssertEqual(userViewModel.name.value, newName)
	        XCTAssertEqual(userNameLabel.text, newName)
	    }
	}

This may not look like much, but once your View Controllers start looking like just a bunch of simple bindings to your models, that's when this starts to pay out. And isn't that what one of the View Controller's main responsibility is, to bind the View to the Model's data?

Let's then...

> 1. **Bind the register button’s enabled property to when both the username and the password are valid**, as long as the register button hasn’t been pressed already and we aren’t registering the user via API.

This is going to take a few steps, we'll need to cover hot and cold signals, signal aggregation, transformations and chaining (!), so hang tight.

# Signal transformations
The easiest way to validate that the username, or the password or any other text, are valid is via a transformation. We will transform the user name text into a `Bool` that will indicate whether the username is valid or not.

To do that we need a signal. Luckily, all `MutableProperty<T>` have one. The prefered method to transform one thing into another is `map`.

We won't be covering all other transformations, but what's important is that RAC 4 `Signal`'s `map` doesn't return a new value, but a new `Signal`. Which allows us to do both, biding *and* chaining.

	class ReactiveTests: XCTestCase {
	    
	    func testCompoundBind() {
	        
	        let registerButton = UIButton()
	        let usernameTextField = UITextField()
	        
	        registerButton.rac_enabled <~ usernameTextField.rac_text.signal.map { (text) -> Bool in
	            
	            return text.characters.count >= 8
	        }

	        XCTAssertFalse(registerButton.enabled)

	        usernameTextField.text = "mariano@zerously.com"
	        usernameTextField.sendActionsForControlEvents(.EditingChanged)
	        
	        XCTAssertTrue(registerButton.enabled)
	    }
	}

As you can see here, what we are doing is mapping the text of the username to whether it's valid or not. This is what we meant by a stream being *a river with all it’s water*: we can fully define whether the register button is enabled or not, across time and across values.

There's a couple new concepts in this test though.

`usernameTextField.sendActionsForControlEvents(.EditingChanged)` is there so that the proper event's will be triggered when setting the text by hand. You won't have to worry about this with a live `UITextField` on a `UIViewController`.

And then there's the `rac_enabled` property that isn't present on the `Util.swift` file we mentioned before.

To add new `UIKit` properties simply add to that file something like this:

	extension UIControl {
	    public var rac_enabled: MutableProperty<Bool> {
	        return lazyMutableProperty(self, key: &AssociationKey.enabled, setter: { self.enabled = $0 }, getter: { self.enabled })
	    }
	}

But there's one last a catch here. This test will fail on the first assert. Which brings us to hot and cold signals.

# Hot and cold signals
So, why did that test fail on the first assert?

Since we were using a hot signal, the binding will only be set once the value of the textfield changes for the first time. Remember that:

> If you get the current value (which was set in the past) alongside with whichever new values are set in the future binded into your property then you are using a **cold signal**.  
If you only start getting the new values (whichever are set in the future) binded into your property then you are using a **hot signal**.

In this particular case, if we want the enabled to be "computed" false, we need to consider the preexisting username text value, which is `nil`.

How do we get a cold signal? Using the property's `SignalProducer` instead of the `Signal`. It's that easy.

	class ReactiveTests: XCTestCase {

	    func testCompoundBind() {
	        
	        let registerButton = UIButton()
	        let userNameTextField = UITextField()
	        
	        registerButton.rac_enabled <~ userNameTextField.rac_text.producer.map { (text) -> Bool in
	            
	            return text.characters.count >= 8
	        }

	        XCTAssertFalse(registerButton.enabled)

	        userNameTextField.text = "mariano@zerously.com"
	        userNameTextField.sendActionsForControlEvents(.EditingChanged)
	        
	        XCTAssertTrue(registerButton.enabled)
	    }
	}

All tests passing, now we need to validate the password as well, how do we do that?

# Signal Aggregation

Have you noticed the name of the test? Exactly, "compound", what we need to do is combine both signals, the username's and the password's.

And here we go, we have the first part of the goal resolved.

	class ReactiveTests: XCTestCase {

	    func testCompoundBind() {
	        
	        let registerButton = UIButton()
	        let usernameTextField = UITextField()
	        let passwordTextField = UITextField()
	        
	        registerButton.rac_enabled <~
	            combineLatest(usernameTextField.rac_text.producer, passwordTextField.rac_text.producer)
	            .map { (username, password) -> Bool in
	            
	            return username.characters.count >= 8 &&
	                    password.characters.count >= 8
	            }

	        XCTAssertFalse(registerButton.enabled)

	        usernameTextField.text = "mariano@zerously.com"
	        usernameTextField.sendActionsForControlEvents(.EditingChanged)

	        XCTAssertFalse(registerButton.enabled)

	        passwordTextField.text = "pa55worD"
	        passwordTextField.sendActionsForControlEvents(.EditingChanged)
	        
	        XCTAssertTrue(registerButton.enabled)
	    }
	}

I'm sure you used apps with [way more creative algorithms](https://www.reddit.com/r/Jokes/comments/1v4bpa/passwords/). ;-)

There are other kinds of signal aggregation and operations, but we aren't going to cover that here.

# Chaining
While we were dealing with our goal of enabling the register button when both the username and the password are valid, we were unadvertedly using chaining already. `combineLatest` returns a `Signal` (or `SignalProducer`) to which we can perform other transformations (like mapping) and that's exactly what chaining is all about.

But, this is awful, shall we move this into a View Model?

	class RegisterViewModel {
	    
	    let username = MutableProperty<String?>(nil)
	    let password = MutableProperty<String?>(nil)
	    let registerEnabledSignalProducer: SignalProducer<Bool, NoError>
	    
	    init() {

	        self.registerEnabledSignalProducer = combineLatest(self.username.producer, self.password.producer)
	            .map { (username, password) -> Bool in

	                return username?.characters.count >= 8 &&
	                        password?.characters.count >= 8
	            }
	    }
	}

	class ReactiveTests: XCTestCase {
	    
	    func testModelBind() {
	        
	        let registerViewModel = RegisterViewModel()
	        let registerButton = UIButton()
	        let usernameTextField = UITextField()
	        let passwordTextField = UITextField()
	        
	        registerViewModel.username <~ usernameTextField.rac_text
	        registerViewModel.password <~ passwordTextField.rac_text
	        registerButton.rac_enabled <~ registerViewModel.registerEnabledSignalProducer

	        XCTAssertFalse(registerButton.enabled)

	        usernameTextField.text = "mariano@zerously.com"
	        usernameTextField.sendActionsForControlEvents(.EditingChanged)

	        XCTAssertFalse(registerButton.enabled)

	        passwordTextField.text = "pa55worD"
	        passwordTextField.sendActionsForControlEvents(.EditingChanged)
	        
	        XCTAssertTrue(registerButton.enabled)
	    }
	}

**That's better!** See how all our code starts looking like simple bindings?

# Next
**Part 3 of this series will be coming out soon and it will cover the last part of the goal, binding this to an API service. Stay tuned.**


[^1]: Notice that this is Objc. RAC 4 is mostly built around Swift.
[^2]: If you do that, I'd suggest that you change the `rac_text` type to `MutableProperty<String?>`. Since that's the type of `UILabel`'s text property, so should be the type of the `rac_text` `MutableProperty`.