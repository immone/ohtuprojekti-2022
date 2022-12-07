*** Settings ***
Library  ../libraries/EditLibrary.py

*** Test Cases ***
Nonexistent Id Should Not Work
    Input Text  NonExistent
    Input Text  Example Author
    Input Text  2022  # Year of publication
    Input Text  Example Publisher
    Input Text  ExampleTag

    Output Contains  Wrong parameters

Existent Id Should Work
    Input Text  Example Title
    Input Text  Example Author
    Input Text  2022  # Year of publication
    Input Text  Example Publisher
    Input Text  ExampleTag

    Add Inputs
    Reset Input

    Input Text  Example Title
    Input Text  Example Author
    Input Text  2022  # Year of publication
    Input Text  Example Publisher
    Input Text  ExampleTag

    Output Contains  Reference edited

Book Reference Should Be Edited Correctly
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
    
    Reference Should Edited Correctly