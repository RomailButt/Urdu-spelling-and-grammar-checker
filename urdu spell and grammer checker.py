from fuzzywuzzy import fuzz, process
import langid
import stanza
import string

# Read the word list from the file
with open('urduList.txt', 'r', encoding='utf-8') as file:
    word_list = [line.strip() for line in file]

def remove_punctuation(word):
    # Exclude specific punctuation marks from removal
    exclude_chars = set("،.٫-۔")  # Add more punctuation marks if needed
    return ''.join(char for char in word if char not in exclude_chars)

def suggest_most_matched_words(incorrect_word):
    # Calculate similarity scores for each word in the list
    similarity_scores = process.extract(incorrect_word, word_list, scorer=fuzz.ratio)

    # Return a list of similar words
    return [word for word, _ in similarity_scores]

def correct_grammar(sentence):
    # Implement your grammar correction rules here
    # This is a simple example that just capitalizes the first letter
    return sentence.capitalize()

def is_urdu(text):
    lang, _ = langid.classify(text)
    return lang == 'ur'

def urdu_grammar_checker(sentence):
    if not is_urdu(sentence):
        print("Input is not in Urdu.")
        return

    # Download and load the Urdu language model from stanza
    stanza.download('ur')
    nlp = stanza.Pipeline('urdu')

    # Process the input sentence using stanza
    doc = nlp(sentence)

    # Check for grammar errors
    errors = []
    for sentence in doc.sentences:
        for word in sentence.words:
            # Add specific rules for grammar checks
            # Example: Check for incorrect verb forms
            if word.upos == 'VERB' and word.feats and 'VerbForm=Fin' not in word.feats:
                errors.append(word.text)

    return errors

if __name__ == "__main__":
    # Get input sentence from the user
    input_sentence = input("Enter a sentence in Urdu: ")

    # Check if the input is in Urdu
    if is_urdu(input_sentence):
        # Check grammar
        error_words = urdu_grammar_checker(input_sentence)

        if not error_words:
            print("No grammar errors found. The sentence is correct.")
        else:
            print("Grammar errors found in the following words:", error_words)

            # Perform spell checker steps for each word with grammar errors
            for incorrect_word in error_words:
                matched_words = suggest_most_matched_words(incorrect_word)

                print(f"Suggested words for '{incorrect_word}':")
                for index, matched_word in enumerate(matched_words, start=1):
                    print(f"{index}. {matched_word}")

                user_choice = input("Choose a correct word (enter the number) or press Enter to accept the suggestion: ")

                # Validate user input
                if user_choice.strip() and user_choice.isdigit() and 0 <= int(user_choice) <= len(matched_words):
                    # Replace the incorrect word with the user's chosen suggestion or keep the original word
                    if int(user_choice) > 0:
                        input_sentence = input_sentence.replace(incorrect_word, matched_words[int(user_choice) - 1], 1)
                elif user_choice.strip() == '0':
                    # Skip replacing the word
                    print("Word skipped.")
                else:
                    print("Invalid choice or no choice made. Accepting the suggestion.")

            # Correct grammar after spell checker steps
            input_sentence = correct_grammar(input_sentence)
            print("Corrected sentence:", input_sentence)

    else:
        print("Input is not in Urdu.")
