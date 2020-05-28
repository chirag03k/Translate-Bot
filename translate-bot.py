import praw
from googletrans import Translator
import iso639

# Connect to Reddit
pass_file = open("password.txt")
pw = pass_file.read()

id_file = open("id.txt")
id = pass_file.read()

secret = open("secret.txt")
secret = pass_file.read()

reddit = praw.Reddit(client_id=id,
                     client_secret=secret,
                     username="gtranslatebot",
                     password=pw,
                     user_agent="google translate bot by /u/chirag03k")


subreddits = reddit.subreddit("all")

# Do the Bot Stuff
keyphrase = "!translate"

translator = Translator()

for comment in subreddits.stream.comments():
    comment_text = comment.body
    if keyphrase in comment_text:
        try:
            to_translate = comment.parent().body
            print(to_translate)
        except:
            to_translate = None
        comment_tokens = comment_text.split()

        # Parsing
        if "from" in comment_text:
            try:
                from_lang = comment_tokens[comment_tokens.index("from") + 1]
                from_lang_code = iso639.to_iso639_1(from_lang)
            except:
                from_lang_code = "Failure"
        else:
            from_lang_code = None
        if "to" in comment_text:
            try:
                to_lang = comment_tokens[comment_tokens.index("to") + 1]
                to_lang_code = iso639.to_iso639_1(to_lang)
            except:
                to_lang_code = "Failure"
        else:
            to_lang_code = "en"

        # Generating Output

        if from_lang_code is "Failure":
            output = "I don't know how to translate from " + from_lang
        elif to_lang_code is "Failure":
            output = "I don't know how to translate into  " + to_lang
        elif to_translate is None:
            output = "I couldn't load the parent comment"
        elif from_lang_code is None:
            translation = translator.translate(to_translate, dest=to_lang_code)
            output = 'Translated from ' + iso639.to_name(translation.src) + '''.
            ''' + translation.text
        else:
            translation = translator.translate(to_translate, src=from_lang_code, dest=to_lang_code)
            output = 'Transated from ' + iso639.to_name(translation.src) + 'to' + iso639.to_name(translation.dest) + '''.
            ''' + translation.text

        #Replying
        comment.reply(output)
        print("replied " + output)
