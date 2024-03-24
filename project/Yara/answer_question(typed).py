from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

from transformers import pipeline
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import spacy

from datetime import datetime
from database_functions import create_connection, get_all_list_keywords, get_steps_for_list

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

    # yield session.call("rie.dialogue.stt.stream")
    last_sentence = input("Give clarifying sentence:")
    while last_sentence == "":
        last_sentence = input("Give clarifying sentence: ")
        yield sleep(2)

    # yield session.call("rie.dialogue.stt.close")

    print("Previous sentence:", last_sentence)
    # TODO: make sure whether replace functions are needed
    for word in last_sentence.replace("?", "").replace(".", "").split(" "):
        for idx, keyword in keywords:
            if word in keyword:
                return idx
    last_sentence = ""
    return -1


@inlineCallbacks
def get_question_topic(session, details, list_name, list):
    # check what part of the list is asked about
    print(list)
    keywords = []
    for idx in range(len(list)):
        step = list[idx]
        keyword = step[2].split(",")
        keywords.append((idx, keyword))
    print(keywords)
    # keywords = [[x, c] for x, a, b, c in list]
    for topic in question_topics:
        for idx, keyword in keywords:
            if topic in keyword:
                return idx

    answers = {"yes": ["yes", "sure", "yeah"], "no": ["no", "nope", "definitely not", "not now"]}
    # answer = yield session.call("rie.dialogue.ask", question="Do you want to talk about " + topic + "?", answers=answers)
    answer = input("Do you want to talk about the " + list_name + "?")
    print("A: ", answer)
    if answer == "no":
        return -1

    # yield session.call("rie.dialogue.say_animated", text="I'm sorry, I don't know what you want to talk about regarding " + topic + ".")
    print("I'm sorry, I don't know what you want to talk about regarding this.")

    # answer = yield session.call("rie.dialogue.ask", question="Is there something specific that you want to know?", answers=answers)
    answer = input("Is there something specific that you want to know?")
    print("A: ", answer)
    if answer == "no":
        return -2

    # yield session.call("rie.dialogue.say_animated", text="Okay, so what do you want to know?")
    print("Okay, so what do you want to know about the " + list_name + "?")

    tries = 0
    while tries < 4:
        idx = yield get_specific_question_topic(session, details, keywords)
        print("IDX:", idx)
        if idx != -1:
            return idx
        tries += 1

    return -1


def order_steps_in_list(list, date):
    completed, unfinished, early, info = [], [], [], []
    for step in list:
        name = step[0]
        status = step[1]
        begin_date = step[3]
        if status == 3:
            info.append(name)
        elif status == 1:
            completed.append(name)
        elif status == 0:
            if date < begin_date:
                early.append(name)
            else:
                unfinished.append(name)
    return completed, unfinished, early, info


@inlineCallbacks
def answer_keyword_question(session, details, list_name, list_id, conn, date):
    global question_topics
    list = get_steps_for_list(conn, list_id)
    if not list:
        # yield session.call("rie.dialogue.say_animated", text="I'm sorry, I don't know anything about this.")
        print("I'm sorry, I don't know anything about this.")
        return False

    list_part = yield get_question_topic(session, details, list_name, list)
    if list_part == -1:  # User doesn't want to talk about this topic
        return False
    elif list_part == -2:
        completed, unfinished, early, info = order_steps_in_list(list, date)
        if len(info) == 1:
            print("I know that " + info[0] + ".")
        elif len(info) > 1:
            print("I have the following information about the " + list_name + ":")
            for step in info:
                print(step)
        if len(completed) == 1:
            print("You did already " + completed[0] + ".")
        elif len(completed) > 1:
            print("You have already done the following:")
            for step in completed:
                print(step)
        if len(unfinished) == 1:
            print("You could still " + unfinished[0] + ".")
        elif len(unfinished) > 1:
            print("There are some things that you can still do:")
            for step in unfinished:
                print(step)
        if len(early) == 1:
            print("It is a bit too early to " + early[0] + ".")
        elif len(early) > 1:
            print("It's a bit too early to:")
            for step in early:
                print(step)
        return True

    # Focus on the specific part that the question is about
    question_item = list[list_part]
    print("qi:", question_item)

    if question_item[1] == 3:
        # yield session.call("rie.dialogue.say_animated", text=question_item[1])
        print(question_item[0])
    elif question_item[1] == 1:
        # yield session.call("rie.dialogue.say_animated", text="You are done with " + question_item[1])
        print("You are done with " + question_item[0])
    elif question_item[1] == 0:
        # yield session.call("rie.dialogue.say_animated", text="You could " + question_item[1] + " As it isn't done yet.")
        print(question_item[3], date, question_item[3] > date)
        if question_item[3] > date:
            print("It is a bit too early to " + question_item[0] + ". Maybe you can do it later?")
        else:
            print("You could " + question_item[0] + " now. As it isn't done yet.")

    # TODO: reset the robot to normal position?
    return True


def prepare_keywords(conn, date):
    keyword_list = get_all_list_keywords(conn, date)
    new_list = []

    for id, name, keywords in keyword_list:
        keywords = keywords.split(",")
        new_list.append((id, name, keywords))

    print("Current keywords:", new_list)
    return new_list


@inlineCallbacks
def answer_question(session, details, conn, date):
    global finish_dialogue, question, question_topics

    # prepare the keywords
    keyword_list = yield prepare_keywords(conn, date)

    # loop while user did not say goodbye or bye
    question = input("Give question: ")
    while question != "bye":
        if question != "":
            # yield session.call("rie.dialogue.stt.close")

            # Listen during conversation (LLM?) to figure out whether user wants to know/do something from a list
            print("Start checking question")
            tokens = word_tokenize(question.lower())

            question_topics, entities = extract_topic(question, tokens)
            question = ""
            is_answered = False
            for topic in question_topics:
                if is_answered:
                     break
                for id, name, keywords in keyword_list:
                    if topic in keywords:
                        print("Talk about topic!")
                        is_answered = yield answer_keyword_question(session, details, name, id, conn, date)
                        break
            print("After question part")

            # yield session.call("rie.dialogue.stt.stream")
        question = input("Give question: ")

        # yield sleep(0.5)


@inlineCallbacks
def main(session, details):
    conn = create_connection(r"db\pythonsqlite.db")
    date = str(datetime.now())[:10]
    date = "2024-03-24"
    yield answer_question(session, details, conn, date)


if __name__ == "__main__":
    main(0, 0)
