import os
import pykakasi
import sys

class FuriganaGenerator:
    """
    A class generates a text with furigana.
    """
    def __init__(self) -> None:
        self.__DELIMITER: list[str] = ["。", "、", "？", ".", ",", "\n"]
        self.__kakasi: pykakasi.kakasi = pykakasi.kakasi()
    
    def generate(self, text: str) -> str:
        """
        generates a text with furigana from argument named text.
        """
        text_with_furigana: str = ""
        chunk: str = ""

        for char in text:
            # If there is a delimiter at the end of a phrase,
            # pykakasi covert the phrase to hiragana which includes the delimiter.
            # This behaior of pykakasi is unwanted for me
            # because this program uses hiragana which pykakashi generates as furigana,
            # and furigana should not include any deliminaters.
            # So, phrases should not include any deliminaters
            # when phrases are inputted to pykakashi.
            if char in self.__DELIMITER:
                if chunk != "":
                    text_with_furigana += self.__convert(text=chunk)
                    chunk = ""

                text_with_furigana += char
            else:
                chunk += char
        
        if chunk != "":
            text_with_furigana += self.__convert(text=chunk)

        return text_with_furigana
    

    def __convert(self, text: str) -> str:
        """
        convert the value of the argument named text to a text with furigana.
        """
        text_with_furigana: str = ""
        results: list[dict[str, str]] = self.__kakasi.convert(text=text)

        for result in results:
            original: str = result["orig"]
            hiragana: str = result["hira"]
            katakana: str = result["kana"]

            if (original != hiragana) and (original != katakana): # Text includes kanji
                text_with_furigana += f"{original}（{hiragana}）"
            else:
                text_with_furigana += original
        
        return text_with_furigana


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} [text]")
        sys.exit(1)

    generator: FuriganaGenerator = FuriganaGenerator()
    text_with_furigana: str = generator.generate(text=sys.argv[1])
    print(text_with_furigana)