import argparse
import itertools
import string

def flags():
    parser = argparse.ArgumentParser()

    parser.add_argument("least_chars", help="The minimum amount characters in the password", type=int)
    parser.add_argument("most_chars", help="The maximum amount characters in the password", type=int)
    parser.add_argument("chars_set", help="The possible types of characters in the password", type=str)

    group_VerQuiet = parser.add_mutually_exclusive_group(required=True)
    group_VerQuiet.add_argument("-v", "--verbose", help="Produces a verbose output", action="store_true")
    group_VerQuiet.add_argument("-q", "--quiet", help="Produces a quiet output", action="store_true")
    group_VerQuiet.add_argument("-dq", "--dead_quiet", help="Produces a dead quiet output \
        (not recommended as it does not ask for confirmation)", action="store_true")
    parser.add_argument("-o", "--output", help="Output result to a file", type=str)


    args = parser.parse_args()

    if args.verbose and args.output:
        parser.error("Verbose and output argument selected at the same time")

    return args

def permutations(args, arg_name):
    """Takes all args and then splits it into least, most, chars for use"""
    least = args.least_chars
    most = args.most_chars
    char = args.chars_set

    if args.output is str:
        output_file = args.output 

    else:
        output_file = False

    
    if arg_name.lower() in ["verbose"]:
        if least == most:
            print(f"There are {len(char) ** most} possible combinations")
        else:
            temp, loop_num = 0, 0
            for _ in range(least, most + 1):
                temp += len(char) ** (least + loop_num)
                loop_num += 1
            print(f"There are {temp} possible combinations")
            del temp, loop_num

        confirm = input("Would you like to list all of them? (Y/N): ")

        if confirm.lower() in ["y", "yes"]:
            for i in range(least, most + 1):
                for i in itertools.product(char, repeat=i):
                    print(i)
        elif confirm.lower() in ["n", "no"]:
            exit()
    
    elif arg_name.lower() in ["quiet"]:
        if least == most:
            temp = len(char) ** most
            confirm = input(f"{temp} possible combinations (Y/N): ")

        else:
            temp, loop_num = 0, 0
            for _ in range(least, most + 1):
                temp += len(char) ** (least + loop_num)
                loop_num += 1
            confirm = input(f"{temp} possible combinations (Y/N): ")
            del loop_num

        if confirm.lower() in ["y", "yes"]:
            if output_file: #FIXME For some reason even when told to use a different file name it still saves as ample?
                with open(output_file, "w+") as f:
                    for i in range(least, most + 1):
                        for comb in itertools.product(char, repeat=i):
                            f.write("".join(comb))
                            f.write("\n")
                            #TODO Remember to somehow tell the user that it is x% done.
                    f.close()

            else:
                with open("ample_passwds.txt", "w+") as f:
                    for i in range(least, most + 1):
                        for comb in itertools.product(char, repeat=i):
                            f.write("".join(comb))
                            f.write("\n")
                            # Here too
                    f.close()

        elif confirm.lower() in ["n", "no"]:
            exit()
            
    elif arg_name.lower() in ["dead_quiet"]:
        if output_file:
            with open(output_file, "w+") as f:
                for i in range(least, most + 1):
                    for comb in itertools.product(char, repeat=i):
                        f.write("".join(comb))
                        f.write("\n")
                f.close()
            exit()
        
        else:
            with open("ample_passwds.txt", "w+") as f:
                for i in range(least, most + 1):
                    for comb in itertools.product(char, repeat=i):
                        f.write("".join(comb))
                        f.write("\n")
                f.close()
            exit()


def argument_handler(args):
    """Handles arguments given to it"""

    if args.verbose:
        permutations(args, "verbose")

    elif args.quiet:
        permutations(args, "quiet")
    
    elif args.dead_quiet:
        permutations(args, "dead_quiet")


if __name__ == "__main__":
    args = flags()
    argument_handler(args)
