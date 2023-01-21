import jaconv
import pathlib
import regex
import sys

class UserDictionary:
    def __init__(self) -> None:
        self.__USER_DIC_PATH: str = r"../files/user_dictionary.csv"
        self.__PART_OF_SPEECH_PATH: str = r"../files/part_of_speech.txt"
        self.__part_of_speech_list: list[str] = []

        user_dic: pathlib.Path = pathlib.Path(self.__USER_DIC_PATH)
        user_dic.touch(exist_ok=True)

        with open(file=self.__PART_OF_SPEECH_PATH, encoding="utf8", mode="r") as f:
            for line in f:
                line = line.replace("\n", "")
                self.__part_of_speech_list.append(line)
    

    def add_entry(self, word: str, part_of_speech: str, reading: str) -> None:
        if not self.__is_part_of_speech(text=part_of_speech):
            self.__error(message=f"Part of Speech must be one of {self.__part_of_speech_list}.")
        if not self.__is_hiragana(text=reading):
            self.__error(message=f"Reading must be hiragana.")
        
        with open(file=self.__USER_DIC_PATH, encoding="utf8", mode="a") as dic:
            reading_katakana: str = jaconv.hira2kata(text=reading)
            entry: str = f"{word},{part_of_speech},{reading_katakana}\n"
            dic.write(entry)
        
    
    def get_user_dictionary_path(self) -> str:
        return self.__USER_DIC_PATH


    def __error(self, message: str) -> None:
        print(f"\n{message}")
        sys.exit(1)
    

    def __is_part_of_speech(self, text: str) -> bool:
        if text in self.__part_of_speech_list:
            return True
        else:
            return False
    

    def __is_hiragana(self, text: str) -> bool:
        hiragana_pattern: regex.Pattern[str] = regex.compile(r"\p{Script=Hiragana}+")
        
        for char in text:
            if hiragana_pattern.fullmatch(string=char) == None:
                return False
        return True
