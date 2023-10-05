import tkinter as tk
# from tkinter.scrolledtext import ScrolledText
# import nltk
# from nltk.corpus import words
# from textblob import TextBlob
from nltk import bigrams, FreqDist
from nltk.probability import ConditionalFreqDist
# from textblob import Word
# import time
# import enchant
import os

# nltk.download("words")
# nltk.download('punkt')

from nltk.tokenize import word_tokenize
import re
import numbers

root = tk.Tk()

file_path = "C:/Users/User/PycharmProjects/NLP_Project/dictionary/english_words_479k.txt"
file = open(file_path, 'r', encoding='utf-8', errors='ignore')

word_list = set()

for x in file:
    #here we got to tokenize and preprocessing the word dictionary
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


class spellingchecker():

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

   # use to store spelling error
    non_real_word_dict = {}
    def transfer_text(self):

        # here use to clear out the list and dictionary
        self.user_input_bigram = []
        self.result_dict = {}
        self.text_dict = {}
        self.clickable_text = []
        self.real_word_list = []
        self.clickable_text_with_index = []
        self.non_real_word_dict = {}

        # inside here using bigram to find the probability
        input_text = self.input_text_widget.get("1.0", "end-1c")
        split_input_text = re.findall(r"\w+", input_text)
        # self.clear_clickable_tags()
        self.output_text_widget.config(state=tk.NORMAL)
        self.output_text_widget.delete("1.0", "end")
        self.output_text_widget.insert("end", input_text + "\n")
        self.output_text_widget.config(state=tk.DISABLED)
        # print(split_input_text)


        # print(input_text)

        # text = self.input_text_widget.get(1.0, 'end-1c')
        # print(text)
        for index, element in enumerate(split_input_text):
            # Adding elements to the dictionary with sequence as the key (starting from 1)
            self.text_dict[index + 1] = element
        # print(text_dict)


        user_input_tokens = word_tokenize(input_text)
        user_input_normalized_token = [token.lower() for token in user_input_tokens if re.match('^[a-zA-Z\']+$|[.,;]$', token)]

        self.user_input_bigram.extend(list(bigrams(user_input_normalized_token)))

        found = False

        for bigram_element in self.user_input_bigram:
            if bigram_element in bigrams_list:
                found = True
                bigram_index = self.user_input_bigram.index(bigram_element)
                pass
                # print("It is found", bigram_element, " ", bigram_index)
            else:
                bigram_index = self.user_input_bigram.index(bigram_element)
                print(bigram_element, " It is not found. The index of bigram is ", bigram_index)
                bigram_first_word = bigram_element[0]
                bigram_second_word = bigram_element[1]
                item_1 = bigram_second_word
                item_2 = bigram_index
                self.clickable_text.append(bigram_second_word)
                self.clickable_text_with_index.append([[item_1,item_2]])

                # here we use to save the first word and second word for each bigram and to know the place of the word in user input
                for index, (first_word, second_word) in enumerate(self.user_input_bigram, start=1):
                    self.result_dict[index] = {
                        'first word': first_word,
                        'second word': second_word
                    }

                #bigram second word with their position
                bigram_second_word_with_pos = [bigram_second_word, bigram_index]

                # save  the word into either real word or non_real word
                if bigram_second_word in word_list:
                    self.real_word_list.append(bigram_second_word_with_pos)
                else:
                    self.non_real_word_dict.update({bigram_second_word: bigram_index})


                self.check_real_words(bigram_first_word)

        # print(self.real_word_dict)
        # print(self.non_real_word_dict)
        print(self.result_dict)
        # print(self.check_non_real_words)
        self.make_words_clickable(self.clickable_text)
        print(self.clickable_text_with_index)

    def clear_clickable_tags(self):
        self.output_text_widget.tag_remove("clickable", "1.0", "end")

    # dont used this function, got something wring at the moment
    def make_words_clickable(self, target_words):
        self.output_text_widget.tag_configure("clickable", foreground="blue", underline=False)
        for word in target_words:
            start = "1.0"
            while start:
                start = self.output_text_widget.search(rf"\y{word}\y", start, stopindex="end", regexp=True)
                if start:
                    end = self.output_text_widget.index(f"{start}+{len(word)}c")
                    self.output_text_widget.tag_add("clickable", start, end)
                    start = end

    def check_non_real_words(self,misspelled_word):
        # if not same as predicted word and spell is not in dict, then it is non-real word, then use min edit dist
        return True

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
        print("Top 5 Predicted Next Words:")
        for word, probability in top_5_predictions:
            print(f"Word: {word}, Probability: {probability:.4f}")

    # def split_word(sentences):
    #     re.findall(r"\w+", sentences)

    def show_word_window(self, clicked_word, previous_word, whole_sentence):
        word_window = tk.Toplevel(root)  # Create a new window
        word_window.title("Clicked Word and Previous Word")
        label = tk.Label(word_window, text="Clicked Word: " + clicked_word)
        label.pack(padx=20, pady=5)
        label = tk.Label(word_window, text="Previous Word: " + previous_word)
        label.pack(padx=20, pady=5)
        label = tk.Label(word_window, text="First to current clicked Word: " + whole_sentence)
        label.pack(padx=20, pady=5)

    # 如何拿到current word position. get the whole sentences until the word we clicked. The do splitting. This splitting should include the punctuation
    # since bigram created also include the punctuation
    # then we compare the position of previous word with clickable_word_with_index 就可以拿到需要让那个文字clickable

    # 第二种 方法直接无视什么index，直接拿previous word 丢进去比较就好了
    def on_word_click(self, event):
        index = self.output_text_widget.index(tk.CURRENT)  # Get the index of the clicked word
        # clicked_word = self.output_text_widget.get(index + " wordstart", index + " wordend")  # Extract the clicked word
        text = self.output_text_widget.get("1.0", index + "wordend")  # Get the text from the beginning to the clicked word
        # print("this is the index of current clicked word: ", index + "wordend")
        words = re.findall(r'\w+', text)  # Extract words using regular expression
        clicked_word = words[-1]  # Get the last word (clicked word)
        print(words)
        clicked_word_index = words.index(clicked_word) + 1
        print(clicked_word_index)
        if len(words) >= 2:
            previous_word = words[-2] # Get the second last word (previous word)
            self.show_word_window(clicked_word, previous_word, str(clicked_word_index))  # Display the clicked word and its previous word in a new window
        else:
            self.show_word_window("No previous word", "No clicked word")

    def __init__(self):
        super().__init__()
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.input_text_widget = tk.Text(self.frame, height=5, width=30)
        self.input_text_widget.grid(row=0, column=0, padx=5, pady=5)

        self.input_text_scrollbar = tk.Scrollbar(self.frame, command=self.input_text_widget.yview)
        self.input_text_scrollbar.grid(row=0, column=1, sticky='ns')
        self.input_text_widget.config(yscrollcommand=self.input_text_scrollbar.set)

        self.transfer_button = tk.Button(self.frame, text="Check Spelling", command=self.transfer_text)
        self.transfer_button.grid(row=0, column=2, padx=5, pady=5)

        self.output_text_widget = tk.Text(self.frame, height=5, width=30, state=tk.DISABLED)
        self.output_text_widget.grid(row=0, column=3, padx=5, pady=5)

        self.output_text_scrollbar = tk.Scrollbar(self.frame, command=self.output_text_widget.yview)
        self.output_text_scrollbar.grid(row=0, column=4, sticky='ns')
        self.output_text_widget.config(yscrollcommand=self.output_text_scrollbar.set)

        self.output_text_widget.bind("<ButtonRelease-1>", self.on_word_click)

        self.char_count = tk.StringVar()
        self.char_count.set("Character Count: 0/500")

        self.word_count = tk.StringVar()
        self.word_count.set("Word Count: 0")

        self.char_count_label = tk.Label(root, textvariable=self.char_count)
        self.char_count_label.pack()

        self.word_count_label = tk.Label(root, textvariable=self.word_count)
        self.word_count_label.pack()

        # printButton = tk.Button(root,
        #                         text="Print",
        #                         command=printInput)
        # printButton.pack()

        # Label Creation
        # lbl = tk.Label(root, text="")
        # lbl.pack()

        # Solution - Step 2. get input event from widget
        self.input_text_widget.bind('<Key>', self.Restrict)
        self.input_text_widget.bind('<KeyRelease>', self.AfterRestrict)  # (update)
        self.input_text_widget.bind('<KeyRelease>', self.update_char_count)

        root.mainloop()


if __name__ == "__main__":
    program = spellingchecker()
