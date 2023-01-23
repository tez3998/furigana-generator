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
    

    def __is_hiragana(self, char) -> bool:
        pattern = regex.compile(r"\p{Script=Hiragana}")
        
        if pattern.fullmatch(string=char) == None:
            return False
        else:
            return True
    

    def __attach_furigana(self, token: Token) -> str:
        stack: list[str] = []
        surface: str = token.surface
        reading: str = token.reading
        text_with_furigana: str = ""
        chunks: list[str] = self.__separete_kanji_from_other_char_types(text=surface)
        stack: list[str] = []

        reversed_chunks: list[str] = list(reversed(chunks))
        reading_index: int = len(reading) - 1
        for ci, chunk in enumerate(reversed_chunks):
            if self.__include_kanji(text=chunk):
                kanji: str = chunk

                if ci == len(reversed_chunks) - 1:
                    furigana: str = jaconv.kata2hira(reading[0: reading_index + 1])
                    stack.append(kanji + self.__open_tag + furigana + self.__close_tag)
                else:
                    next_chunk: str = reversed_chunks[ci + 1]
                    next_char: str = next_chunk[len(next_chunk) - 1]
                    old_reading_index: str = reading_index

                    while True:
                        char: str
                        if self.__is_hiragana(char=next_char):
                            char = jaconv.kata2hira(text=reading[reading_index])
                        else:
                            char = reading[reading_index]

                        if char == next_char:
                            furigana: str = jaconv.kata2hira(reading[reading_index + 1: old_reading_index + 1])
                            stack.append(kanji + self.__open_tag + furigana + self.__close_tag)
                            break
                        else:
                            reading_index -= 1
            else:
                no_kanji: str = chunk

                stack.append(no_kanji)
                reading_index -= len(no_kanji)

        for item in reversed(stack):
            text_with_furigana += item

        return text_with_furigana
    

    def __separete_kanji_from_other_char_types(self, text: str) -> list[str]:
        chunks: list[str] = []
        prev_char_was_kanji: bool
        chunk: str

        if self.__include_kanji(text=text[0]):
            prev_char_was_kanji = True
        else:
            prev_char_was_kanji = False
        chunk = text[0]

        if len(text) == 1:
            chunks.append(chunk)
            return chunks
        else:
            for char in text[1:]:
                include_kanji: bool = self.__include_kanji(text=char)

                if prev_char_was_kanji and (not include_kanji):
                    chunks.append(chunk)
                    chunk = char
                    prev_char_was_kanji = False
                elif (not prev_char_was_kanji) and include_kanji:
                    chunks.append(chunk)
                    chunk = char
                    prev_char_was_kanji = True
                else:
                    chunk += char
            chunks.append(chunk)
            return chunks