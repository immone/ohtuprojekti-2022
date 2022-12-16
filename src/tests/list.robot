*** Settings ***
Library  ../libraries/ListLibrary.py

*** Test Cases ***
Should List All
    Input Text  Example Title
    Input Text  Example Author
    Input Text  2021  # Year of publication
    Input Text  Example Publisher
    Input Text  ExampleTag
    Input Text  Book

    Add Inputs
    Reset Input

    Input Text  no
    Add Inputs

    Should List Correctly  ExampleTag

Should List Any Tagged
    Input Text  Example Title
    Input Text  Example Author
    Input Text  2021  # Year of publication
    Input Text  Example Publisher
    Input Text  ExampleTag
    Input Text  Book

    Add Inputs
    Reset Input

    Input Text  Example TitleToBeTagged
    Input Text  Example AuthorToBeTagged
    Input Text  2021  # Year of publication
    Input Text  Example Publisher
    Input Text  RealTag1
    Input Text  BookToBeTagged

    Input Text  yes
    Input Text  any
    Input Text  RealTag1
    Add Inputs

    Input Text  Example Title2
    Input Text  Example Author2
    Input Text  2021  # Year of publication
    Input Text  Example Publisher2
    Input Text  ExampleTag2
    Input Text  Book2

    Add Inputs

    Should List Correctly  ExampleTag
