import random
import re
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime

INTENTS = [
    ("greeting", [r"\b(hi|hello|hey|good morning|good afternoon|good evening)\b", r"\bhow are you\b"], [
        "Hello! 😊 How can I help you today?",
        "Hi there! Type 'help' to see example questions.",
        "Hey! Nice to chat with you. What would you like to know?",
    ]),
    ("goodbye", [r"\b(bye|goodbye|see you|exit|quit)\b"], [
        "Goodbye! Have a great day. 👋", "See you next time!",
    ]),
    ("thanks", [r"\b(thanks|thank you|thx)\b"], [
        "You're welcome!", "Happy to help! 😊",
    ]),
    ("name", [r"\b(your name|who are you|what are you)\b"], [
        "I'm Offline AI Chatbot, a Python mini project that works without an API.",
        "You can call me Offline Bot. I run locally on your computer.",
    ]),
    ("help", [r"\b(help|what can you do|features|options)\b"], [
        "I can respond to greetings, answer a few general questions, tell the time/date, "
        "and provide basic study tips. Try: 'What is AI?', 'What is Python?', "
        "'What is machine learning?', 'Give me study tips', or 'What time is it?'"
    ]),
    ("ai", [r"\b(what is ai|artificial intelligence|define ai)\b"], [
        "Artificial Intelligence (AI) is a field of computing that develops systems for "
        "tasks such as recognizing patterns, understanding language, making predictions, "
        "and solving problems."
    ]),
    ("python", [r"\b(what is python|python language|learn python)\b"], [
        "Python is a high-level, general-purpose programming language known for readable "
        "syntax. It is used in automation, web development, data analysis, machine learning, and AI."
    ]),
    ("machine learning", [r"\b(machine learning|what is ml|define ml)\b"], [
        "Machine learning is a branch of AI in which computers learn patterns from data "
        "to make predictions or decisions, rather than relying only on hand-written rules."
    ]),
    ("study", [r"\b(study tips|how to study|exam preparation|prepare for exam)\b"], [
        "Try this study plan: choose one small topic, study for 25 minutes, take a 5-minute "
        "break, summarize it from memory, and solve practice questions. Review difficult topics later."
    ]),
    ("motivation", [r"\b(motivate me|motivation|feeling lazy|inspiration)\b"], [
        "Start with just five minutes. A small step is easier to begin, and progress often "
        "builds motivation. Choose one task and complete it now."
    ]),
    ("time", [r"\b(what time|current time|tell me the time)\b"], [
        lambda: "The current local time is " + datetime.now().strftime("%I:%M %p") + "."
    ]),
    ("date", [r"\b(today's date|what date|current date|what day is it)\b"], [
        lambda: "Today's date is " + datetime.now().strftime("%A, %d %B %Y") + "."
    ]),
    ("creator", [r"\b(who made you|who created you|your developer)\b"], [
        "I was created as a student mini-project using Python. This version works locally "
        "and does not connect to an online AI service."
    ]),
]

def get_response(user_text):
    text = re.sub(r"\s+", " ", user_text.lower().strip())
    if not text:
        return "Please type a message first."
    for _, patterns, responses in INTENTS:
        for pattern in patterns:
            if re.search(pattern, text):
                response = random.choice(responses)
                return response() if callable(response) else response
    return (
        "I'm an offline, rule-based chatbot, so I don't understand every question yet. "
        "Try asking about AI, Python, machine learning, study tips, the date, or the time. "
        "You can improve me by adding more patterns and responses in the code."
    )

class OfflineChatbotApp:
    def __init__(self, root):
        self.root = root
        root.title("Offline AI Chatbot - MCA Mini Project")
        root.geometry("760x620")
        root.minsize(560, 460)
        root.configure(bg="#f2f4f8")

        tk.Label(root, text="🤖 Offline AI Chatbot", font=("Segoe UI", 20, "bold"),
                 bg="#f2f4f8", fg="#1f2937").pack(pady=(14, 2))
        tk.Label(root, text="Python mini project • By Cu • Works offline",
                 font=("Segoe UI", 10), bg="#f2f4f8", fg="#4b5563").pack(pady=(0, 10))

        self.chat_area = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, font=("Segoe UI", 11), state=tk.DISABLED,
            padx=12, pady=12, bg="white", fg="#111827", relief=tk.FLAT
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 12))
        self.chat_area.tag_config("user", foreground="#075985", spacing1=8, spacing3=5)
        self.chat_area.tag_config("bot", foreground="#166534", spacing1=8, spacing3=5)

        bottom = tk.Frame(root, bg="#f2f4f8")
        bottom.pack(fill=tk.X, padx=16, pady=(0, 16))
        self.entry = tk.Entry(bottom, font=("Segoe UI", 11), relief=tk.FLAT, bd=0)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=11, padx=(0, 8))
        self.entry.bind("<Return>", self.send_message)

        tk.Button(bottom, text="Send", command=self.send_message, font=("Segoe UI", 10, "bold"),
                  bg="#2563eb", fg="white", activebackground="#1d4ed8",
                  activeforeground="white", relief=tk.FLAT, padx=18, pady=8,
                  cursor="hand2").pack(side=tk.LEFT)
        tk.Button(bottom, text="Clear", command=self.clear_chat, font=("Segoe UI", 10),
                  bg="#e5e7eb", fg="#111827", relief=tk.FLAT, padx=14, pady=8,
                  cursor="hand2").pack(side=tk.LEFT, padx=(8, 0))

        self.add_message("Bot", "Hello! I'm your Offline AI Chatbot. I work without an API "
                         "or internet connection. Type 'help' to see example questions.", "bot")
        self.entry.focus_set()

    def add_message(self, speaker, text, tag):
        self.chat_area.configure(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"{speaker}: {text}\n\n", tag)
        self.chat_area.configure(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def send_message(self, event=None):
        user_text = self.entry.get().strip()
        if not user_text:
            return
        self.entry.delete(0, tk.END)
        self.add_message("You", user_text, "user")
        self.add_message("Bot", get_response(user_text), "bot")

    def clear_chat(self):
        if messagebox.askyesno("Clear chat", "Do you want to clear the conversation?"):
            self.chat_area.configure(state=tk.NORMAL)
            self.chat_area.delete("1.0", tk.END)
            self.chat_area.configure(state=tk.DISABLED)
            self.add_message("Bot", "Chat cleared. How can I help you?", "bot")

def main():
    root = tk.Tk()
    OfflineChatbotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
