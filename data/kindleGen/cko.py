import sys
from bs4 import BeautifulSoup
import markdown


# def prettify(self, encoding=None, formatter="minimal", myTab=2): 
#     Tag.myTab= myTab # add a reference to it in the Tag class
#     if encoding is None:
#         return self.decode(True, formatter=formatter)
#     else:
#         return self.encode(encoding, True, formatter=formatter)

def read_content(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        return content

def write_content(file_path, content):
    with open(file_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    # If no arguments were provided, do nothing.
    if len(sys.argv) <= 1: 
        print("No file path arguments provided; do nothing.")
        exit(0)
    
    file_path = sys.argv[1]
    
    content = read_content(file_path)
    # pretty_content = BeautifulSoup(content, "lxml").prettify(indent_width = 4, formatter=None)
    # write_content(file_path, pretty_content)    
    html = markdown.markdown(content, tab_length=8)
    write_content(file_path, html)    