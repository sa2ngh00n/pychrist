"""
TO DO:
캘린더 추가, 일정 기능 추가
관련 정보 검색해주는 기능 추가
리스트 만드는 기능 추가
"""

# 필요한 요소 import
import os, json, aiofiles,random,requests
import pythonbible as bible
from pythonbible import Book
from py_trans import PyTranslator
from pythonbible.errors import VersionMissingVerseError
from dotenv import load_dotenv

#env 파일 불러오기
load_dotenv("search_api.env")
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
    "에스드라스" : 67,
    "토비트" : 68,
    "지혜서" : 69,
    "집회서" : 70,
    "마카베오기1서" : 71,
    "마카베오기2서" : 72
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
    "Songs_of_songs": 22,
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
    "Revelation": 66,
    "Esdras_1" : 67,
    "Tobit" : 68,
    "Wisdom_of_solomon" : 69,
    "Ecclesiasticus" : 70,
    "Maccabees_1" : 71,
    "Maccabees_2" : 72
}

day = ["아침","점심","저녁"]

#매개 변수 정의
api_key = os.getenv('API_KEY')
search_engine_id = os.getenv('SEARCH_ENGINE_ID')

# 번역 해주는 함수
def translate_text(text : str) -> str: 
    """
    this function translates eng to korean
    """
    translated_info = tr.translate_com(str(text), 'ko')
    # 예시 : {'status': 'success', 'engine': 'Translate com', 'translation': '안녕하세요!', 'dest': 'ko', 'orgin': 'Hello!', 'origin_lang': 'en'}
    return translated_info['translation']

# id 00n 으로 format 해주는 함수
def format_nums(id : int) -> str:
    """
    This function formats number of id to str
    """
    return "{:03d}".format(id)

# verse id 만들어 주는 함수
def generate_verse_id(book, chapter : int, verse : int) -> str:
    """
    This function generates verse id 
    """
    if type(book) == str:
        book_num = format_nums(bible_books.get(book))
    elif type(book) == int:
        book_num = format_nums(book)

    chapter_num = format_nums(int(chapter))
    verse_num = format_nums(int(verse))

    return book_num + chapter_num + verse_num

# 구문 찾아주는 함수
def find_verse(book : str, chapter : str, verse : str) -> str:
    """This function finds verse"""
    verse_id = int(generate_verse_id(book, chapter, verse))
    #Missing error 예외 처리 후 해결해야함 try-except 문 사용
    try:
        verse_text = bible.get_verse_text(verse_id=verse_id, version=bible.Version.KING_JAMES)
        return translate_text(verse_text)
    except VersionMissingVerseError as e:
        return "(구절 없음)"

#랜덤으로 구절 생성해주는 함수
def void_random_verse() -> str:
    "This function returns random verse"
    r_book_choice = random.choice(list(Book))
    r_book = bible_books_eng[str(r_book_choice)[5:].capitalize()]
    r_chapter = random.randint(1, bible.get_number_of_chapters(r_book_choice))
    r_verse = random.randint(1, bible.get_number_of_verses(r_book_choice, r_chapter))
    verse_text = find_verse(r_book, r_chapter, r_verse)
    book_name = list(bible_books.keys())[list(bible_books.values()).index(r_book)]
    return f"{verse_text} <{book_name} | {r_chapter}장 | {r_verse}절>"

#구글 api 이용하여 검색하는 함수
def google_search(api_key, search_engine_id, query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': query
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


#명령어 처리
def process_command(command : str):
    """
    This function processes command
    """
    sliced_command = command.split("-") 
    # example : ['mode ', 'r']
    # index 0 = method, 1 = option 1, 2 = option 2
    
    if 'mode ' == sliced_command[0]:
        if 'f' == sliced_command[1]:
            #find mode 구현
            user_book = input("책 : ")
            user_chapter = input("장 : ")
            user_verse = input("절 : ")
            print(find_verse(user_book, user_chapter, user_verse))
        elif 'r' == sliced_command[1]:
            #random mode 3번 출력
            for i in range(3):
                print(void_random_verse(),f"[{day[i]}]")
        elif 'l' == sliced_command[1]:
            #list mode 구현 (모든 언어 표현 가능하게 translate 를 이용해 구현하기)
            if 'e' == sliced_command[2]:
                #eng list 출력
                for book in bible_books_eng.keys():
                    print(f"{book}"),
            else:
                #korean list 출력
                for book in bible_books.keys():
                    print(f"{book}"),
        elif 's' == sliced_command[1]:
            query = input("검색 : ")
            results = google_search(api_key, search_engine_id, query)
            for item in results.get('items', []):
                print(f"Title: {item.get('title')}")
                print(f"Link: {item.get('link')}")
                print(f"Snippet: {item.get('snippet')}\n")
    elif 'exit' == command:
        #프로그램 종료
        exit()
    elif 'clear' == command:
        #콘솔 정리
        os.system('cls' if os.name == 'nt' else 'clear')
    elif command == 'help':
            print("""
            find mode : 원하는 구절을 찾고 싶을 때 [mode -f]
            search mode : 관련 정보 검색하고 싶을 때 [mode -s]
            random mode : 하루에 묵상할 3개의 구절을 찾고 싶을 때 [mode -r]
            list mode : 성경의 list를 보고 싶을 때 [mode -l] 영어 모드 -> mode -l -e
            exit : 프로그램을 종료할 때 [exit]
            """)
    else:
        print(f"{command} : 명령어가 존재하지 않습니다.\n'help'로 명령어 목록을 확인해 주세요")

#MAIN
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
        user_command = input(": ")
        process_command(user_command)
