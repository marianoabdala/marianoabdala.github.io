---
layout: post
title:  "Introduction to FRP (part 4)"
date:   2016-04-03 19:55:06 -0300
---

This is the fourth part of the Introduction to FRP series. Here's the [first]({% post_url 2016-03-20-introduction-to-frp-pt1 %}), [second]({% post_url 2016-03-24-introduction-to-frp-pt2 %}) and [third]({% post_url 2016-04-03-introduction-to-frp-pt3 %}) parts.

Believe it or not, this is the easy part, implementing this on a ViewController to use it on an app.

Let's do just that, let's create a ViewController on a Storyboard with the same UI elements as the tests and simply copy the bindings into the new ViewController.

```swift
class ViewController: UIViewController {

    @IBOutlet private weak var errorLabel: UILabel!
    @IBOutlet private weak var usernameTextField: UITextField!
    @IBOutlet private weak var passwordTextField: UITextField!
    @IBOutlet private weak var activityIndicatorView: UIActivityIndicatorView!
    @IBOutlet private weak var registerButton: UIButton!
    
    private let registerService: RegisterServiceProtocol
    private let registerViewModel: RegisterViewModel

    required init?(coder aDecoder: NSCoder) {

        self.registerService = RegisterService(urlSession: NSURLSession.sharedSession())
        self.registerViewModel = RegisterViewModel(registerService: self.registerService)

        super.init(coder: aDecoder)
    }
    
    override func viewDidLoad() {
        
        super.viewDidLoad()
        self.setupBindings()
    }
    
    private func setupBindings() {
        
        self.errorLabel.rac_text <~ registerViewModel.registryError
        self.registerViewModel.username <~ self.usernameTextField.rac_text
        self.registerViewModel.password <~ self.passwordTextField.rac_text
        self.activityIndicatorView.rac_animating <~ registerViewModel.isRegistering
        self.registerButton.rac_enabled <~ self.registerViewModel.registerEnabledSignalProducer
    }
    
    @IBAction private func registerButtonTapped(sender: AnyObject) {
        
        self.registerViewModel.register().observeCompleted { [weak self] in
            
            guard let strongSelf = self else {
                
                return
            }
            
            strongSelf.performSegueWithIdentifier("registerIdentifier", sender: strongSelf)
        }
    }
}
```

This is not a excerp. This is **the whole thing**.

This code covers all of this:
  
> 1. Hook into the textfields' `shouldChangeCharactersInRange:replacementString:` delegate method.  
2. Every time the text changes, check whether it's valid or not.  
3. Check if the counterpart textfield's text is valid.  
4. Check the `isRegistering` property is `false`.  
5. Enable the register button.  
6. Hook into the register button `UIControlEventTouchUpInside` event.  
7. When the register button is tapped collect the username and password values, call the register API and set the `isRegistering` property to `true`.

And more! It also makes the actual API call, handles errors and pushes a new ViewController when succeded.

# Conclusion

FRP leads us to structure our code in such a way that the effort required to implement dependency injection, separation of concerns, testing and other good practices is marginal. 

The amount of code that's not testable is minimal and will rarely fail.

FRP is *intrusive*, meaning that it influences the domain design as well as its implementation and that removing it would require a great amount of time and effort, but there's a big enough community to support and prevent scenarios where you'd have to do so.

# More
A sample project with all the code and working app can be found in [GitHub](https://github.com/marianoabdala/Introduction-to-FRP).