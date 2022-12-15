*** Settings ***
Library  ../libraries/TranslatorLibrary.py

    
*** Test Cases ***
All References With Empty Input
    Input Text  <EMPTY>
    
    Get All Refs

Tagged References With Tag
    Input Text  t-ttt

    Get With Tag  


