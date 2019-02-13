import sys

if __name__ == "__main__":
    print("[START SCRIPT]")

    # Check if script is part of pipe process
    if sys.stdin.isatty():
        # Script is called as a standalone
        print("stdin isatty")
        print 'Number of arguments:', len(sys.argv), 'arguments.'
        print 'Argument List:', str(sys.argv)
    else:
        # Script is part of pipe processing
        print("stdin NOT isatty")
        # Open stdin to process piped arguments; 
        # There are 2 methods processing the piped arguments
        # 1 - One at a time
        # 2 - Batch - Get all the lines of output as list of strings

        # Method 1 - Process each line of output one at a time.
        # for line in sys.stdin:
        #     print line

        # Method 2 - Get all the lines of output as list of strings
        data = sys.stdin.readlines()
        print data
        # Sample output of data:
        # ['yahoo world\n', '{"price": 1.22, "result": "success"}\n']

        
        

    # if sys.stdout.isatty():
    #     print("stdout isatty")
    # else:
    #     print("stdout NOT isatty")

    # When script is not part of pipe process
    #   stdin isatty
    #   stdout isatty
    # When script IS part of pipe process
    #   stdin NOT isatty
    #   stdout isatty


    print("[END SCRIPT]")