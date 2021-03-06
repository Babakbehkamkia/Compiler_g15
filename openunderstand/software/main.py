from antlr4 import *
from gen.JavaParserLabeled import JavaParserLabeled
from gen.JavaLexer import JavaLexer
from metric import DSCmetric
import argparse


def main(args):

    stream = FileStream(args.file, encoding="utf8")
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parse_tree = parser.compilationUnit()

    my_listener = DSCmetric(args.file)

    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)


    d_use = my_listener.get_use
    # print("[\n\t{")
    # for k in d_use.keys():
    #     print(f"\t\t{k}", end=" : ")
    #     print(d_use[k])
    # print("\t}")
    # print("]")

    d_type = my_listener.get_type
    # print("[\n\t{")
    # for k in d_type.keys():
    #     print(f"\t\t{k}", end=" : ")
    #     print(d_type[k])
    # print("\t}")
    # print("]")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-n', '--file',
        help="Input source", default=r'A.java'
    )
    args = argparser.parse_args()
    main(args)
