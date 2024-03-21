from transformers import pipeline

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import spacy

# Load English language model for spaCy
nlp = spacy.load("en_core_web_sm")

# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')

classifier = pipeline("text-classification", model="shahrukhx01/question-vs-statement-classifier")


def determine_question_old(statement_tokens):
    # Check if the first token is a question word
    # question_words = ['who', 'what', 'when', 'where', 'why', 'how', 'which']
    question_words = ["what", "why", "when", "where",
                      "name", "is", "how", "do", "did", "does",
                      "which", "are", "could", "would",
                      "should", "has", "have", "whom", "whose", "don't"]
    is_question = statement_tokens[0] in question_words
    return is_question


def determine_question_ml(statement):
    global classifier
    is_question = classifier(statement)
    return is_question[0]["label"] == 'LABEL_1'


def extract_topic(question, tokens):
    global nlp

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]

    # POS Tagging
    pos_tags = nltk.pos_tag(filtered_tokens)

    # Named Entity Recognition
    doc = nlp(question)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Topic extraction
    topics = []
    for token, pos in pos_tags:
        if pos.startswith('NN') or pos.startswith('VB'):
            topics.append(token)

    return topics, entities


if __name__ == '__main__':
    # Example usage
    question1 = "can you please tell me whether I packed my bags yet."
    question2 = "did I pack my bag yet."
    question3 = "what are the impacts of climate change on agriculture?"
    question4 = "i like packing my bags."

    questions = [question1, question2, question3, question4]

    for statement in questions:
        print("Statement:", statement)
        # Tokenize the question
        tokens = word_tokenize(statement.lower())

        print("non ML:", determine_question_old(tokens))
        print("    ML:", determine_question_ml(statement))

        topic, entities = extract_topic(statement, tokens)
        print("Topic:", topic)
        print("Entities:", entities)
