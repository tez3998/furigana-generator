import argparse
import sys

from furigana_generator import FuriganaGenerator
from user_dictionary import UserDictionary

def error(message: str) -> None:
    print(message)
    sys.exit(1)


def accept_input_continuously(user_dic_path: str) -> None:
    EXIT_FLAGS: list[str] = ["q", "Q"]
    furigana_generator: FuriganaGenerator = FuriganaGenerator(user_dic_path=user_dic_path)

    print("Input q or Q to exit.")

    while True:
        print("INPUT >", end="")
        input_text: str = input()
        if input_text in EXIT_FLAGS:
            sys.exit(0)
        else:
            output_text: str = furigana_generator.generate(text=input_text)
            print(f"OUTPUT>{output_text}\n")


def main() -> None:
    MIN_NUM_ARGS: int = 2

    arg_parser: argparse.ArgumentParser = argparse.ArgumentParser()
    arg_parser.add_argument("-c", "--continued", action="store_true", help="enter continuous input mode")
    arg_parser.add_argument("-a", "--add", action="store_true", help="flag of entry addiotion to user dictionary")
    arg_parser.add_argument("-w", "--word", help="specify word")
    arg_parser.add_argument("-p", "--part", help="specify part of speech of word")
    arg_parser.add_argument("-r", "--reading", help="specify reading of word")

    if len(sys.argv) < MIN_NUM_ARGS:
        arg_parser.print_usage()
        sys.exit(1)

    user_dictionary: UserDictionary = UserDictionary()
    arg1: str = sys.argv[1]

    if arg1[0] != "-": # in case of no option
        furigana_generator: FuriganaGenerator = FuriganaGenerator(user_dic_path=user_dictionary.get_user_dictionary_path())
        input_text: str = arg1
        output_text: str = furigana_generator.generate(text=input_text)
        print(output_text)
    else:
        args: argparse.Namespace = arg_parser.parse_args()

        if args.continued: # in case of continuous input mode
            accept_input_continuously(user_dic_path=user_dictionary.get_user_dictionary_path())
        elif args.add:
            if args.word == None:
                error(message="Word not specified. Use -w or --word option.")

            if args.part == None:
                error(message="Part of word not specified. Use -p or --part option.")

            if args.reading == None:
                error(message="Reading of word not specified. Use -r or --reading option.")
            
            user_dictionary.add_entry(word=args.word, part_of_speech=args.part, reading=args.reading)
            print("New entry added.")


if __name__ == "__main__":
    main()