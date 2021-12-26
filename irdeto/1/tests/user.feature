Feature: User
    Scenario: User logs in with valid username and password
        Given SUT is in Login state
        And User with user:password credentials exists
        When GET request with username=user&password=password is sent to user/login endpoint
        Then Response status == 200
        And SUT state changed to Dashboard

    Scenario: SUT remains in Login state if User enters invalid username 
        Given SUT is in Login state
        And User with user:password credentials doesn't exist
        When GET request with username=user&password=password is sent to user/login endpoint
        Then Response status == 400
        And SUT remains in Login state
        And Error message displayed

    Scenario: SUT remains in Login state if User enters invalid password
        Given SUT is in Login state
        And User with user username exists
        And User's password is not password
        When GET request with username=user&password=password is sent to user/login endpoint
        Then Response status == 400
        And SUT remains in Login state
        And Error message displayed

    Scenario: User's username can be changed and User can login afterwards with new credentials
        Given SUT is in Config state
        And User with username:password credentials exists
        And User's userId == 1
        When PUT request with username=user1 is sent to user/1 endpoint
        Then Response status == 200
        And SUT switches to Login state
        And User logs in with username1:password credentials

    Scenario: User's password can be changed and User can login afterwards with new credentials
        Given SUT is in Config state
        And User with username:password credentials exists
        And User's userId == 1
        When PUT request with password=password1 is sent to user/1 endpoint
        Then Response status == 200
        And SUT switches to Login state
        And User logs in with username1:password1 credentials

    Scenario: User's control access can be changed to "allow" and User logs in afterwards
        Given SUT is in Config state
        And User with username:password credentials exists
        And User's userId == 1
        And User's controlAccess == "deny"
        When PUT request with controlAccess=allow is sent to user/1 endpoint
        Then Response status == 200
        And SUT switches to Login state
        And User logs in with username:password credentials
        And User controlAccess == "allow"

    # Some stubs:
    Scenario: User's control access can be changed to "deny" and User logs in afterwards

    Scenario: SUT remains in Config state if password is not changed
    Scenario: SUT remains in Config state if username is not changed
    Scenario: SUT remains in Config state if control access is not changed

