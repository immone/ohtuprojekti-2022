*** Settings ***
Library  ../libraries/EditLibrary.py

*** Test Cases ***
Nonexistent Id Should Not Work

    Input Text  Example Title
    Output Contains  No such reference ID exists

Reference Should Be Edited Correctly
    Input Text  Example Title
    Input Text  Example Author
    Input Text  2022  # Year of publication
    Input Text  Example Publisher
    Input Text  ExampleTag

    Add Inputs
    Reset Input
    Set Type  book

    Input Text  Author2022
    Input Text  Example Title
    Input Text  Example Author
    Input Text  2022  # Year of publication
    Input Text  Example Publisher

    Output Contains  Reference edited.
