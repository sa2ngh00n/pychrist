import os
import json
import random
import aiofiles
from py_trans import PyTranslator
import pythonbible as bible

# tr 객체 선언
tr = PyTranslator()

# 성경 책 dict
bible_books = {
    "창세기": 1,
    "출애굽기": 2,
    "레위기": 3,
    "민수기": 4,
    "신명기": 5,
    "여호수아": 6,
    "사사기": 7,
    "룻": 8,
    "사무엘상": 9,
    "사무엘하": 10,
    "열왕기상": 11,
    "열왕기하": 12,
    "역대상": 13,
    "역대하": 14,
    "에스라": 15,
    "느헤미야": 16,
    "에스더": 17,
    "욥": 18,
    "시편": 19,
    "잠언": 20,
    "전도서": 21,
    "아가": 22,
    "이사야": 23,
    "예레미야": 24,
    "에스겔": 26,
    "다니엘": 27,
    "호세아": 28,
    "요엘": 29,
    "아모스": 30,
    "오바댜": 31,
    "요나": 32,
    "미가": 33,
    "나훔": 34,
    "하박국": 35,
    "스바냐": 36,
    "학개": 37,
    "스가랴": 38,
    "말라기": 39,
    "마태복음": 40,
    "마가복음": 41,
    "누가복음": 42,
    "요한복음": 43,
    "사도행전": 44,
    "로마서": 45,
    "고린도전서": 46,
    "고린도후서": 47,
    "갈라디아서": 48,
    "에베소서": 49,
    "빌립보서": 50,
    "골로새서": 51,
    "데살로니가전서": 52,
    "데살로니가후서": 53,
    "디모데전서": 54,
    "디모데후서": 55,
    "디도서": 56,
    "빌레몬서": 57,
    "히브리서": 58,
    "야고보서": 59,
    "베드로전서": 60,
    "베드로후서": 61,
    "요한1서": 62,
    "요한2서": 63,
    "요한3서": 64,
    "유다서": 65,
    "요한계시록": 66,
}

bible_books_eng = {
    "Genesis": 1,
    "Exodus": 2,
    "Leviticus": 3,
    "Numbers": 4,
    "Deuteronomy": 5,
    "Joshua": 6,
    "Judges": 7,
    "Ruth": 8,
    "Samuel_1": 9,
    "Samuel_2": 10,
    "Kings_1": 11,
    "Kings_2": 12,
    "Chronicles_1": 13,
    "Chronicles_2": 14,
    "Ezra": 15,
    "Nehemiah": 16,
    "Esther": 17,
    "Job": 18,
    "Psalms": 19,
    "Proverbs": 20,
    "Ecclesiastes": 21,
    "Wisdom_of_Solomon": 22,
    "Isaiah": 23,
    "Jeremiah": 24,
    "Lamentations": 25,
    "Ezekiel": 26,
    "Daniel": 27,
    "Hosea": 28,
    "Joel": 29,
    "Amos": 30,
    "Obadiah": 31,
    "Jonah": 32,
    "Micah": 33,
    "Nahum": 34,
    "Habakkuk": 35,
    "Zephaniah": 36,
    "Haggai": 37,
    "Zechariah": 38,
    "Malachi": 39,
    "Matthew": 40,
    "Mark": 41,
    "Luke": 42,
    "John": 43,
    "Acts": 44,
    "Romans": 45,
    "Corinthians_1": 46,
    "Corinthians_2": 47,
    "Galatians": 48,
    "Ephesians": 49,
    "Philippians": 50,
    "Colossians": 51,
    "Thessalonians_1": 52,
    "Thessalonians_2": 53,
    "Timothy_1": 54,
    "Timothy_2": 55,
    "Titus": 56,
    "Philemon": 57,
    "Hebrews": 58,
    "James": 59,
    "Peter_1": 60,
    "Peter_2": 61,
    "John_1": 62,
    "John_2": 63,
    "John_3": 64,
    "Jude": 65,
    "Revelation": 66
}

# 번역 해주는 함수
def translate_text(text, dest="ko"):
    translated_info = tr.translate_com(str(text), dest)
    return translated_info['translation']

# id 00n 으로 format 해주는 함수
def formating_nums(id):
    return "{:03d}".format(id)

# verse ID 찾아주는 함수
def verse_ID_generator(book, chapter, verse):
    book_num = str(bible_books.get(book, ""))
    chapter_num = formating_nums(int(chapter))
    verse_num = formating_nums(int(verse))

    return book_num + chapter_num + verse_num

# 구문 찾아주는 함수
def find_verse(book, chapter, verse):
    verse_ID = int(verse_ID_generator(book, chapter, verse))
    verse_text = bible.get_verse_text(verse_id=verse_ID, version=bible.Version.AMERICAN_STANDARD)
    return translate_text(verse_text)

#랜덤으로 구절 정하는 함수
def random_verse():
    r_book_choice = random.choice(list(bible_books_eng.keys()))
    r_book = bible_books_eng[r_book_choice]
    r_chapter = random.randint(1, bible.get_number_of_chapters(r_book_choice))
    r_verse = random.randint(1, bible.get_number_of_verses(r_book_choice, r_chapter))
    return find_verse(r_book, r_chapter, r_verse)

# 명령어 처리
def process_command(command):
    if 'help' in command:
        print("""
        find mode : 원하는 구절을 찾고 싶을 때 [mode -f]
        random mode : 하루에 묵상할 3개의 구절을 찾고 싶을 때 [mode -r]
        list mode : 성경의 list를 보고 싶을 때 [mode -l] 영어 모드 -> mode -l -e
        exit : 프로그램을 종료할 때 [exit]
        """)
    elif 'mode' in command:
        if '-f' in command:
            user_book = input("책 : ")
            user_chapter = input("장 : ")
            user_verse = input("절 : ")
            print(find_verse(user_book, user_chapter, user_verse))
        elif '-r' in command:
            for _ in range(3):
                print(random_verse())
        elif '-l' in command:
            if '-e' in command:
                for book in bible_books_eng.keys():
                    print(book)
            else:
                for book in bible_books.keys():
                    print(book)
    elif 'exit' == command:
        exit()
    elif 'clear' == command:
        os.system('cls' if os.name == 'nt' else 'clear')

#main
if __name__ == "__main__":
    print(r"""                                                                                          
                                                    ,---,                                          ___     
                ,-.----.                          ,--.' |                 ,--,                   ,--.'|_   
                \    /  \                         |  |  :       __  ,-. ,--.'|                   |  | :,'  
                |   :    |                        :  :  :     ,' ,'/ /| |  |,       .--.--.      :  : ' :  
                |   | .\ :       .--,     ,---.   :  |  |,--. '  | |' | `--'_      /  /    '   .;__,'  /   
                .   : |: |     /_ ./|    /     \  |  :  '   | |  |   ,' ,' ,'|    |  :  /`./   |  |   |    
                |   |  \ :  , ' , ' :   /    / '  |  |   /' : '  :  /   '  | |    |  :  ;_     :__,'| :    
                |   : .  | /___/ \: |  .    ' /   '  :  | | | |  | '    |  | :     \  \    `.    '  : |__  
                :     |`-'  .  \  ' |  '   ; :__  |  |  ' | : ;  : |    '  : |__    `----.   \   |  | '.'| 
                :   : :      \  ;   :  '   | '.'| |  :  :_:,' |  , ;    |  | '.'|  /  /`--'  /   ;  :    ; 
                |   | :       \  \  ;  |   :    : |  | ,'      ---'     ;  :    ; '--'.     /    |  ,   /  
                `---'.|        :  \  \  \   \  /  `--''                 |  ,   /    `--'---'      ---`-'   
                `---`         \  ' ;   `----'                          ---`-'                            
                 `--`                                                                                                                             
    """)
    print("명령어를 보려면 'help'를 입력하세요.")
    while True:
        user_input = input(": ")
        process_command(user_input)
