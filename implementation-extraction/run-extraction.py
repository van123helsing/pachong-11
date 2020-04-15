import sys


def main():
    if len(sys.argv) > 1:
        ABC = sys.argv[1]
        if ABC == 'A':
            exec(open('regular-expression.py').read())
        elif ABC == 'B':
            exec(open('XPath.py').read())
        elif ABC == 'C':
            exec(open('RoadRunner.py').read())
        else:
            print("Kot parameter morate vnesti eno izmed črk A, B, C")
    else:
        print("Kot parameter morate vnesti eno izmed črk A, B, C")


if __name__ == "__main__":
    main()
