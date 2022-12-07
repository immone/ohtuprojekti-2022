*** Settings ***
Library  ../libraries/AddLibrary.py

*** Test Cases ***
Add Book Reference
    Input Text  Example Title
    Input Text  Example Author
    Input Text  2022  # Year of publication
    Input Text  Example Publisher
    Input Text  ExampleTag

    Output Should Contain  Reference added
    Output Should Contain  Author2022  # Automatically generated reference ID

Book Reference Is Saved Correctly After Adding
    Input Text  Example Title
    Input Text  Example Author
    Input Text  2022  # Year of publication
    Input Text  Example Publisher
    Input Text  ExampleTag

    Reference Should Be Saved With Provided Fields