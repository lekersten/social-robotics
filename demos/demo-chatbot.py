from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot("Alpha Mini")

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train based on the english conversations corpus
trainer.train("chatterbot.corpus.english.conversations")

exit_conditions = (":q", "quit", "exit")

while True:
    query = input("> ")
    if query in exit_conditions:
        break
    else:
        print(f"🪴 {chatbot.get_response(query)}")


# Train based on the english corpus
#trainer.train("chatterbot.corpus.english")

# Train based on english greetings corpus
#trainer.train("chatterbot.corpus.english.greetings")

