from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

from transformers import pipeline
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from datetime import datetime
from database_functions import create_connection, get_all_list_keywords, get_steps_for_list

classifier = pipeline("text-classification", model="shahrukhx01/question-vs-statement-classifier")

finish_dialogue = False
question = ""
question_topics = []
last_sentence = ""


def determine_if_question(statement):
    global classifier
    is_question = classifier(statement)
    return is_question[0]["label"] == 'LABEL_1'


def extract_topic(tokens):
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]

    # POS Tagging
    pos_tags = nltk.pos_tag(filtered_tokens)

    # Topic extraction
    topics = []
    for token, pos in pos_tags:
        if pos.startswith('NN') or pos.startswith('VB'):
            topics.append(token)

    print("topics: ", topics)
    return topics


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
    global last_sentence, question

    yield session.call("rie.dialogue.stt.stream")

    while last_sentence == "":
        print("Last sentence:", last_sentence)
        yield sleep(2)

    yield session.call("rie.dialogue.stt.close")

    # print("q:", question)
    question = ""

    print("Previous sentence:", last_sentence)
    for word in last_sentence.split(" "):
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

    for word in question.split(" "):
        for idx, keyword in keywords:
            if word in keyword:
                return idx

    answers = {"yes": ["yes", "sure", "yeah"], "no": ["no", "nope", "definitely not", "not now"]}
    answer = yield session.call("rie.dialogue.ask", question="Do you want to talk about the " + list_name + "?",
                                answers=answers)
    # print("A: ", answer)
    if answer == "no":
        return -1

    yield session.call("rie.dialogue.say_animated",
                       text="I'm sorry, I don't know what you want to talk about regarding this.")

    answer = yield session.call("rie.dialogue.ask", question="Is there something specific that you want to know?",
                                answers=answers)
    # print("A: ", answer)
    if answer == "no":
        return -2
    
    yield session.call("rie.dialogue.say_animated", text="Okay, so what do you want to know about the " + list_name + "?")

    tries = 0
    while tries < 4:
        # print("New try")
        idx = yield get_specific_question_topic(session, details, keywords)
        # print("IDX:", idx)
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
        yield session.call("rie.dialogue.say_animated", text="I'm sorry, I don't know anything about this.")
        return False

    list_part = yield get_question_topic(session, details, list_name, list)
    if list_part == -1:  # User doesn't want to talk about this topic
        return False
    elif list_part == -2:  # user wants to know everything
        completed, unfinished, early, info = yield order_steps_in_list(list, date)
        if len(info) == 1:
            yield session.call("rie.dialogue.say_animated", text="I know that " + info[0] + ".")
        elif len(info) > 1:
            yield session.call("rie.dialogue.say_animated", text="I have the following information about the " + list_name + ":")
            for step in info:
                yield session.call("rie.dialogue.say_animated", text=step)
        if len(completed) == 1:
            yield session.call("rie.dialogue.say_animated", text="You did already " + completed[0] + ".")
        elif len(completed) > 1:
            yield session.call("rie.dialogue.say_animated", text="You have already done the following:")
            for step in completed:
                yield session.call("rie.dialogue.say_animated", text=step)
        if len(unfinished) == 1:
            yield session.call("rie.dialogue.say_animated", text="You could still " + unfinished[0] + ".")
        elif len(unfinished) > 1:
            yield session.call("rie.dialogue.say_animated", text="There are some things that you can still do:")
            for step in unfinished:
                yield session.call("rie.dialogue.say_animated", text=step)
        if len(early) == 1:
            yield session.call("rie.dialogue.say_animated", text="It is a bit too early to " + early[0] + ".")
        elif len(early) > 1:
            yield session.call("rie.dialogue.say_animated", text="It's a bit too early to:")
            for step in early:
                yield session.call("rie.dialogue.say_animated", text=step)
        return True

    # Focus on the specific part that the question is about
    question_item = list[list_part]
    print("response:", question_item[0])

    if question_item[1] == 3:
        yield session.call("rie.dialogue.say_animated", text=question_item[0])
    elif question_item[1] == 1:
        yield session.call("rie.dialogue.say_animated", text="You are done with "+question_item[0] + ".")
    elif question_item[1] == 0:
        if question_item[3] > date:
            yield session.call("rie.dialogue.say_animated",
                               text="It is a bit too early to " + question_item[0] + ". Maybe you can do it later?")
        else:
            yield session.call("rie.dialogue.say_animated",
                               text="You could " + question_item[0] + " now. As it isn't done yet.")

    # reset the robot to a neutral position
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    session.call("rom.actuator.motor.write",
                 frames=[{"time": 1000, "data": {"body.head.pitch": 0, "body.head.yaw": 0}}],
                 force=True
                 )

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
    # set language to English (use 'nl' for Dutch)
    yield session.call("rie.dialogue.config.language", lang="en")

    # subscribes the asr function with the input stt stream
    yield session.subscribe(asr, "rie.dialogue.stt.stream")
    # calls the stream. From here, the robot prints each 'final' sentence
    yield session.call("rie.dialogue.stt.stream")

    # prepare the keywords
    keyword_list = yield prepare_keywords(conn, date)

    # loop while user did not say goodbye or bye
    while not finish_dialogue:
        if question != "":
            yield session.call("rie.dialogue.stt.close")

            # Listen during conversation (LLM?) to figure out whether user wants to know/do something from a list
            print("Start checking question")
            tokens = word_tokenize(question.lower())

            question_topics = extract_topic(tokens)
            is_answered = False
            for topic in question_topics:
                if is_answered:
                     break
                for id, name, keywords in keyword_list:
                    if topic in keywords:
                        is_answered = yield answer_keyword_question(session, details, name, id, conn, date)
                        break

            question = ""

            if not is_answered:
                yield session.call("rie.dialogue.say_animated", text="Sorry, I don't know anything about that.")
            print("After question part")

            yield session.call("rie.dialogue.stt.stream")

        yield sleep(0.5)

    yield session.call("rie.dialogue.stt.close")


@inlineCallbacks
def main(session, details):
    yield session.call("rie.dialogue.config.language", lang="en")

    conn = create_connection(r"db\pythonsqlite.db")
    date = str(datetime.now())[:10]
    date = "2024-03-28"     # Both vacation and easter visit list
    # date = "2024-03-24"     # Too early to pack bags for vacation
    yield session.call("rie.dialogue.say_animated", text="Robot started!")
    yield answer_question(session, details, conn, date)
    session.leave()


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.66014f75a6c4715863c5a3f4",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
