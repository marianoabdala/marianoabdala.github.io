---
layout: post
title:  "Restricting Access with Protocols"
date:   2016-06-28 12:33:23 -0300
---

One very common pattern to drive communications with a backend server in iOS is to have a huge _Client_ class. That client usually consists of some sort of initialization, configuration, some shared state --like a queue of operations-- and a large collection of functions to either fetch something from the server or reflect on it some change in the app's internal data state. Each of those functions normally have complex parameters and return values.

You may have also observed a protocol with _each and every_ communication option with the server being passed around to view controllers, view models, a sync engine or any other communication orchestrator.

Ever found something of this sort?

This makes the client hard to test because mocking a test class means replicating a huge protocol, unsecure because everyone with a reference to the client can call any function, even if by accident, and hard to understand because of the access to said great amount of functions provides with little context.

One approach, that may not always be applicable, is to extract common behaviour somewhere else and turn those functions into well defined operations that you dispatch into said place. The main problem with this is that it must be done all at once.

A middle-ground solution, and one that may be implemented **gradually**, is to restrict access with protocols.

#### How do you do that?

By the use of protocols you can define and group functionallity together. For instance, instead of having one huge `Client` protocol, start by spliting it into smaller chuncks.

You can use your view models as a guide. The `FollowedUsersListViewModel` may use `fecth`, `follow` and `unfollow`.

Create a protocol for such purpose:

```swift
protocol UserListingClient {

    func fetchUsers() -> [UserModel]
    func follow(_ user: UserModel)
    func unfollow(_ user: UserModel)
}
```

And change the view model to initialize with such a client, as opposed to giving it access to the whole _Client_.

```swift
class FollowedUsersListViewModel {

    init(withClient client: UserListingClient) {

        ...
    }
}
```

Now, your view model will only be able to access the right functions on your client.

#### Next step
Let's see how the `UserDetailViewModel`'s client may look like:

```swift
protocol UserDetailsClient {

    func fetchUserDetails(for user: UserModel) -> UserDetailsModel
    func follow(_ user: UserModel)
    func unfollow(_ user: UserModel)
}
```

And change the view model to initialize with such a client.

```swift
class UserDetailsViewModel {

    init(withUser user: UserModel, client: UserDetailsClient) {

        ...
    }
}
```


Have you noticied that both `UserListingClient` and `UserDetailsClient` use `follow` and `unfollow`?

Let's extract those into a `UserFollowingClient` and add that protocol to the `UserListingClient` and `UserDetailsClient` protocols.

```swift
protocol UserFollowingClient {
    
    func follow(_ user: UserModel)
    func unfollow(_ user: UserModel)
}

protocol UserListingClient: UserFollowingClient {
 
    func fetchUsers() -> [UserModel]
}

protocol UserDetailsClient: UserFollowingClient {
    
    func fetchUserDetails(for user: UserModel) -> UserDetailsModel
}
```

#### A bit deeper
Let's say we add a the ability to report a user from both the list and the user details for misbheaviour. We can simply define the `UserReportingClient` protocol and add it to the `UserListingClient` and the `UserDetailsClient`, like this:

```swift
enum UserReportingReason {
    
    case ...
}

protocol UserReportingClient {
    
    func report(_ user: UserModel, for reason: UserReportingReason)
}

protocol UserListingClient: UserFollowingClient, UserReportingClient {
    
    func fetchUsers() -> [UserModel]
}

protocol UserDetailsClient: UserFollowingClient, UserReportingClient {
    
    func fetchUserDetails(for user: UserModel) -> UserDetailsModel
}
```

There! No need to change the view models.

#### Free feature set mapping
By doing this you not only restrict the functions that each of your view models will be able to access, but also start to design a map of how your client may be divided into smaller chuncks.

One way of doing this is moving the functions into independent extensions of their smaller grouping.

```swift
extension Client: UserFollowingClient {
    
    func follow(_ user: UserModel) {
        
        ...
    }
    
    func unfollow(_ user: UserModel) {
        
        ...    
    }
}
```

This alone will help in extracting operation specific code out of the main class, making it easier in the future to identify the client's core feature set and operations.

#### Easier mocking
Good unit testing is key in assuring the stability of an app's codebase, but sometimes testing is just too hard.

By exposing smaller units of behaviour, your tests should be easier to write. Specially when trying to mock the client.

Say we want to test the `FollowedUsersListViewModel` and we want to test error handling. We don't need to mock the whole client, we can just create a mock class that only implements `UserListingClient`.

Let's modify `UserListingClient` and its protocols to have all methods `throw`:

```swift
protocol UserFollowingClient {
    
    func follow(_ user: UserModel) throws
    func unfollow(_ user: UserModel) throws
}

protocol UserReportingClient {
    
    func report(_ user: UserModel, for reason: UserReportingReason) throws
}

protocol UserListingClient: UserFollowingClient, UserReportingClient {
    
    func fetchUsers() throws -> [UserModel]
}
```

And make a simple mock class to test exactly that.

```swift
enum MyError: ErrorProtocol {
    
    case SomeError
}

class ThrowingUserListingClient: UserListingClient {
    
    func follow(_ user: UserModel) throws {
        
        throw MyError.SomeError
    }
    
    func unfollow(_ user: UserModel) throws {
        
        throw MyError.SomeError
    }
    
    func report(_ user: UserModel, for reason: UserReportingReason) throws {
        
        throw MyError.SomeError
    }
    
    func fetchUsers() throws -> [UserModel] {
        
        throw MyError.SomeError
    }
}
```

Pass that to `FollowedUsersListViewModel` and test away!

#### Done
Smaller chuncks of code, more control, more context, easier to mock clients, one step closer to being able to split a huge class into smaller classes.
