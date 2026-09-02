from pathlib import Path
import os

def main():
    for i in range(1, 11):
        filename = f"resume_{i}.json"
        # Creates an empty file without writing text
        open(filename, "a").close()

if __name__ == "__main__":
    main()