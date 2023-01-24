import jaconv
import os
import regex
from janome.tokenizer import Tokenizer, Token

class FuriganaGenerator:
    def __init__(self, user_dic_path: str) -> None:
        user_dic_path = os.path.abspath(path=user_dic_path)
        
        if os.path.getsize(user_dic_path) == 0:
            self.__tokenizer: Tokenizer = Tokenizer()
        else:
            self.__tokenizer: Tokenizer = Tokenizer(udic=user_dic_path,
                                                    udic_type="simpledic",
                                                    udic_enc="utf8")
        self.__open_tag: str = "{"
        self.__close_tag: str = "}"


    def generate(self, text: str) -> str:
        tokens: list[Token] = list(self.__tokenizer.tokenize(text=text))
        text_with_furigana: str = ""
        
        for token in tokens:
            surface: str = token.surface

            if self.__include_kanji(text=surface):
                # furigana: str = jaconv.kata2hira(token.reading)
                # text_with_furigana += f"{surface}{self.__open_tag}{furigana}{self.__close_tag}"
                text_with_furigana += self.__attach_furigana(token=token)
            else:
                text_with_furigana += surface
        
        return text_with_furigana
    

    def __include_kanji(self, text: str) -> bool:
        kanji_pattern: regex.Pattern[str] = regex.compile(r"\p{Script=Han}")
        
        if kanji_pattern.search(string=text) == None:
            return False
        else:
            return True
    

    def __is_hiragana(self, char: str) -> bool:
        pattern = regex.compile(r"\p{Script=Hiragana}")
        
        if pattern.fullmatch(string=char) == None:
            return False
        else:
            return True
    

    def __attach_furigana(self, token: Token) -> str:
        text_with_furigana: str = ""
        surface: str = token.surface
        si: int = 0 # index of surface
        reading: str = token.reading
        ri: int = 0 # index of reading
        char: str = ""
        chunk: str = ""
        chunk_reading: str = ""
        prev_char_was_kanji: bool

        char = surface[si]
        if self.__include_kanji(text=char):
            prev_char_was_kanji = True
            chunk_reading = jaconv.kata2hira(text=reading[ri])
        else:
            prev_char_was_kanji = False
        chunk = char
        si += 1
        ri += 1

        while (ri < len(reading)) and (si < len(surface)):
            char = surface[si]
            if self.__include_kanji(text=char):
                if prev_char_was_kanji: # in the middle of kanji chunk
                    chunk += char
                else: # at the start of kanji chunk
                    text_with_furigana += chunk
                    chunk = char
                    prev_char_was_kanji = True
            else:
                if prev_char_was_kanji: # at the start of no kanji chunk
                    old_ri: int = ri
                    while (ri < len(reading)) and (si < len(surface)):
                        r: str = reading[ri]
                        if self.__is_hiragana(char=char):
                            r = jaconv.kata2hira(text=r)

                        if (char == r) and (len(chunk_reading) + ri - old_ri > 0): # kanji must have one or more reading characters.
                            chunk_reading += jaconv.kata2hira(text=reading[old_ri: ri])
                            break
                        else:
                            ri += 1
                    text_with_furigana += f"{chunk}{self.__open_tag}{chunk_reading}{self.__close_tag}"
                    chunk = char
                    chunk_reading = ""
                    prev_char_was_kanji = False
                else: # in the middle of no kanji chunk
                    chunk += char
                ri += 1
            si += 1

        if prev_char_was_kanji:
            chunk_reading += jaconv.kata2hira(text=reading[ri: len(reading)])
            text_with_furigana += f"{chunk}{self.__open_tag}{chunk_reading}{self.__close_tag}"
        else:
            text_with_furigana += chunk

        return text_with_furigana