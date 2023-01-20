import sys

from furigana_generator import FuriganaGenerator

def main():
    generator: FuriganaGenerator = FuriganaGenerator()
    input_text: str = sys.argv[1]
    output_text: str = generator.generate(text=input_text)
    print(output_text, end="\n")


if __name__ == "__main__":
    main()