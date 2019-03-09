import os
import sys

if __name__ == "__main__":
    print('hello')
    print(os.environ)
    arguments={item.split('=')[0]:item.split('=')[1] for item in sys.argv[1:]}
    print(arguments)
