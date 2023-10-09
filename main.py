import tkinter as tk
import nltk
from nltk import bigrams, FreqDist
from nltk.probability import ConditionalFreqDist
import os
from tkinter import ttk
from nltk.tokenize import word_tokenize
import re
import numbers
import Levenshtein
from tkinter import scrolledtext

root = tk.Tk()

file_path = "C:/Users/User/PycharmProjects/NLP_Project/dictionary/english_words_479k.txt"
file = open(file_path, 'r', encoding='utf-8', errors='ignore')

word_list = set()

for x in file:
    # here we got to tokenize and preprocessing the word dictionary
    tokens = word_tokenize(x)
    normalized_tokens = [token.lower() for token in tokens if re.match('^[a-zA-Z\']+$|[.,;]$', token)]
    word_list.update(normalized_tokens)

# Check is there any numerical value inside
list2 = [x for x in word_list if isinstance(x, numbers.Number)]

train_folder_path = 'C:/Users/User/Downloads/NLP_Group3/NLP_Group3/Corpus'
train_file_path = []
bigrams_list = []

for train_file in os.listdir(train_folder_path):
    if os.path.isfile(os.path.join(train_folder_path, train_file)):
        file_path = os.path.join(train_folder_path, train_file).replace('\\', '/')
        train_file_path.append(file_path)

word_list_2 = set()  # used to store those word that are not in the word dictionary before

for file_path in train_file_path:
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        training_file = file.read()

    word_tokens = word_tokenize(training_file)
    word_normalized_token = [token.lower() for token in word_tokens if re.match('^[a-zA-Z\']+$|[.,;]$', token)]

    # print(word_normalized_token)
    word_list_2.update(word_normalized_token)
    bigrams_list.extend(list(bigrams(word_normalized_token)))

# print(len(word_list))
# print(len(word_list_2))

own_dict_bigrams = list(bigrams(word_list))
# print(len(bigrams_list))
bigrams_list.extend(own_dict_bigrams)
word_list.update(word_list_2)
# print(len(bigrams_list))
bigrams_freq = ConditionalFreqDist(bigrams_list)
# print(bigrams_list)
freq_dist = FreqDist(bigrams_list)
# print(bigrams_freq)

class SpellingChecker():
    def OtherTextWidget(self, string):
        print("Key Press Phase:", string)

    # Solution - Step 1. toggle full flag
    global full  # (update)
    full = False

    # Solution - Step 4. profit
    def AfterRestrict(self, e=None):  # (update)
        global full
        if True == full:
            self.OtherTextWidget(e.widget.get("1.0", "1.5"))
            print("Key Release Phase:", e.widget.get("1.0", "1.5"))

    # Solution - Step 3. limit input
    def Restrict(self, e=None):
        global full  # (update)
        string = e.widget.get("1.0", "end-1c")
        if 499 <= len(string):
            e.widget.delete('1.499', "end-1c")
            full = True  # (update)
        else:  # (update)
            full = False

    # Here we update for chac count and word count and also restrict the char limit
    def update_char_count(self, e=None):
        current_text = self.input_text_widget.get("1.0", "end-1c")
        current_text_char = current_text.replace(' ', '').replace('\n', '')
        self.char_count.set(f"Character Count: {len(current_text_char)}/500")

        tokens = re.split(r'\s+', current_text)
        non_empty_words = [token for token in tokens if token]  # Count non-empty tokens
        self.word_count.set(f"Word Count: {len(non_empty_words)}")

        # Here we use to restrict those use copy and paste that more than 500 word
        global full  # (update)
        string = e.widget.get("1.0", "end-1c")
        if 499 <= len(string):
            e.widget.delete('1.500', "end-1c")
            full = True  # (update)
        else:  # (update)
            full = False

    # def printInput():
    #     inp = input_text_widget.get(1.0, "end-1c")
    #     get_inp_arr = TextBlob(inp).words
    #     print(get_inp_arr)
    #     lbl.config(text = "Provided Input: "+inp)

    # Bigram the input text
    user_input_bigram = []

    # use to store the found word and store where it is placed in the user input.
    result_dict = {}

    # this is to store all the word where user enter
    text_dict = {}

    # to store the clickable text to prompt a new window
    clickable_text = []

    # use to store those real word error (which mean spelling correct but bigram wrong)
    real_word_list = []

    # use for show the pop out window with the word location
    clickable_text_with_index = []

    # use for label the real word
    real_word_label = {}

    # use to store spelling error in list
    non_real_word_list = []

    # use for label the real word
    non_real_word_label = {}

    # use to save the word and position of clicked word
    clicked_word_list = []

    def transfer_text(self):

        # here use to clear out the list and dictionary
        self.user_input_bigram = []
        self.result_dict = {}
        self.text_dict = {}
        self.clickable_text = []
        self.real_word_list = []
        self.clickable_text_with_index = []
        self.non_real_word_list = []
        self.real_word_label = {}
        self.non_real_word_label = {}

        # inside here using bigram to find the probability
        input_text = self.input_text_widget.get("1.0", "end-1c")  # to get whole sentence from input
        split_input_text = nltk.tokenize.word_tokenize(input_text.lower())  # split sentences into one by one
        # print(split_input_text)
        # self.clear_clickable_tags()

        for index, element in enumerate(split_input_text):
            # Adding elements to the dictionary with sequence as the key (starting from 1)
            self.text_dict[index + 1] = element
        # print(text_dict)

        user_input_tokens = word_tokenize(input_text)
        user_input_normalized_token = [token.lower() for token in user_input_tokens if
                                       re.match('^[a-zA-Z\']+$|[.,;]$', token)]

        self.user_input_bigram.extend(list(
            bigrams(user_input_normalized_token)))  # until here we got a list that contain the bigram of user input

        # here is where we used to identify the real word or non-real word error
        for bigram_element in self.user_input_bigram:
            if bigram_element in bigrams_list:
                found = True
                # here is where we found same bigram from user input in the trained bigram list
                pass

            else:
                # here is if not found in the bigram list, now we need to determine in real word err or non real word err
                bigram_index = self.user_input_bigram.index(
                    bigram_element)  # this is use to find which bigram index in the user input
                # print(bigram_element, " It is not found. The index of bigram is ", bigram_index)
                bigram_first_word = bigram_element[0]
                bigram_second_word = bigram_element[1]
                second_word_index = bigram_index + 1
                item_1 = bigram_second_word
                item_2 = second_word_index
                self.clickable_text.append(bigram_second_word)
                self.clickable_text_with_index.append([[item_1, item_2]])

                # here we use to save the first word and second word for each bigram and to know the place of the word in user input
                for index, (first_word, second_word) in enumerate(self.user_input_bigram, start=1):
                    self.result_dict[index - 1] = {
                        'first word': first_word,
                        'second word': second_word
                    }

                # bigram second word with their position
                # this same clickable text with index
                user_input_first_word_with_pos = [split_input_text[0], 1]
                bigram_second_word_with_pos = [bigram_second_word, second_word_index]

                # save the word into either real word or non_real word
                if split_input_text[0] not in word_list:
                    self.non_real_word_list.append(user_input_first_word_with_pos)

                if bigram_second_word in word_list:
                    self.real_word_list.append(bigram_second_word_with_pos)
                else:
                    self.non_real_word_list.append(bigram_second_word_with_pos)

        # for real_word_error in self.real_word_list:
        # self.check_real_words(bigram_second_word)

        # print(self.non_real_word_list)
        # print(self.real_word_dict)
        # print(self.result_dict)
        if not self.non_real_word_list:
            print(" ")
        else:
            for item in split_input_text:
                non_real_word_list_only_word = [item[0] for item in self.non_real_word_list]
                non_real_word_list_with_position = [item[1] for item in self.non_real_word_list]
                user_input_word_index = split_input_text.index(item)  # to get the index of word of the user input

                if user_input_word_index in non_real_word_list_with_position:
                    pointed_word = split_input_text[user_input_word_index]
                    start_char_index = input_text.find(item)
                    end_char_index = start_char_index + len(pointed_word) - 1
                    word_index = f"{user_input_word_index}"
                    self.non_real_word_label.setdefault(pointed_word, {})[word_index] = (
                        start_char_index, end_char_index
                    )

        if not self.real_word_list:
            print(" ")
        else:
            for item in split_input_text:
                real_word_list_only_word = [item[0] for item in self.real_word_list]
                real_word_list_with_position = [item[1] for item in self.real_word_list]
                user_input_word_index = split_input_text.index(item)  # to get the index of word of the user input

                if user_input_word_index in real_word_list_with_position:
                    pointed_word = split_input_text[user_input_word_index]
                    start_char_index = input_text.find(item)
                    end_char_index = start_char_index + len(pointed_word) - 1
                    word_index = f"{user_input_word_index}"
                    self.real_word_label.setdefault(pointed_word, {})[word_index] = (
                        start_char_index, end_char_index
                    )

        # print(self.check_non_real_words)
        # print(self.non_real_word_label)
        self.output_text_widget.config(state=tk.NORMAL)  # here is to insert into the output textbox
        self.output_text_widget.delete("1.0", "end")

        # use to highlight the real word error in blue
        for word, indices in self.non_real_word_label.items():
            for category, (start, end) in indices.items():
                self.output_text_widget.insert(tk.END, input_text[:start])  # Add text before the word
                self.output_text_widget.insert(tk.END, input_text[start:end + 1])  # Add the word
                self.output_text_widget.tag_add("red_bg", f"1.{start}", f"1.{end + 1}")  # Highlight with red background
                input_text = input_text[end + 1:]  # Remove processed part from input text

        # use to highlight the non real word error in blue
        for word, indices in self.real_word_label.items():
            for category, (start, end) in indices.items():
                self.output_text_widget.insert(tk.END, input_text[:start])  # Add text before the word
                self.output_text_widget.insert(tk.END, input_text[start:end + 1])  # Add the word
                self.output_text_widget.tag_add("blue_bg", f"1.{start}",
                                                f"1.{end + 1}")  # Highlight with blue background
                input_text = input_text[end + 1:]

        self.output_text_widget.insert(tk.END, input_text)  # Add the remaining text after the highlighted range
        self.output_text_widget.config(state=tk.DISABLED)  # Disable editing of output textbox

        # print(self.result_dict)
        print(self.real_word_list)
        # print(self.non_real_word_list)
        # print(self.user_input_bigram)

    def on_click(self, event):
        # Get the clicked word
        self.clicked_word_list = []

        start_index = event.widget.index("current wordstart")

        # this is purposely use for extarct word because .get() will not include the last character hence we need to add 1 to it
        end_index_word_extract = event.widget.index("current wordend")

        # Exclude the trailing whitespace by adjusting the end index
        end_index = event.widget.index("current wordend-1c")

        extracted_text = self.output_text_widget.get(start_index, end_index_word_extract)
        print(extracted_text)

        index = self.output_text_widget.index("current wordend")
        first_word_until_clicked = self.output_text_widget.get("1.0", index)
        # print(first_word_until_clicked)

        # assumption: we include the punctuation in word predicting for better model structure but during the suggestion, we will exclude the punctuation for better word structure
        first_word_until_clicked_split = nltk.tokenize.word_tokenize(first_word_until_clicked)

        # this is used to find the word index of the clicked word
        word_index = len(first_word_until_clicked_split) - 1

        # this is used to get the last word index to prevent any error when click the last word
        input_text = self.input_text_widget.get("1.0", "end-1c")  # to get whole sentence from input
        split_input_text = nltk.tokenize.word_tokenize(input_text.lower())  # split sentences into one by one

        # purpose for this list is used to check whether the word we click exist in real word list or not
        word_list_verified_used = [extracted_text, word_index]
        print(word_list_verified_used)

        # purpose for this list is used to save the clicked word into a list actually can use this 'word_list_verified_used' list also,
        # we may change word_list_verified_used to this name
        self.clicked_word_list = [extracted_text, word_index]

        if word_list_verified_used in self.real_word_list:
            if len(first_word_until_clicked_split) >= 2:
                # to get the previous word from the word we clicked (purposely used for real word error suggestion)
                previous_word_clicked = first_word_until_clicked_split[-2]

                # here we do real word check
                # here we need to do the condition check whether the word is exist in the real word list or not
                if word_index == 0:
                    self.tree.delete(*self.tree.get_children())
                    print("")

                else:
                    print(word_index)
                    self.check_real_words(previous_word_clicked)

        # here we do non real word check
        if word_list_verified_used in self.non_real_word_list:
            self.check_non_real_word(extracted_text)

        # Display the word index at the bottom
        self.bottom_label.config(text=f"Start Index: {start_index}, End Index: {end_index}")

    def calculate_edit_distance(self, misspelled_word):
        # if not same as predicted word and spell is not in dict, then it is non-real word, then use min edit dist

        # next we are going to do this and solve how to check the error word when there is only one word is enter
        # (by adding the first word from user input into non_real_word_list)
        # the procedure is almost the same as what we done in real word error
        distances = [(word, Levenshtein.distance(misspelled_word, word)) for word in word_list]

        # Sort words based on edit distance in ascending order
        sorted_distances = sorted(distances, key=lambda x: x[1])

        # Select top 5 predictions along with their distances
        top_predictions = sorted_distances[:5]

        return top_predictions

    def check_non_real_word(self, non_real_word):
        # Get predictions for a list of words
        predictions = self.calculate_edit_distance(non_real_word)
        print(predictions)

        print(f"Misspelled word: {non_real_word}")
        print(f"Top 5 suggestions:")
        for suggestion, distance in predictions:
            print(f"- {suggestion} (Edit Distance: {distance})")
        print()
        self.process_tuple_list(predictions)

    def check_real_words(self, real_word):
        # here we used not same as the predicted word but spell is correct, then it is real word error

        candidate_bigrams = [bigram for bigram in bigrams_list if bigram[0] == real_word]
        # print(candidate_bigrams)
        total_bigrams = len(candidate_bigrams)

        predicted_bigrams_probs = []
        word_found = False
        for bigram in candidate_bigrams:
            word, probability = bigram[1], freq_dist[bigram] / total_bigrams
            is_word_found = any(word_going_to_found == word for word_going_to_found, _ in predicted_bigrams_probs)

            if is_word_found:
                pass
            else:
                predicted_bigrams_probs.append((word, probability))

        # Sort the candidate bigrams by probability in descending order
        sorted_predictions = sorted(predicted_bigrams_probs, key=lambda x: x[1], reverse=True)

        # Select the top 5 predicted words
        top_5_predictions = sorted_predictions[:5]

        # Print the top 5 predicted next words
        # print("Top 5 Predicted Next Words:")
        for word, probability in top_5_predictions:
            print("")
            # print(top_5_predictions)
            print(f"Word: {word}, Probability: {probability:.4f}")

        self.process_tuple_list(top_5_predictions)

    def process_tuple_list(self, tuple_list):
        self.tree.delete(*self.tree.get_children())
        for item in tuple_list:
            word, value = item  # Unpack the tuple into word and value
            self.tree.insert('', 'end', values=(word, value))

    def update_input_text(self, event):
        selected_item = self.tree.item(self.tree.selection())
        selected_word = selected_item['values'][0]
        current_text = self.input_text_widget.get("1.0", "end-1c")
        words = nltk.tokenize.word_tokenize(current_text)
        print(self.clicked_word_list)
        clicked_index = self.clicked_word_list[1]
        if len(words) >= 2:
            words[clicked_index] = selected_word
            updated_text = ' '.join(words)
            self.input_text_widget.delete("1.0", "end-1c")
            self.input_text_widget.insert("1.0", updated_text)

    # This is for search window update
    def update_list(self, event):
        user_input = self.entry.get().lower()
        filtered_list = [word for word in word_list if user_input in word.lower()]
        filtered_list.sort()
        self.text.delete(1.0, tk.END)
        for word in filtered_list:
            self.text.insert(tk.END, word + '\n')

    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.geometry("1200x600")

        # This is for input window
        self.input_text_widget = tk.Text(self.root, height=5, width=30)
        self.input_text_widget.grid(row=0, column=0, padx=10, pady=10)

        # This is the check button
        self.transfer_button = tk.Button(self.root, text="Check Spelling", command=self.transfer_text)
        self.transfer_button.grid(row=0, column=1, padx=10, pady=10)

        # This is for output window
        self.output_text_widget = tk.Text(self.root, height=5, width=30, state=tk.DISABLED)
        self.output_text_widget.grid(row=0, column=2, padx=10, pady=10)
        self.output_text_widget.tag_configure("red_bg", background="light coral")  # Configure tag for red background
        self.output_text_widget.tag_configure("blue_bg", background="light blue")  # Configure tag for blue

        # This is for suggestion window
        self.tree = ttk.Treeview(root, columns=("Word", "Value"), show="headings")
        self.tree.heading("Word", text="Word")
        self.tree.heading("Value", text="Value")
        self.tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # This is for searching window
        self.entry_label = tk.Label(root, text="Enter a word:")
        self.entry_label.grid(row=5, column=0, padx=10, pady=10)
        self.entry = tk.Entry(root, width=30)
        self.entry.grid(row=5, column=1, padx=10, pady=10)
        self.text = scrolledtext.ScrolledText(root, width=40, height=10)
        self.text.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

        # This is for show char and word index
        self.bottom_label = tk.Label(root, text="Start Index: , End Index: ")
        self.bottom_label.grid(row=1, column=4, padx=10, pady=10)

        self.char_count = tk.StringVar()
        self.char_count.set("Character Count: 0/500")

        self.word_count = tk.StringVar()
        self.word_count.set("Word Count: 0")

        self.char_count_label = tk.Label(root, textvariable=self.char_count)
        self.char_count_label.grid(row=1, column=2, padx=10, pady=10)

        self.word_count_label = tk.Label(root, textvariable=self.word_count)
        self.word_count_label.grid(row=1, column=3, padx=10, pady=10)

        # This is used to bind the event
        self.input_text_widget.bind('<Key>', self.Restrict)
        self.input_text_widget.bind('<KeyRelease>', self.AfterRestrict)  # (update)
        self.input_text_widget.bind('<KeyRelease>', self.update_char_count)
        self.output_text_widget.bind("<ButtonRelease-1>", self.on_click)
        self.tree.bind("<ButtonRelease-1>", self.update_input_text)
        self.entry.bind('<KeyRelease>', self.update_list)

        root.mainloop()


if __name__ == "__main__":
    program = SpellingChecker(root)
