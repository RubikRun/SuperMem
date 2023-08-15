from interface.cli import CLI
from user import User
from data.database import Database
from dictionary import Dictionary
from word import Word
from random import shuffle, randint

CONFIDENCE_DELTA = 1

# A class for a home page of a user
# Each user has their own home page with their languages and words
class HomePage:
    # Creates a home page for the given user
    def __init__(self, user: User):
        self.user = user

    # Runs the home page
    def run(self, database: Database) -> None:
        while True:
            # Print home page message and options for what to do
            CLI.print_big("Home Page of {}".format(self.user.username))
            # User chooses an option
            option = CLI.ask_option_num(
                "Choose an option, or type \"exit\":", [
                "Start learning a new language",
                "What languages am I learning?",
                "Learn a new word",
                "Do a word test"
            ])
            # If option is None we need to exit
            if option is None:
                return
            elif option == 1:
                self.start_learning_new_language(database)
            elif option == 2:
                self.show_active_languages()
            elif option == 3:
                self.learn_new_word(database)
            elif option == 4:
                self.do_word_test()

    # Asks a user what language they want to start learning, gives them a list of only the languages that are available for them.
    # Adds the chosen language to the user's active languages
    def start_learning_new_language(self, database: Database) -> None:
        available_languages = self.get_learnable_languages_with_dict(database)
        # Ask for the language
        language = CLI.ask_option("What language do you want to start learning?", available_languages)
        if language is None:
            return
        # Add the new language to user's active languages
        self.user.active_languages.append(language)
        # Add a new count for active words of the new language, beginning at 0
        self.user.active_words.append(0)
        # Setup user's dictionaries again to handle the new language
        database.setup_user_dictionaries(self.user)
        # Setup user's confidences again to handle the new language
        database.setup_user_confidences(self.user)
        CLI.print("Okay. {} added to your active languages.\n".format(language))

    # Returns a list with languages that the user can learn and that have a dictionary with the user's main language.
    def get_learnable_languages_with_dict(self, database: Database) -> list[str]:
        languages = database.get_all_languages()
        # User cannot be learning their own language or a language they're already learning,
        # so remove those from the list of languages
        learnable_languages = languages.copy()
        learnable_languages.remove(self.user.main_language)
        for language in self.user.active_languages:
            learnable_languages.remove(language)
        # Also remove languages that don't have a dictionary with the user's main language
        learnable_languages_with_dict = []
        for language in learnable_languages:
            for dictionary in database.dictionaries:
                if (dictionary.language_a == self.user.main_language and dictionary.language_b == language)\
                or (dictionary.language_a == language and dictionary.language_b == self.user.main_language):
                    learnable_languages_with_dict.append(language)
                    break
        # Return the remaining languages
        return learnable_languages_with_dict

    # Shows the user their active languages.
    def show_active_languages(self) -> None:
        if not self.user.active_languages:
            CLI.print("You are not learning any languages.\n")
            return
        languages_str = self.user.active_languages[0]
        for language in self.user.active_languages[1:]:
            languages_str += ", " + language
        CLI.print("You are learning {}\n".format(languages_str))

    # Lets user learn a new word in one of their active languages.
    # The new word is the next word after user's active words in the chosen language.
    # After showing the word to the user, user's active words are increased by one for the chosen language
    def learn_new_word(self, database: Database) -> None:
        # Choose a language
        language_idx = self.choose_active_language()
        if language_idx is None:
            CLI.print("You have no active languages. Start learning a language first.\n")
            return
        language = self.user.active_languages[language_idx]
        # Retrieve the next word from the dictionary of the chosen language
        word = self.user.dictionaries[language_idx].words[self.user.active_words[language_idx]]
        # Increase the count of active words for the chosen language
        self.user.active_words[language_idx] += 1
        # Setup user's confidences again to handle the change of active words
        database.setup_user_confidences(self.user)
        # Show the new word to the user
        CLI.print("Okay, here's a new word in {}:\n".format(language))
        CLI.print_clearly("{} <-----means-----> {}".format(word.term_a, word.term_b))

    # Lets user choose one of their active languages, or if it's just a single language, directly returns it.
    # Returns the index of the chosen language (0-based)
    def choose_active_language(self) -> int:
        # If active languages are 0 or 1, there's nothing to choose
        if not self.user.active_languages:
            return None
        if len(self.user.active_languages) == 1:
            return 0
        # Ask for an active language
        language_num = CLI.ask_option_num("Choose one of the languages that you're learning.", self.user.active_languages)
        return language_num - 1

    def do_word_test(self) -> None:
        # Choose a language
        language_idx = self.choose_active_language()
        if language_idx is None:
            CLI.print("You have no active languages. Start learning a language first.\n")
            return
        language = self.user.active_languages[language_idx]
        # Get the number of words that user knows in this language
        words_count = self.user.active_words[language_idx]
        if words_count < 1:
            CLI.print("You don't know any words in this language. Learn some words first.\n")
            return
        # Get the dictionary between that language and user's main language
        dictionary = self.user.dictionaries[language_idx]
        # Check the direction of the dictionary, whether it's from known to unknown or the other way
        dict_from_kn = False
        if dictionary.language_a == self.user.main_language:
            dict_from_kn = True
        # Choose the direction of the test, whether to be from known to unknown or vice versa
        from_kn = CLI.ask_option_num(
            "Choose direction of the test:", [
            "Questions in {}, answers in {}".format(language, self.user.main_language),
            "Questions in {}, answers in {}".format(self.user.main_language, language)
        ]) == 2
        # Check whether dictionary languages should be swapped
        should_swap_dict = (from_kn != dict_from_kn)
        # Ask user for mode of ordering the words
        order_mode = CLI.ask_option_num(
            "Choose mode:", [
            "Order words by their level (ascending)",
            "Order words by their level (descending)",
            "Order words by your confidence (ascending)",
            "Order words by your confidence (descending)",
            "Shuffle words",
            "Order words by your confidence, but with some shuffling (ascending)",
            "Order words by your confidence, but with some shuffling (descending)"
        ])
        # Get word indices in the correct order
        word_idxs = self.get_words_ordered_in_mode(dictionary.words[:words_count], order_mode, language_idx)
        # Traverse the words that user knows
        for word_idx in word_idxs:
            word = dictionary.words[word_idx]
            # Retrieve the term that will be asked and the term that should be answered, based on the direction of the test
            asked_term = word.term_a
            real_answer = word.term_b
            if should_swap_dict:
                asked_term = word.term_b
                real_answer = word.term_a
            # Determine the question, based on the direction of the test
            question = "How do you say \"{}\" in {}?\n".format(asked_term, language)
            if from_kn == 0:
                question = "What's \"{}\" in {}?\n".format(asked_term, self.user.main_language)
            # Ask the question
            CLI.print(question)
            # Get user's answer
            answer = CLI.ask_for("Answer: ")
            # Check if it matches the real answer
            if answer == real_answer:
                if self.user.confidences[language_idx][word_idx] <= 100 - CONFIDENCE_DELTA:
                    self.user.confidences[language_idx][word_idx] += CONFIDENCE_DELTA
                CLI.print("Correct!    (confidence: {})\n".format(self.user.confidences[language_idx][word_idx]))
            else:
                if self.user.confidences[language_idx][word_idx] >= CONFIDENCE_DELTA:
                    self.user.confidences[language_idx][word_idx] -= CONFIDENCE_DELTA
                CLI.print("No. It's {}    (confidence: {})\n".format(real_answer, self.user.confidences[language_idx][word_idx]))

    # Orders words in the given mode and returns a list of indices to the words in the original list. Does not modify the original list
    def get_words_ordered_in_mode(self, words: list[Word], mode: int, lang_idx: int) -> list[int]:
        word_idxs = None
        if mode == 1:
            word_idxs = [tup[0] for tup in sorted(enumerate(words), key=lambda x:x[1].level)]
        elif mode == 2:
            word_idxs = [tup[0] for tup in sorted(enumerate(words), key=lambda x:x[1].level, reverse = True)]
        elif mode == 3:
            # Workaround for the case of same confidences:
            # In this case the second element of the tuple is compared when sorting,
            # and the second element is of type Word so they cannot be compared.
            # We just need something that can be compared and won't be the same there
            # and the word will be at index 2
            dummy_list = list(range(len(words)))
            word_idxs = list(tup[2].index for tup in sorted(zip(self.user.confidences[lang_idx], dummy_list, words)))
        elif mode == 4:
            dummy_list = list(range(len(words)))
            word_idxs = list(tup[2].index for tup in sorted(zip(self.user.confidences[lang_idx], dummy_list, words), reverse = True))
        elif mode == 5:
            word_idxs = list(range(len(words)))
            shuffle(word_idxs)
        # NOT TESTED
        elif mode == 6:
            word_idxs = []
            how_much_prob = 30

            confs = [x * how_much_prob for x in self.user.confidences[lang_idx]]
            confs_sum = sum(confs)

            word_is_used = [False] * len(words)
            words_used = 0
            remaining_length = confs_sum
            weat = 0
            while words_used < len(words):
                walk = randint(0, remaining_length)
                while walk > 0:
                    walk -= confs[weat]
                    weat = (weat + 1) % len(words)
                    while word_is_used[weat]:
                        weat = (weat + 1) % len(words)
                word_is_used[weat] = True
                word_idxs.append(weat)
                remaining_length -= confs[weat]
                words_used += 1
        # NOT TESTED
        elif mode == 7:
            word_idxs = []
            how_much_prob = 30

            confs = [(100 - x) * how_much_prob for x in self.user.confidences[lang_idx]]
            confs_sum = sum(confs)

            word_is_used = [False] * len(words)
            words_used = 0
            remaining_length = confs_sum
            weat = 0
            while words_used < len(words):
                walk = randint(0, remaining_length)
                while walk > 0:
                    walk -= confs[weat]
                    weat = (weat + 1) % len(words)
                    while word_is_used[weat]:
                        weat = (weat + 1) % len(words)
                word_is_used[weat] = True
                word_idxs.append(weat)
                remaining_length -= confs[weat]
                words_used += 1

        return word_idxs