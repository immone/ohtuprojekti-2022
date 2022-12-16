*** Settings ***
Library  ../libraries/ListLibrary.py

*** Test Cases ***
Should List All
    Input Text  Example Title
    Input Text  Example Author
    Input Text  2021  # Year of publication
    Input Text  Example Publisher
    Input Text  ExampleTag





Should List Tagged
