import langid
import stanza

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
    input_sentence = input("Enter a sentence: ")

    # Check if the input is in Urdu
    if is_urdu(input_sentence):
        # Check grammar
        error_words = urdu_grammar_checker(input_sentence)

        if not error_words:
            print("No grammar errors found. The sentence is correct.")
        else:
            print("Grammar errors found in the following words:", error_words)
    else:
        print("Input is not in Urdu.")
