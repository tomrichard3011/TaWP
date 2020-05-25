# TaWP
Targeted Wordlist Project

Takes biographical information about a person and creates a wordlist using those words.

To create a large list, we use the cartesian product of the words against themselves.

![Cartesian Product Img](https://upload.wikimedia.org/wikipedia/commons/4/4e/Cartesian_Product_qtl1.svg)

Basic information needed: first name, last name, date of birth

Main features:
- case transformation: john, John, jOhn, JOhn, etc.
- leet transformation: doe, d0e, d03, etc. 
- levels of leet *view below for more info*
- Number manipulation; 10/12/1920, 12101920, 19201012, etc.

**Leet Level Description**
There are three levels of leet included for character replacement. The suggested level is 2, 
and 3 may run into memory issues if you have too much info.
