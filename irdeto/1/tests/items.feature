Feature: Items
    Scenario: Items page can be switched to next
        Given SUT is in Dashboard state
        And there are page_quantifier + n items
        And page==0
        When GET request with page=1 is sent to items endpoint
        Then Response status == 200
        And Response body contains list of items with n items

    Scenario: Items page can be switched to previous
        Given SUT is in Dashboard state
        And there are page_quantifier + n items
        And page==1
        When GET request with page=0 is sent to items endpoint
        Then Response status == 200
        And Response body contains list of items with page_quantifier items

    Scenario: Items can be sorted by date in descending order
        Given SUT is in Dashboard state
        And there are page_quantifier + n items
        And page==0
        And items are not sorted by date
        When GET request with sortByDate=desc is sent to items endpoint
        Then Response status == 200
        And Response body contains list of items sorted by date in descending order

    Scenario: Items can be sorted by date in ascending order
        Given SUT is in Dashboard state
        And there are page_quantifier + n items
        And page==0
        And items are not sorted by date
        When GET request with sortByDate=asc is sent to items endpoint
        Then Response status == 200
        And Response body contains list of items sorted by date in ascending order

    Scenario: Items can be filtered by run state
        Given SUT is in Dashboard state
        And there are page_quantifier + n items
        And page==0
        And there are A items of run, B items of pause and C items of stop state
        And A <= page_quantifier and B <= page_quantifier and C <= page_quantifier
        When GET request with state=run is sent to items endpoint
        Then Response status == 200
        And Response body contains list of A items with run state

    # Some stubs:
    Scenario: Items page is not switched if no more items left

    Scenario: Items can be filtered by pause state
    Scenario: Items can be filtered by stop state