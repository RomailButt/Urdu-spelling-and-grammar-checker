from fuzzywuzzy import fuzz, process
import langid
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

# Get a sentence from the user
sentence = input("Enter a sentence in Urdu: ")

while True:
    # Split the sentence into words
    sentence_words = sentence.split()

    # Initialize a variable to check if all words match
    all_words_match = True

    # Keep track of the index of the incorrect word
    incorrect_word_index = -1

    # Check each word in the sentence
    for i, word in enumerate(sentence_words):
        # Remove punctuation from the word
        clean_word = remove_punctuation(word)

        if clean_word not in word_list:
            print(f"Word not matched: {word}")
            all_words_match = False
            incorrect_word_index = i

    if all_words_match:
        corrected_sentence = ' '.join(sentence_words)
        corrected_sentence = correct_grammar(corrected_sentence)
        print("Your sentence is correct:", corrected_sentence)
        break
    else:
        incorrect_word = sentence_words[incorrect_word_index]
        matched_words = suggest_most_matched_words(incorrect_word)

        print(f"Suggested words for '{incorrect_word}':")
        for index, matched_word in enumerate(matched_words, start=1):
            print(f"{index}. {matched_word}")

        user_choice = input("Choose a correct word (enter the number) or press Enter to accept the suggestion: ")

        # Validate user input
        if user_choice.strip() and user_choice.isdigit() and 0 <= int(user_choice) <= len(matched_words):
            # Replace the incorrect word with the user's chosen suggestion or keep the original word
            if int(user_choice) > 0:
                sentence_words[incorrect_word_index] = matched_words[int(user_choice) - 1]
        elif user_choice.strip() == '0':
            # Skip replacing the word
            print("Word skipped.")
        else:
            print("Invalid choice or no choice made. Accepting the suggestion.")

        # Update the sentence with the corrected word or keep the original word
        sentence = ' '.join(sentence_words)
