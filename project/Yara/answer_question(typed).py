from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

from transformers import pipeline
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import spacy

from datetime import datetime
from database_functions import create_connection, get_all_list_keywords

# Load English language model for spaCy
nlp = spacy.load("en_core_web_sm")
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')

classifier = pipeline("text-classification", model="shahrukhx01/question-vs-statement-classifier")

finish_dialogue = False
question = ""
question_topics = []
last_sentence = ""


def determine_if_question(statement):
    global classifier
    is_question = classifier(statement)
    return is_question[0]["label"] == 'LABEL_1'


def extract_topic(question, tokens):
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

    print("topic: ", topics, entities)
    return topics, entities


def asr(frames):
    global finish_dialogue, question, last_sentence
    if frames['data']['body']['final']:
        dialogue = frames["data"]["body"]["text"]
        last_sentence = dialogue
        print("dialogue:", dialogue)
        if question == "" and determine_if_question(dialogue):
            question = dialogue

        if frames["data"]["body"]["text"] == "bye" or \
                frames["data"]["body"]["text"] == "goodbye":
            finish_dialogue = True


@inlineCallbacks
def get_specific_question_topic(session, details, keywords):
    global last_sentence

    yield session.call("rie.dialogue.stt.stream")

    while last_sentence == "":
        yield sleep(2)

    yield session.call("rie.dialogue.stt.stream")

    print("Previous sentence:", last_sentence)
    for word in last_sentence.split(" "):
        for idx, keyword in keywords:
            if word in keyword:
                return idx
    last_sentence = ""
    return 0


@inlineCallbacks
def get_question_topic(session, details, topic, list):
    # TODO: keywords can be in question but not in topics, solve? or ask clarifying question and solve there?
    # check what part of the list is asked about
    keywords = [[x, c] for x, a, b, c in list]
    for topic in question_topics:
        for idx, keyword in keywords:
            if topic in keyword:
                return idx

    # TODO: ask whether person wants to talk about the topic
    answers = {"yes": ["yes", "sure", "yeah"], "no": ["no", "nope", "definitely not", "not now"]}
    answer = yield session.call("rie.dialogue.ask", question="Do you want to talk about " + topic + "?",
                                answers=answers)
    print("A: ", answer)
    if answer == "no":
        return 0

    yield session.call("rie.dialogue.say_animated",
                       text="I'm sorry, I don't know what you want to talk about regarding " + topic + ".")

    answer = yield session.call("rie.dialogue.ask", question="Is there something specific that you want to know?",
                                answers=answers)
    print("A: ", answer)
    if answer == "no":
        # TODO: make sure to ask about whether want to know everything / all that is done / all that should still be done
        return -1

    yield session.call("rie.dialogue.say_animated", text="Okay, so what do you want to know?")

    tries = 0
    while tries < 4:
        idx = yield get_specific_question_topic(session, details, keywords)
        print("IDX:", idx)
        if idx != 0:
            return idx
        tries += 1

        # TODO: need to reopen/close dialogue stream to get response
        # TODO: ask clarifying question if no list part determined yet (What do you want to know about [topic]?)
        # TODO: add option for asking about everything that is done or needs to be done

    return 0


@inlineCallbacks
def answer_keyword_question(session, details, keyword, list_id):
    global question_topics
    # TODO: Get list from database (whatever I use for that)
    if list_id == 1:
        list = [["Prepare the batter", True], ["Put the cake in the oven", False],
                ["Take the cake out of the oven", False]]
    elif list_id == 2:
        list = [[1, "Pack your bags.", True, ["bag", "bags", "luggage", "suitcase"]],
                [2, "Print your travel info.", False, ["print"]],
                [3, "You will leave on the 5th of April", "INFO", ["leave", "april"]]]
    else:
        yield session.call("rie.dialogue.say_animated", text="I'm sorry, I don't know anything about this.")
        return

    list_part = yield get_question_topic(session, details, keyword, list)
    if list_part == 0:  # User doesn't want to talk about this topic
        return
    elif list_part == -1:
        return
        # TODO: is option to ask about everything/all done/all not done
        # if len(completed_items) == 0:
        #     yield session.call("rie.dialogue.say_animated", text="Nothing from this list is done yet. Do you want to start now?")
        # elif len(completed_items) == len(list):
        #     yield session.call("rie.dialogue.say_animated", text="Everything is already done for this! Do you want me to repeat every step?")

    # Focus on the specific part that the question is about
    question_item = list[list_part - 1]

    if question_item[2] == "INFO":
        yield session.call("rie.dialogue.say_animated", text=question_item[1])

    if question_item[2]:
        yield session.call("rie.dialogue.say_animated", text="You are done with " + question_item[1])
    else:
        yield session.call("rie.dialogue.say_animated", text="You could " + question_item[1] + " As it isn't done yet.")

    # TODO: reset the robot to normal position


def prepare_keywords(conn, date):
    keyword_list = get_all_list_keywords(conn, date)
    new_list = []

    for id, keywords in keyword_list:
        keywords = keywords.split(",")
        new_list.append((id, keywords))

    print(new_list)
    return new_list


@inlineCallbacks
def answer_question(session, details, conn, date):
    global finish_dialogue, question, question_topics

    # prepare the keywords
    keyword_list = yield prepare_keywords(conn, date)

    # loop while user did not say goodbye or bye
    question = input("Give question:")
    while question != "bye":
        if question != "":
            yield session.call("rie.dialogue.stt.close")

            # Listen during conversation (LLM?) to figure out whether user wants to know/do something from a list
            print("Start checking question")
            tokens = word_tokenize(question.lower())

            question_topics, entities = extract_topic(question, tokens)
            question = ""
            for topic in question_topics:
                for id, keywords in keyword_list:
                    if topic in keywords:
                        yield answer_keyword_question(session, details, topic, id)
                        break
            print("After question part")

            # yield session.call("rie.dialogue.stt.stream")

        yield sleep(0.5)
        question = input("Give question:")



@inlineCallbacks
def main(session, details):
    conn = create_connection(r"db\pythonsqlite.db")
    date = str(datetime.now())[:10]
    yield answer_question(session, details, conn, date)


if __name__ == "__main__":
    main()
