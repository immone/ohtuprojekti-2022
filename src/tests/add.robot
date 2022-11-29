*** Settings ***
Library  ../libraries/AddLibrary.py

*** Test Cases ***
Add Book Reference
    Input Text  ExampleId
    Input Text  Example Title
    Input Text  1  # Number of authors
    Input Text  Example Author
    Input Text  2022  # Year of publication
    Input Text  Example Publisher

    Output Should Contain  Reference added

Book Reference Is Saved Correctly After Adding
    Input Text  ExampleId
    Input Text  Example Title
    Input Text  1  # Number of authors
    Input Text  Example Author
    Input Text  2022  # Year of publication
    Input Text  Example Publisher

    Reference Should Be Saved With Provided Fields