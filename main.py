import tkinter as tk
import re
from tkinter.scrolledtext import ScrolledText
import nltk
from nltk.corpus import words
from textblob import TextBlob
from textblob import Word
import time
import enchant

#nltk.download("words")
#nltk.download('punkt')




def spellingchecker():

    def OtherTextWidget(string):
        print("Key Press Phase:", string)

    # Solution - Step 1. toggle full flag
    global full  # (update)
    full = False

    # Solution - Step 4. profit
    def AfterRestrict(e=None):  # (update)
        global full
        if True == full:
            OtherTextWidget(e.widget.get("1.0", "1.5"))
            print("Key Release Phase:", e.widget.get("1.0", "1.5"))

    # Solution - Step 3. limit input
    def Restrict(e=None):
        global full  # (update)
        string = e.widget.get("1.0", "end-1c")
        if 499 <= len(string):
            e.widget.delete('1.499', "end-1c")
            full = True  # (update)
        else:  # (update)
            full = False

    # Here we update for chac count and word count and also restrict the char limit
    def update_char_count(e=None):
        current_text = input_text_widget.get("1.0", "end-1c")
        current_text_char = current_text.replace(' ', '').replace('\n', '')
        char_count.set(f"Character Count: {len(current_text_char)}/500")

        tokens = re.split(r'\s+', current_text)
        non_empty_words = [token for token in tokens if token]  # Count non-empty tokens
        word_count.set(f"Word Count: {len(non_empty_words)}")

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

    def transfer_text():
        input_text = input_text_widget.get("1.0", "end-1c")
        split_input_text = re.findall(r"\w+", input_text)
        clear_clickable_tags()
        output_text_widget.config(state=tk.NORMAL)
        output_text_widget.delete("1.0", "end")
        output_text_widget.insert("end", input_text + "\n")
        output_text_widget.config(state=tk.DISABLED)
        print(split_input_text)
        make_words_clickable(split_input_text)

    def clear_clickable_tags():
        output_text_widget.tag_remove("clickable", "1.0", "end")

    def make_words_clickable(target_words):
        output_text_widget.tag_configure("clickable", foreground="blue", underline=True)
        for word in target_words:
            start = "1.0"
            while start:
                start = output_text_widget.search(rf"\y{word}\y", start, stopindex="end", regexp=True)
                if start:
                    end = output_text_widget.index(f"{start}+{len(word)}c")
                    output_text_widget.tag_add("clickable", start, end)
                    start = end

    def check_real_words(word):
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
        elif word != result[0][0] and result [0][1] < 1:
            print("Error Type: real-word error")
            print(f'Spelling of "{word}" is incorrect!')

    # def split_word(sentences):
    #     re.findall(r"\w+", sentences)

    def show_popup(event):
        clicked_word_index = output_text_widget.index(tk.CURRENT + " wordstart")
        clicked_word_end_index = output_text_widget.index(tk.CURRENT + " wordend")
        clicked_word = output_text_widget.get(clicked_word_index, clicked_word_end_index).strip()
        print(clicked_word)
        check_real_words(clicked_word)

        if clicked_word:
            if "clickable" in output_text_widget.tag_names(tk.CURRENT):
                new_window = tk.Toplevel(root)
                new_window.title("Clicked Word")
                label = tk.Label(new_window, text=f"You clicked: {clicked_word}")
                label.pack(padx=20, pady=20)

    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    input_text_widget = tk.Text(frame, height=5, width=30)
    input_text_widget.grid(row=0, column=0, padx=5, pady=5)

    input_text_scrollbar = tk.Scrollbar(frame, command=input_text_widget.yview)
    input_text_scrollbar.grid(row=0, column=1, sticky='ns')
    input_text_widget.config(yscrollcommand=input_text_scrollbar.set)

    transfer_button = tk.Button(frame, text="Check Spelling", command=transfer_text)
    transfer_button.grid(row=0, column=2, padx=5, pady=5)

    output_text_widget = tk.Text(frame, height=5, width=30, state=tk.DISABLED)
    output_text_widget.grid(row=0, column=3, padx=5, pady=5)

    output_text_scrollbar = tk.Scrollbar(frame, command=output_text_widget.yview)
    output_text_scrollbar.grid(row=0, column=4, sticky='ns')
    output_text_widget.config(yscrollcommand=output_text_scrollbar.set)

    output_text_widget.tag_bind("clickable", "<Button-1>", show_popup)

    char_count = tk.StringVar()
    char_count.set("Character Count: 0/500")

    word_count = tk.StringVar()
    word_count.set("Word Count: 0")

    char_count_label = tk.Label(root, textvariable=char_count)
    char_count_label.pack()

    word_count_label = tk.Label(root, textvariable=word_count)
    word_count_label.pack()

    # printButton = tk.Button(root,
    #                         text="Print",
    #                         command=printInput)
    # printButton.pack()


    # Label Creation
    # lbl = tk.Label(root, text="")
    # lbl.pack()

    # Solution - Step 2. get input event from widget
    input_text_widget.bind('<Key>', Restrict)
    input_text_widget.bind('<KeyRelease>', AfterRestrict) #(update)
    input_text_widget.bind('<KeyRelease>', update_char_count)

    root.mainloop()

if __name__ == "__main__":
    spellingchecker()