*** Settings ***
Library  ../libraries/DeleteLibrary.py

*** Test Cases ***
Nonexistent Id Should Not Work
    Input Text  NonExistent
    Output Contains  No such reference ID exists

Existent Id Should Work
    Input Text  Example Title
    Input Text  Example Author
    Input Text  2022  # Year of publication
    Input Text  Example Publisher
    Input Text  ExampleTag

    Add Inputs
    Reset Input

    Input Text  Example Title

    Output Contains  Reference deleted

Two Book References Should Be Deleted Correctly
    Input Text  Example Title
    Input Text  Example Author
    Input Text  2021  # Year of publication
    Input Text  Example Publisher
    Input Text  ExampleTag

    Add Inputs
    Reset Input

    Input Text  Example Title2
    Input Text  Example Author
    Input Text  2022  # Year of publication2
    Input Text  Example Publisher2
    Input Text  ExampleTag2

    Add Inputs
    Reset Input

    Input Text  Author2022
    Reference Should Be Deleted Correctly

    Reset Input

    Input Text  Author2021
    Add Inputs
    Reference Should Be Deleted Correctly