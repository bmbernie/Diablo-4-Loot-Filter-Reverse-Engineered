import base64
import diablo_4_loot_filter_pb2

MAX_FILTER_NAME_LENGTH = 24

def validate_filter_name(name: str) -> None:
    if len(name) > MAX_FILTER_NAME_LENGTH:
        raise ValueError(
            f"Filter name is too long: {len(name)} characters. "
            f"Maximum is {MAX_FILTER_NAME_LENGTH}."
        )

def make_filter(name: str) -> str:
    f = diablo_4_loot_filter_pb2.LootFilter()
    f.name = name
    f.field_3 = 4
    f.field_4 = 4
    return base64.b64encode(f.SerializeToString()).decode("ascii")

f = diablo_4_loot_filter_pb2.LootFilter()
f.name = "Minimum Viable Filter"
f.field_3 = 4
f.field_4 = 1

encoded = f.SerializeToString()
export_string = base64.b64encode(encoded).decode("ascii")

print(export_string)

f = diablo_4_loot_filter_pb2.LootFilter()

# top-level metadata
f.name = "Single Rule Test With a long name, too long"
f.field_3 = 4
f.field_4 = 4

# create one rule
rule = f.rules.add()

rule.name = "show all rule"

# RuleAction.SHOW_ITEM = 0
rule.action_type = 0

# ARGB red
rule.color = 0xffff0000

rule.enabled = True

# serialize
binary = f.SerializeToString()

# export format
encoded = base64.b64encode(binary).decode("ascii")

print(encoded)

test_names = [
    "é" * 24,   # 24 characters, 48 UTF-8 bytes
    "é" * 25,
    "🔥" * 24, # 24 characters, 96 UTF-8 bytes
    "🔥" * 25,
    ]

for name in test_names:
    print()
    print(f"Name: {name!r}")
    print(f"Characters: {len(name)}")
    print(f"UTF-8 bytes: {len(name.encode('utf-8'))}")
    print(make_filter(name))

print()
print(make_filter("Привет"))