import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import nltk
from nltk.corpus import words
from textblob import TextBlob
from textblob import Word
import time
import enchant


# nltk.download("words")
# nltk.download('punkt')

from nltk.tokenize import word_tokenize
import re
import numbers

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

    def transfer_text(self):
        input_text = self.input_text_widget.get("1.0", "end-1c")
        split_input_text = re.findall(r"\w+", input_text)
        self.clear_clickable_tags()
        self.output_text_widget.config(state=tk.NORMAL)
        self.output_text_widget.delete("1.0", "end")
        self.output_text_widget.insert("end", input_text + "\n")
        self.output_text_widget.config(state=tk.DISABLED)
        print(split_input_text)
        self.make_words_clickable(split_input_text)

    def clear_clickable_tags(self):
        self.output_text_widget.tag_remove("clickable", "1.0", "end")

    def make_words_clickable(self, target_words):
        self.output_text_widget.tag_configure("clickable", foreground="blue", underline=True)
        for word in target_words:
            start = "1.0"
            while start:
                start = self.output_text_widget.search(rf"\y{word}\y", start, stopindex="end", regexp=True)
                if start:
                    end = self.output_text_widget.index(f"{start}+{len(word)}c")
                    self.output_text_widget.tag_add("clickable", start, end)
                    start = end

    def check_real_words(self,word):
        word = Word(word)
        result = word.spellcheck()

        if word == result[0][0] and result[0][1] == 0:
            print(f'"{word}" is unable to detect. Will try to search in dictionary')
            print("Loading.....")
            time.sleep(5)
            exists = enchant.dict_exists(word)
            if exists == True:
                print("The dictionary for " + word + " exists. It is real word but with wrong spelling")
            else:
                print("Error Type: Non-word error")
        elif word == result[0][0] and result[0][1] == 1:
            print(f'Spelling of "{word}" is correct!')
        elif word != result[0][0] and result[0][1] < 1:
            print("Error Type: real-word error")
            print(f'Spelling of "{word}" is incorrect!')

    # def split_word(sentences):
    #     re.findall(r"\w+", sentences)

    def show_popup(self,event):
        clicked_word_index = self.output_text_widget.index(tk.CURRENT + " wordstart")
        clicked_word_end_index = self.output_text_widget.index(tk.CURRENT + " wordend")
        clicked_word = self.output_text_widget.get(clicked_word_index, clicked_word_end_index).strip()
        print(clicked_word)
        self.check_real_words(clicked_word)

        if clicked_word:
            if "clickable" in self.output_text_widget.tag_names(tk.CURRENT):
                new_window = tk.Toplevel(self.root)
                new_window.title("Clicked Word")
                label = tk.Label(new_window, text=f"You clicked: {clicked_word}")
                label.pack(padx=20, pady=20)

    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
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

        self.output_text_widget.tag_bind("clickable", "<Button-1>", self.show_popup)

        self.char_count = tk.StringVar()
        self.char_count.set("Character Count: 0/500")

        self.word_count = tk.StringVar()
        self.word_count.set("Word Count: 0")

        self.char_count_label = tk.Label(self.root, textvariable=self.char_count)
        self.char_count_label.pack()

        self.word_count_label = tk.Label(self.root, textvariable=self.word_count)
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

        self.root.mainloop()


if __name__ == "__main__":
    program = spellingchecker()
