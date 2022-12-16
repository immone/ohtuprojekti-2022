*** Settings ***
Library  ../libraries/AddLibrary.py

*** Test Cases ***
Add Book Reference
    Input Text  1  # 1 = book
    Input Text  Example Title
    Input Text  Example Author
    Input Text  2022  # Year of publication
    Input Text  Example Publisher
    Input Text  ExampleTag

    Output Should Contain  Reference added
    Output Should Contain  Author2022  # Automatically generated reference ID

Book Reference Is Saved Correctly After Adding
    Input Text  1  # 1 = book
    Input Text  Example Title
    Input Text  Example Author
    Input Text  2022  # Year of publication
    Input Text  Example Publisher
    Input Text  ExampleTag

    Book Reference Should Be Saved With Provided Fields

Add InProceedings Reference
    Input Text  2  # 2 = inproceedings
    Input Text  Example Title
    Input Text  Example Book Title
    Input Text  Example Author
    Input Text  Example Series
    Input Text  2022  # Year of publication
    Input Text  100--200  # Pages
    Input Text  Example Publisher
    Input Text  Example Address
    Input Text  ExampleTag

    Output Should Contain  Reference added
    Output Should Contain  Author2022  # Automatically generated reference ID

InProceedings Reference Is Saved Correctly After Adding
    Input Text  2  # 2 = inproceedings
    Input Text  Example Title
    Input Text  Example Book Title
    Input Text  Example Author
    Input Text  Example Series
    Input Text  2022  # Year of publication
    Input Text  100--200  # Pages
    Input Text  Example Publisher
    Input Text  Example Address
    Input Text  ExampleTag

    InProceedings Reference Should Be Saved With Provided Fields

Add Misc Reference
    Input Text  3  # 3 = misc
    Input Text  Example Title
    Input Text  Example Author
    Input Text  Example HowPublished
    Input Text  2022  # Year of publication
    Input Text  Example Note
    Input Text  ExampleTag

    Output Should Contain  Reference added
    Output Should Contain  Author2022  # Automatically generated reference ID

Misc Reference Is Saved Correctly After Adding
    Input Text  3  # 3 = misc
    Input Text  Example Title
    Input Text  Example Author
    Input Text  Example HowPublished
    Input Text  2022  # Year of publication
    Input Text  Example Note
    Input Text  ExampleTag

    Misc Reference Should Be Saved With Provided Fields