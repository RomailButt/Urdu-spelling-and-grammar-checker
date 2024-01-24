import enchant
from nltk.tokenize import word_tokenize
import language_tool_python

def spelling_checker(input_text):
    words = word_tokenize(input_text)
    english_dict = enchant.Dict("en_US")
    suggestions = {}
    words = [word for word in words if word.isalpha()]
    for word in words:
        if not english_dict.check(word):
            suggestions[word] = english_dict.suggest(word)
    return suggestions

def correct_spelling_input(suggestions):
    replacements = {}
    for misspelled_word, suggested_words in suggestions.items():
        print(f"\nWord: {misspelled_word}")
        print(f"Suggestions:")
        for index, suggestion in enumerate(suggested_words, start=1):
            print(f"   {index}. {suggestion}")
        while True:
            try:
                choice = int(input(f"Press the number to replace with (or 0 to keep the original): "))
                if choice == 0:
                    break
                elif 1 <= choice <= len(suggested_words):
                    replacements[misspelled_word] = suggested_words[choice - 1]
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    return replacements

def replace_words(input_text, replacements):
    for misspelled_word, replacement in replacements.items():
        input_text = input_text.replace(misspelled_word, replacement)
    return input_text

def grammar_checker(corrected_text):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(corrected_text)
    return matches

if __name__ == "__main__":
    user_input = input("Enter a paragraph or sentence: ")
    suggestions = spelling_checker(user_input)
    if suggestions:
        replacements = correct_spelling_input(suggestions)
        corrected_text = replace_words(user_input, replacements)
        print(f"\nCorrected paragraph:\n{corrected_text}")

        # Check grammar and language
        grammar_matches = grammar_checker(corrected_text)

        if grammar_matches:
            print("\nGrammar issues:")
            for match in grammar_matches:
                print(f"   {match.ruleId}: {match.message}")
        else:
            print("\nNo grammar issues found.")
    else:
        print("No spelling mistakes found.")
