import sys
import base64
import struct

WIRE_VARINT = 0
WIRE_64BIT = 1
WIRE_LENGTH_DELIMITED = 2
WIRE_32BIT = 5

def get_encoded_filter():
    if len(sys.argv) != 2:
        print("Usage: ")
        print("    python lootfilter_decoded.py $LOOT_FILTER")
        return ""
    elif len(sys.argv) > 1:
        return sys.argv[1]

def read_varint(data, offset):
    result = 0
    shift = 0

    while True:
        b = data[offset]
        offset += 1

        result |= (b & 0x7F) << shift

        if not (b & 0x80):
            break

        shift += 7

    return result, offset


def is_probably_text(b):
    try:
        s = b.decode("utf-8")

        printable = sum(
            1 for c in s
            if c.isprintable() or c.isspace()
        )

        return printable / max(len(s), 1) > 0.85
    except:
        return False

def parse_message(data, indent=0):
    offset = 0

    while offset < len(data):
        try:
            tag, offset = read_varint(data, offset)
        except:
            print(" " * indent + "<parse error>")
            return

        field_number = tag >> 3
        wire_type = tag & 0x7
        prefix = " " * indent
        print(f"{prefix}{field_number}: ", end="")

        # -------------------------
        # VARINT
        # -------------------------
        if wire_type == WIRE_VARINT:

            value, offset = read_varint(data, offset)
            print(value)

        # -------------------------
        # LENGTH DELIMITED
        # -------------------------
        elif wire_type == WIRE_LENGTH_DELIMITED:

            length, offset = read_varint(data, offset)

            value = data[offset:offset + length]
            offset += length

            # Try UTF-8
            if is_probably_text(value):

                try:
                    text = value.decode("utf-8")
                    print(f'"{text}"')

                except:
                    print(value)

            else:
                print("{")

                # recurse into nested message
                parse_message(value, indent + 2)

                print(prefix + "}")

        # -------------------------
        # 32-bit
        # -------------------------
        elif wire_type == WIRE_32BIT:

            raw = data[offset:offset + 4]
            offset += 4
            value = struct.unpack("<I", raw)[0] # little endian unsigned int32
            print(f"0x{value:08x}")

        # -------------------------
        # 64-bit
        # -------------------------
        elif wire_type == WIRE_64BIT:
            raw = data[offset:offset + 8]
            offset += 8
            value = struct.unpack("<I", raw)[0]  # little-endian unsigned int64
            print(f"0x{value:016x}")

        else:
            print(f"<unsupported wire type {wire_type}>")
            return


def main():
    encoded_loot_filter = get_encoded_filter()

    if len(encoded_loot_filter) == 0:
        print("Empty Loot filter, exiting...")
        sys.exit(0)
    try:
        decoded_lootfilter = base64.b64decode(encoded_loot_filter)
        parse_message(decoded_lootfilter)
    except Exception as e:
        print(f"Decode error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()