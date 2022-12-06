*** Settings ***
Library  ../libraries/SearchLibrary.py

# There are a few mock references that are searched. The references have been named so that they can be referenced easily in the tests
#    SMITH     = "The Origins of Life: A Comprehensive Guide," by Jane Smith and John Doe, published in 2019 by Oxford University Press.
#    RODRIGUEZ = "Advanced Quantum Mechanics: Theory and Applications," by Maria Rodriguez and David Johnson, published in 2020 by Cambridge University Press.
#    JOHNSON   = "The Evolution of Human Language: From Grunts to Grammar," by Sarah Johnson and William Thompson, published in 2021 by Harvard University Press.
#    WILLIAMS  = "The Future of Artificial Intelligence: Implications and Opportunities," by David Williams and Elizabeth Taylor, published in 2022 by Princeton University Press.

*** Test Cases ***
Reference Can Be Searched By Authors
    Input Terms  smith

    Results Should Contain  SMITH

Reference Can Be Searched By Title
    Input Terms  quantum

    Results Should Contain  RODRIGUEZ

Reference Can Be Searched By Year
    Input Terms  2021

    Results Should Contain  JOHNSON

Reference Can Be Searched By Publisher
    Input Terms  princeton

    Results Should Contain  WILLIAMS

Multiple References Can Be Searched With Complicated Search Terms
    Input Terms  origins implications and maria 19  # search terms from every reference except for JOHNSON

    Results Should Contain  SMITH RODRIGUEZ WILLIAMS
