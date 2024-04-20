# 필요한 요소 import
import os, json, aiofiles
from py_trans import PyTranslator
import pythonbible as bible
import random

# tr 객체 선언
tr = PyTranslator()

# 성경 책 dict
bible_books = {
    #korean
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
    "예레미야애가": 25,
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
    "1 Samuel": 9,
    "2 Samuel": 10,
    "1 Kings": 11,
    "2 Kings": 12,
    "1 Chronicles": 13,
    "2 Chronicles": 14,
    "Ezra": 15,
    "Nehemiah": 16,
    "Esther": 17,
    "Job": 18,
    "Psalms": 19,
    "Proverbs": 20,
    "Ecclesiastes": 21,
    "Song of Solomon": 22,
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
    "1 Corinthians": 46,
    "2 Corinthians": 47,
    "Galatians": 48,
    "Ephesians": 49,
    "Philippians": 50,
    "Colossians": 51,
    "1 Thessalonians": 52,
    "2 Thessalonians": 53,
    "1 Timothy": 54,
    "2 Timothy": 55,
    "Titus": 56,
    "Philemon": 57,
    "Hebrews": 58,
    "James": 59,
    "1 Peter": 60,
    "2 Peter": 61,
    "1 John": 62,
    "2 John": 63,
    "3 John": 64,
    "Jude": 65,
    "Revelation": 66
}

# 번역 해주는 함수
def translate_text(text):
    translated_info = tr.google(str(text), "ko")
    # 예시 : {'status': 'success', 'engine': 'Google Translate', 'translation': '안녕하세요!', 'dest': 'ko', 'orgin': 'Hello!', 'origin_lang': 'en'}
    return translated_info['translation']

# id 00n 으로 format 해주는 함수
def formating_nums(id):
    return "{:03d}".format(id)

# verse ID 찾아주는 함수(효율성 개선 시급)
def verse_ID_generator(book, chapter, verse):
    if type(book) == str:
        book_num = str(bible_books.get(book))
    elif type(book) == int:
        book_num = formating_nums(book)

    chapter_num = formating_nums(int(chapter))
    verse_num = formating_nums(int(verse))

    return book_num + chapter_num + verse_num


# 구문 찾아주는 함수
def find_verse(book, chapter, verse):
    verse_ID = int(verse_ID_generator(book, chapter, verse))
    verse_text = bible.get_verse_text(verse_id=verse_ID, version=bible.Version.AMERICAN_STANDARD)
    result = translate_text(verse_text)
    print(result)

#랜덤으로 구절 정하는 함수(구현 중)
def random_verse():

    r_book = random.choice(list(bible_books_eng.keys()))
    print(bible.get_number_of_chapters(r_book)) #bible book class 에 대해 공부
    # r_chapter = random.randint(1,bible.get_number_of_chapters(r_book))
    # r_verse = random.randint(1, bible.get_number_of_verses(r_book,r_chapter))
    # print(r_book, r_chapter, r_verse)

if __name__ == "__main__":
    # book = input("책 : ")
    # chapter = input("장 : ")
    # verse = input("절 : ")
    # find_verse(book, chapter, verse)
    random_verse()


# 추가할 기능
# 랜덤으로 구절 찾기
# 없는 값 입력 받았을 때 오류 출력하고 돌아가기
