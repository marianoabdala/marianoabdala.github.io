---
layout: post
title:  "Introduction to FRP (part 3)"
date:   2016-04-03 10:22:32 -0300
---

This is the third part of the Introduction to FRP series. Here's the [first]({% post_url 2016-03-20-introduction-to-frp-pt1 %}) and [second]({% post_url 2016-03-24-introduction-to-frp-pt2 %}) parts.

Here, we'll be covering networking. In itself, networking with FRP isn't a long subject, but it provides us with an excuse to cover many generic FRP concepts that normally happen (and are easier to explain and grasp) when you use it to manage networking.

Let's pick it up where we left it and focus on the second part of the statement:
  
> 1. Bind the register button’s enabled property to when both the username and the password are valid, **as long as the register button hasn’t been pressed already and we aren’t registering the user via API**.

To achieve this we'll add a `isRegistering` property on the `RegisterViewModel` and update the `registerEnabledSignalProducer` that drives whether the register button is enabled:

```swift
struct RegisterViewModel {

    let username = MutableProperty<String?>(nil)
    let password = MutableProperty<String?>(nil)
    let registerEnabledSignalProducer: SignalProducer<Bool, NoError>
    let isRegistering = MutableProperty(false)

    init() {

        self.registerEnabledSignalProducer = combineLatest(self.username.producer, self.password.producer, self.isRegistering.producer)
            .map { (username, password, isRegistering) -> Bool in

              return username?.characters.count >= 8 &&
                      password?.characters.count >= 8 &&
                      isRegistering == false
            }
    }
}
```

Now all we need to do is set the value of the `isRegistering` property when we call the API and when the API responds. Notice Also that we combined username, password and isRegistering using `combineLatest`, which allows us to combine up to 10 `Signal`s/`SignalProducer`s!!

So, let's get our hands dirty, shall we? Let's make and actual API call and handle it, even though **we already covered the original requirements**.

# Simple Service

```swift
struct RegisterService {
    
    private let urlSession: NSURLSession
    
    init(urlSession: NSURLSession) {
        
        self.urlSession = urlSession
    }
    
    func register(username username: String, password: String) -> SignalProducer<(NSData, NSURLResponse), NSError> {

        // Let's assume we are inserting username and password to the request.
        guard let url = NSURL(string: "http://zerously.com/misc/register.json") else {
            
            return SignalProducer<(NSData, NSURLResponse), NSError>(error: NSError(domain: "RegisterService", code: -1, userInfo: ["Reason": "Invalid URL."]))
        }
        
        let request = NSURLRequest(URL: url)
        return self.urlSession.rac_dataWithRequest(request)
    }
}
```

The key to this service is that we aren't returning a value or a model, we are returning a SignalProducer, for the consumer to transform, manage and handle; and ReactiveCocoa has a very handy method to achieve that right of from a `NSURLSession`, the `rac_dataWithRequest(_:)` method.

For simplicity sake we aren't adding username and password to the request, but we could verify if they are valid and return a `SignalProducer` that will produce an error immediately in a similary way as the one shown in the code, for verifying the URL is valid.

# Usage from the View Model

Here's how a rough call to this would look like from the ViewModel:

```swift
struct RegisterViewModel {

    let registerService: RegisterService

    init(registerService: RegisterService) {

        self.registerService = registerService
        ...
    }

    func register() {

        guard let username = self.username.value,
                    password = self.password.value else {

                return
        }

        self.isRegistering.value = true

        self.registerService.register(username: username, password: password)
            .observeOn(UIScheduler())
            .startWithNext {

                self.isRegistering.value = false
            }
    }
}
```

A few things to note here:

* We are injecting the `RegisterService` into the ViewModel, we'll see how that's useful later.
* We are handling the happy path for the `isRegistering` property we created previously.
* We are calling `.observeOn(UIScheduler())` to make sure we are working on the main thread from here on since the changes in `isRegistering` will affect UI.

Seems like we are forgetting something? We aren't doing anything with the result of the API call! We need to inform the ViewController that we finished registering the user successfully, so...

```swift
func register() -> Bool {

	...
}
```

What? **No!**

By now, we know much more expresive and rective ways of doing this... It'll require us not to consume, but to create a `Signal`.

```swift
func register() -> Signal<Void, NoError> {

    var didRegisterSink: Observer<Void, NoError>?
    let didRegisterSignal = Signal<Void, NoError> { (sink) -> Disposable? in
        
        didRegisterSink = sink
        return nil
    }
    
    self.isRegistering.value = true

    self.registerService.register(username: username, password: password)
        .observeOn(UIScheduler())
        .startWithNext {

            self.isRegistering.value = false
            didRegisterSink?.sendCompleted()
    	}
    
    return didRegisterSignal
}
```

So, how does this work?

Every time you create a `Signal` or a `SignalProducer` you'll get a `sink` that's going to be the reciever of the events. Just like to `observeNext` or `observeCompleted` you can `sendNext` and `sendCompleted` on the other side, on the sink.

We can now bind this to our test.

```swift
func testAPICall() {
    
    let registerService = RegisterService(urlSession: NSURLSession.sharedSession())
    let registerViewModel = RegisterViewModel(registerService: registerService)
    let registerButton = UIButton()
    let usernameTextField = UITextField()
    let passwordTextField = UITextField()
    
    registerViewModel.username <~ usernameTextField.rac_text
    registerViewModel.password <~ passwordTextField.rac_text
    registerButton.rac_enabled <~ registerViewModel.registerEnabledSignalProducer

    XCTAssertFalse(registerButton.enabled)
    
    usernameTextField.inputText("mariano@zerously.com")
    
    XCTAssertFalse(registerButton.enabled)
    
    passwordTextField.inputText("pa55worD")
    
    XCTAssertTrue(registerButton.enabled)
    
    let expectation = expectationWithDescription("Wait for register to return")

    registerViewModel.register().observeCompleted {

        XCTAssertTrue(registerButton.enabled)

        // On a View Controller, we'd probably move to the onboarding screen.
        // Since this is a test, we'll simply mark the expectation as fulfilled.
        expectation.fulfill()
    }
    
    XCTAssertFalse(registerButton.enabled)
    
    waitForExpectationsWithTimeout(10) { (error) in
        
        if error != nil {

            XCTFail()
        }
    }
}
```

# Non-trivial behaviour

As we add non-trivial behaviour to this example, we have to make sure we have errors handled too, so let's add a `registryError` property and bind it in our tests to a `errorLabel`. While we are here, let's add an `activityIndicatorView` and bind it to the `isRegistering` property.

To achieve bindablity on a `UIActivityIndicatorView` we need to add the following to the `Util.swift` file:

```swift
extension UIActivityIndicatorView {
    public var rac_animating: MutableProperty<Bool> {
        return lazyMutableProperty(self, key: &AssociationKey.animated, setter: { if $0 { self.startAnimating() } else { self.stopAnimating() } }, getter: { self.isAnimating() })
    }
}
```

Expanding the test would look like this:

```swift
func testAPICall() {
    
    let registerService = RegisterService(urlSession: NSURLSession.sharedSession())
    let registerViewModel = RegisterViewModel(registerService: registerService)
    let registerButton = UIButton()
    let usernameTextField = UITextField()
    let passwordTextField = UITextField()
    
    registerViewModel.username <~ usernameTextField.rac_text
    registerViewModel.password <~ passwordTextField.rac_text
    registerButton.rac_enabled <~ registerViewModel.registerEnabledSignalProducer

    XCTAssertFalse(registerButton.enabled)
    
    usernameTextField.inputText("mariano@zerously.com")
    
    XCTAssertFalse(registerButton.enabled)
    
    passwordTextField.inputText("pa55worD")
    
    XCTAssertTrue(registerButton.enabled)
    
    let activityIndicatorView = UIActivityIndicatorView()
    let errorLabel = UILabel()
    
    errorLabel.rac_text <~ registerViewModel.registryError
    activityIndicatorView.rac_animating <~ registerViewModel.isRegistering
    
    let expectation = expectationWithDescription("Wait for register to return")

    registerViewModel.register().observeCompleted {

        XCTAssertTrue(registerButton.enabled)
        XCTAssertFalse(activityIndicatorView.isAnimating())

        // On a View Controller, we'd probably move to the onboarding screen.
        // Since this is a test, we'll simply mark the expectation as fulfilled.
        expectation.fulfill()
    }
    
    XCTAssertFalse(registerButton.enabled)
    XCTAssertTrue(activityIndicatorView.isAnimating())
    
    waitForExpectationsWithTimeout(10) { (error) in
        
        if error != nil {

            XCTFail()
        }
    }
}
```

And this is how the expanded `register` fuction would look like:

```swift
func register() -> Signal<Void, NoError> {

    var didRegisterSink: Observer<Void, NoError>?
    let didRegisterSignal = Signal<Void, NoError> { (sink) -> Disposable? in
        
        didRegisterSink = sink
        return nil
    }
    
    guard let username = self.username.value,
                password = self.password.value else {

            self.registryError.value = "Invalid username or password"
            self.isRegistering.value = false
            
            return didRegisterSignal
    }

    self.isRegistering.value = true

    self.registerService.register(username: username, password: password)
        .map { (data, urlResponse) -> String? in
    
            self.isRegistering.value = false
            
            if let responseDictionary = try? NSJSONSerialization.JSONObjectWithData(data, options: .MutableLeaves) as! [String: AnyObject] {
                
                return responseDictionary["token"] as? String
                
            } else {
                
                return nil
            }
        }
        .mapError { (error) -> NSError in

            self.registryError.value = error.userInfo["Reason"] as? String
            self.isRegistering.value = false

            return error
        }
        .observeOn(UIScheduler())
        .startWithNext { (token) in

            if let token = token {
                
                // Let's assume that the token should go into some sort of
                // local authentication store for later use.
                print(token)
                
                self.isRegistering.value = false
                didRegisterSink?.sendCompleted()
                
            } else {
                
                self.registryError.value = "Invalid token"
                self.isRegistering.value = false
            }
    }
    
    return didRegisterSignal
}
```

This exemplifies non-trivial usage of mapping, chanining, binding and signal creation. Just like `observeNext` is triggered when the observer does a `sendNext`, and the `map` transforms the data a `Signal` sends, the `mapError` transforms the data a `Signal` sends when there's been an error.

# Testing Error handling

Our tests didn't include the error handling, so let's make sure that works as we expect. For doing so, we'll need our RegisterService to fail, in a few different ways.

Luckily we already are injecting the RegisterService and we can choose to inject a failing RegisterService instead.

To achieve that, we'll need to standardize the `RegisterService` the ViewModel uses into a protocol:

```swift
protocol RegisterServiceProtocol {
    
    func register(username username: String, password: String) -> SignalProducer<(NSData, NSURLResponse), NSError>
}
```

Have `RegisterService` inherite from it:

```swift
struct RegisterService: RegisterServiceProtocol {

	...
}
```

And have the `RegisterViewModel` taking that as a valid initializer:

```swift
struct RegisterViewModel {
    
    let registerService: RegisterServiceProtocol

    init(registerService: RegisterServiceProtocol) {

        self.registerService = registerService
        ...
    }
}
```

Our tests should still be passing, but they aren't considering any failure. Let's create a new test that will address that. Notice that we are using the `NoTokenRegisterService` this time, to force an issue and test how we handle it.

```swift
func testAPICallDataFailure() {
    
    let registerService = NoTokenRegisterService(urlSession: NSURLSession.sharedSession())
    let registerViewModel = RegisterViewModel(registerService: registerService)
    let registerButton = UIButton()
    let usernameTextField = UITextField()
    let passwordTextField = UITextField()
    
    registerViewModel.username <~ usernameTextField.rac_text
    registerViewModel.password <~ passwordTextField.rac_text
    registerButton.rac_enabled <~ registerViewModel.registerEnabledSignalProducer

    usernameTextField.inputText("mariano@zerously.com")
    passwordTextField.inputText("pa55worD")

    let activityIndicatorView = UIActivityIndicatorView()
    let errorLabel = UILabel()
    
    errorLabel.rac_text <~ registerViewModel.registryError
    activityIndicatorView.rac_animating <~ registerViewModel.isRegistering
    
    registerViewModel.register().observeCompleted {

        XCTFail("Should fail and not call sendCompleted")
    }
    
    XCTAssertTrue(registerButton.enabled)
    XCTAssertFalse(activityIndicatorView.isAnimating())
    XCTAssertEqual(errorLabel.text, "Invalid token")
}
```

Here's the NoTokenRegisterService code:

```swift
struct NoTokenRegisterService: RegisterServiceProtocol {

    private let urlSession: NSURLSession
    
    init(urlSession: NSURLSession) {
        
        self.urlSession = urlSession
    }

    func register(username username: String, password: String) -> SignalProducer<(NSData, NSURLResponse), NSError> {
        
        let signalProducer = SignalProducer<(NSData, NSURLResponse), NSError> { (sink, compositeDisposable) in
            
            let data = try! NSJSONSerialization.dataWithJSONObject(["Hello": "No Token Here"], options: .PrettyPrinted)
            let urlResponse = NSURLResponse()
            
            sink.sendNext((data, urlResponse))
        }
        
        return signalProducer
    }
}
```

And here's the `ErrorRegisterService` and its test:

```swift
struct ErrorRegisterService: RegisterServiceProtocol {
    
    private let urlSession: NSURLSession
    
    init(urlSession: NSURLSession) {
        
        self.urlSession = urlSession
    }
    
    func register(username username: String, password: String) -> SignalProducer<(NSData, NSURLResponse), NSError> {
        
        return SignalProducer<(NSData, NSURLResponse), NSError>(error: NSError(domain: "RegisterService", code: -1, userInfo: ["Reason": "Dunno."]))
    }
}

class ReactiveTests: XCTestCase {
    
    func testAPICallError() {
        
        let registerService = ErrorRegisterService(urlSession: NSURLSession.sharedSession())
        let registerViewModel = RegisterViewModel(registerService: registerService)
        let registerButton = UIButton()
        let usernameTextField = UITextField()
        let passwordTextField = UITextField()
        
        registerViewModel.username <~ usernameTextField.rac_text
        registerViewModel.password <~ passwordTextField.rac_text
        registerButton.rac_enabled <~ registerViewModel.registerEnabledSignalProducer
        
        usernameTextField.inputText("mariano@zerously.com")
        passwordTextField.inputText("pa55worD")
        
        let activityIndicatorView = UIActivityIndicatorView()
        let errorLabel = UILabel()
        
        errorLabel.rac_text <~ registerViewModel.registryError
        activityIndicatorView.rac_animating <~ registerViewModel.isRegistering
        
        registerViewModel.register().observeCompleted {
            
            XCTFail("Should fail and not call sendCompleted")
        }
        
        XCTAssertTrue(registerButton.enabled)
        XCTAssertFalse(activityIndicatorView.isAnimating())
        XCTAssertEqual(errorLabel.text, "Dunno.")
    }
}
```

This is all great. We have things working the way we want, and reasonable test coverage. Shall we move this into a ViewController and see how it looks on an app rather than on tests?

# Next
[Part 4]({% post_url 2016-04-03-introduction-to-frp-pt4 %}): Using ReactiveCocoa 4 on an app.