*** Settings ***
Library  ../libraries/EditLibrary.py

*** Test Cases ***
Nonexistent Id Should Not Work

    Input Text  Example Title
    Input Text  Example Author
    Input Text  2022  # Year of publication
    Input Text  Example Publisher
    Input Text  ExampleTag

    Add Inputs
    Set Type  book
    Reset Input

    Input Text  NonExistent ID
    Input Text  Example Title2
    Input Text  Example Author2
    Input Text  2021 # Year of publication
    Input Text  Example Publisher2
    Input Text  ExampleTag2

    Output Contains  No such reference ID exists

Reference Should Be Edited Correctly
    Input Text  Example Title
    Input Text  Example Author
    Input Text  2022  # Year of publication
    Input Text  Example Publisher
    Input Text  ExampleTag

    Add Inputs
    Reset Input

    Input Text  Author2022
    Input Text  Example Title
    Input Text  Example Author
    Input Text  2022  # Year of publication
    Input Text  Example Publisher

    Reference Should Be Edited Correctly
