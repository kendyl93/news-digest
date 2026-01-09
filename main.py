import sys
import feedparser

def main() -> None:
    print("Python:", sys.version.split()[0])
    print("feedparser:", feedparser.__version__)
    print("OK ✅")

if __name__ == "__main__":
    main()
