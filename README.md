Urdu Spell and Grammar Checker

Introduction:

Urdu Spell and Grammar Checker is a simple desktop application built with Python and Tkinter that provides spell-checking and basic grammar correction for Urdu language text. The application incorporates fuzzy matching and language identification to offer suggestions for misspelled words and identifies potential grammar errors.

Key Features:

- Spell Checking: Detects and suggests corrections for misspelled Urdu words.
- Grammar Checking: Utilizes the Stanza library to identify and correct basic grammar errors in Urdu sentences.
- User-Friendly Interface: An intuitive Tkinter-based interface allows users to enter Urdu sentences, check spelling and grammar, and receive suggestions for corrections.

Below are the libraries used in your project:

1. Tkinter:
   - Description: Tkinter is the standard GUI (Graphical User Interface) toolkit that comes with Python. It is widely used for creating desktop applications with a graphical interface.
   - Purpose in the Project: Tkinter is used to build the graphical user interface for the Urdu Spell and Grammar Checker application. It provides widgets such as labels, entry fields, buttons, and text areas to create an interactive user interface.

2. fuzzywuzzy:
   - Description: Fuzzywuzzy is a library in Python that provides fuzzy string matching, which measures the similarity between strings. It is particularly useful for spell-checking and suggesting corrections for misspelled words.
   - Purpose in the Project: Fuzzywuzzy is used to calculate similarity scores between words in the input sentence and a pre-defined list of Urdu words. This helps suggest corrections for misspelled words.

3. langid:
   - Description: Langid is a library for language identification in Python. It classifies the language of a given text.
   - Purpose in the Project: Langid is used to identify the language of the input sentence, ensuring that the spell and grammar checks are performed specifically for Urdu text.

4. stanza:
   - Description: Stanza is a natural language processing library for Python. It provides pre-trained models for various languages, including Urdu, for tasks such as tokenization, part-of-speech tagging, and dependency parsing.
   - Purpose in the Project: Stanza is used to download and load the Urdu language model. It helps in processing the input sentence to identify and correct basic grammar errors.

These libraries collectively contribute to the functionality of the Urdu Spell and Grammar Checker, providing tools for user interface development, fuzzy string matching, language identification, and natural language processing.
