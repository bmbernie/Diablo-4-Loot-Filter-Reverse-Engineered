import sys
import base64

def isBase64(s):
    try:
        return base64.b64encode(base64.b64decode(s)).decode() == s
    except Exception as e:
        return False

def main():
    argc = len(sys.argv)

    if not sys.stdin.isatty():
        input_bytes = sys.stdin.read()
    else:
        input_bytes = sys.argv[1]

    if not isBase64(sys.argv[1]):
        print("".join(f"{b:02X}" for b in input_bytes))
    else:
        raw_bytes = base64.b64decode(input_bytes)
        print("".join(f"{b:02X}" for b in raw_bytes))

    return

if __name__ == "__main__":
    main()