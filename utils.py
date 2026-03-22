import os
import chardet
import random

def load_compliments():
    if os.path.exists('trolls.txt'):
        with open('trolls.txt', 'rb') as f:
            raw_data = f.read()
            encoding_info = chardet.detect(raw_data)
            file_encoding = encoding_info['encoding'] if encoding_info['encoding'] else 'utf-8'
        try:
            with open('trolls.txt', 'r', encoding=file_encoding, errors='replace') as f:
                compliments = [line.strip() for line in f.readlines() if line.strip()]
            return compliments
        except Exception as e:
            print(f"Ошибка чтения файла trolls.txt: {e}")
            return []
    return []

def add_compliment(compliment):
    with open('trolls.txt', 'a', encoding='utf-8') as f:
        f.write(f"{compliment}\n")

def load_words():
    if os.path.exists("slova.py"):
        import slova
        return slova.__dict__
    else:
        return {
            "numbers": [],
            "countries": [],
            "regions": [],
            "operators": [],
            "names": [],
            "addresses": [],
            "birth_dates": [],
            "good_reps": [],
            "bad_reps": [],
            "interests": [],
            "social_marks": [],
            "comments_counts": []
        }

def save_words(slova):
    with open("slova.py", "w", encoding="utf-8") as file:
        for key, value in slova.items():
            file.write(f"{key} = {repr(value)}\n")

def check_empty(value_list, default_value="пусто"):
    return random.choice(value_list) if value_list else default_value
