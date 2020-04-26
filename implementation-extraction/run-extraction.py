import sys
import XPath
import regular_expression
import RoadRunner


def main():
    if len(sys.argv) > 1:
        ABC = sys.argv[1]
        if ABC == 'A':
            regular_expression.process()
        elif ABC == 'B':
            XPath.process()
        elif ABC == 'C':
            RoadRunner.process()
        else:
            print("Kot parameter morate vnesti eno izmed črk A, B, C")
    else:
        print("Kot parameter morate vnesti eno izmed črk A, B, C")


if __name__ == "__main__":
    main()
