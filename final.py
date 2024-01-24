from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, END, RIGHT, Y , N , S , W , E
from tkinter import messagebox
from fuzzywuzzy import fuzz, process
import langid
import stanza

# Read the word list from the file
with open('urduList.txt', 'r', encoding='utf-8') as file:
    word_list = [line.strip() for line in file]

def remove_punctuation(word):
    # Exclude specific punctuation marks from removal
    exclude_chars = set("؟',،.٫-۔“”‘’[]{}()<>:;?!&") # Add more punctuation marks if needed
    return ''.join(char for char in word if char not in exclude_chars)

def suggest_most_matched_words(incorrect_word, limit=15):
    # Calculate similarity scores for each word in the list
    similarity_scores = process.extract(incorrect_word, word_list, scorer=fuzz.ratio, limit=limit)

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
        return None, None

    # Download and load the Urdu language model from stanza
    stanza.download('ur')
    nlp = stanza.Pipeline('urdu')

    # Process the input sentence using stanza
    doc = nlp(sentence)

    # Check for grammar errors
    errors = []
    corrected_sentence_words = []
    for sentence in doc.sentences:
        for word in sentence.words:
            # Add specific rules for grammar checks
            # Example: Check for incorrect verb forms
            if word.upos == 'VERB' and word.feats and 'VerbForm=Fin' not in word.feats:
                errors.append(word.text)
                # Correct the error in the sentence
                corrected_sentence_words.append(word.lemma)
            else:
                corrected_sentence_words.append(word.text)

    # Generate a corrected sentence
    corrected_sentence = ' '.join(corrected_sentence_words)

    return errors, corrected_sentence

def check_spelling():
    global sentence_entry, suggestions_frame, suggestion_buttons, wrong_words_frame

    # Get the sentence from the entry widget
    sentence = sentence_entry.get()

    # Check if the input is in Urdu
    if is_urdu(sentence):
        # Split the sentence into words
        sentence_words = sentence.split()

        # Initialize a variable to check if all words match
        all_words_match = True

        # Keep track of the indices of incorrect words
        incorrect_word_indices = []

        # Check each word in the sentence
        for i, word in enumerate(sentence_words):
            # Remove punctuation from the word
            clean_word = remove_punctuation(word)

            if clean_word not in word_list:
                all_words_match = False
                incorrect_word_indices.append(i)

        # Update the wrong words and indices in the new Text widget
        update_wrong_words_frame(incorrect_word_indices, sentence_words)

        if all_words_match:
            # If all words are correct, clear the list of suggestions
            clear_suggestion_list()
            corrected_sentence = ' '.join(sentence_words)
            corrected_sentence = correct_grammar(corrected_sentence)
            messagebox.showinfo("Spell Checker", f"Your sentence is correct: {corrected_sentence}")
        else:
            for index in incorrect_word_indices:
                incorrect_word = sentence_words[index]
                matched_words = suggest_most_matched_words(incorrect_word)

                # Update the suggestion buttons dynamically
                update_suggestion_buttons(matched_words, index)
    else:
        messagebox.showwarning("Language Error", "Input is not in Urdu.")

def update_suggestion_buttons(matched_words, index):
    global suggestions_frame, suggestion_buttons

    # Update the suggestion buttons dynamically
    for button in suggestion_buttons:
        button.destroy()

    for i, matched_word in enumerate(matched_words, start=1):
        suggestion_button = Button(suggestions_frame, text=f"Suggestion {i}: {matched_word}",
                                   command=lambda x=matched_word: choose_suggestion(x, index))
        suggestion_button.grid(row=i, column=0, padx=10, pady=5, sticky="w")
        suggestion_buttons.append(suggestion_button)

def choose_suggestion(selected_suggestion, index):
    global sentence_entry

    # Update the sentence in the entry widget with the selected suggestion
    current_sentence = sentence_entry.get()
    sentence_words = current_sentence.split()
    sentence_words[index] = selected_suggestion
    updated_sentence = ' '.join(sentence_words)

    sentence_entry.delete(0, END)
    sentence_entry.insert(0, updated_sentence)

    # Clear the suggestions frame
    suggestions_frame.delete(1.0, END)

    # Re-run the spell check and update suggestions for all incorrect words
    check_spelling()

def run_grammar_checker():
    global sentence_entry

    # Get the sentence from the entry widget
    sentence = sentence_entry.get()

    # Check if the input is in Urdu
    if is_urdu(sentence):
        # Check grammar
        error_words, corrected_sentence = urdu_grammar_checker(sentence)

        if not error_words:
            messagebox.showinfo("Grammar Checker", f"No grammar errors found. The sentence is correct.\nCorrected Sentence: {corrected_sentence}")
        else:
            messagebox.showwarning("Grammar Checker", f"Grammar errors found in the following words: {error_words}\nCorrected Sentence: {corrected_sentence}")
            # Update the entry widget with the corrected sentence
            sentence_entry.delete(0, END)
            sentence_entry.insert(0, corrected_sentence)
    else:
        messagebox.showwarning("Grammar Checker", "Input is not in Urdu.")

def clear_suggestion_list():
    global suggestions_frame, suggestion_buttons

    # Clear the suggestions frame
    suggestions_frame.delete(1.0, END)

    # Destroy suggestion buttons
    for button in suggestion_buttons:
        button.destroy()

    # Clear the suggestion buttons list
    suggestion_buttons = []

def update_wrong_words_frame(incorrect_word_indices, sentence_words):
    global wrong_words_frame

    # Clear the existing content in the wrong words frame
    wrong_words_frame.delete(1.0, END)

    # Display the wrong words and their indices in the new Text widget
    for index in incorrect_word_indices:
        wrong_word = sentence_words[index]
        wrong_words_frame.insert(END, f"Index {index + 1}: {wrong_word}\n")


# Create the main window
root = Tk()
root.title("Urdu Spell and Grammar Checker")

# Create and place widgets
Label(root, text="Enter a sentence in Urdu:").grid(row=0, column=0, padx=10, pady=10)
sentence_entry = Entry(root, width=50)
sentence_entry.grid(row=0, column=1, padx=10, pady=10)

check_button = Button(root, text="Check Spelling", command=check_spelling)
check_button.grid(row=0, column=2, padx=10, pady=10)

grammar_button = Button(root, text="Grammar Checker", command=run_grammar_checker)
grammar_button.grid(row=0, column=3, padx=10, pady=10)

suggestions_frame = Text(root, height=5, width=50, wrap='word')
suggestions_frame.grid(row=1, column=1, padx=10, pady=10)

# Create a new Text widget for wrong words with a scrollbar
wrong_words_frame = Text(root, height=5, width=30, wrap='word')
wrong_words_frame.grid(row=1, column=2, padx=10, pady=10)

# Add a scrollbar to the wrong words frame
scrollbar = Scrollbar(root, command=wrong_words_frame.yview, width=15)

scrollbar.grid(row=1, column=3, sticky=(N, S, W, E))
wrong_words_frame['yscrollcommand'] = scrollbar.set

# Create a list to store suggestion buttons
suggestion_buttons = []

# Start the Tkinter main loop
root.mainloop()
