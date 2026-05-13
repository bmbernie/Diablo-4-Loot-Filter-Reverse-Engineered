![image](assets/specific_unique_filter.jpg)

# Obtain Base64 Encoded Filter

1. From within Diablo 4, navigate to the Loot Filter menu.
2. Create a filter.
3. From the kebab menu (3 vertical dots), select **Export Filter**.

The filter contents are now stored in your clipboard.

# Examine Filter

1. Paste the filter into hexeditor.

~~~text
ClMKEmlzIFNwZWNpZmljIFVuaXF1ZRAAHQAA//8iNAgIFTdoAwAViOcTABWrqx0AFdW6JwAVuHsFABUlbh8AFZO9JgAVWV8DABXSqx0AFbQQJAAoARIWU3BlY2lmaWMgVW5pcXVlIEZpbHRlchgFIAI=
~~~

Note: Your filter string will be different unless you created an identical filter.

Inspection shows that the filter contents are Base64-encoded, presumably to simplify sharing on the web. An interesting detail is that the game does not appear to use URL-safe Base64 encoding.

# Extract and Save Raw Filter

Windows:
~~~PowerShell
[System.IO.File]::WriteAllBytes((Join-Path (Get-Location) "filter_test_case.bin"), [System.Convert]::FromBase64String($(Get-Clipboard)))
~~~

macOS:
~~~sh
pbpaste | base64 --decode > filter_test_case.bin
~~~

Linux:
~~~sh
xclip -selection clipboard -o | base64 --decode > filter_test_case.bin
~~~

# Raw Filter Output

~~~hexdump
00000000  0A 53 0A 12 69 73 20 53 70 65 63 69 66 69 63 20  |.S..is Specific |
00000010  55 6E 69 71 75 65 10 00 1D 00 00 FF FF 22 34 08  |Unique.....ÿÿ"4.|
00000020  08 15 37 68 03 00 15 88 E7 13 00 15 AB AB 1D 00  |..7h....ç...««..|
00000030  15 D5 BA 27 00 15 B8 7B 05 00 15 25 6E 1F 00 15  |.Õº'..¸{...%n...|
00000040  93 BD 26 00 15 59 5F 03 00 15 D2 AB 1D 00 15 B4  |.½&..Y_...Ò«...´|
00000050  10 24 00 28 01 12 16 53 70 65 63 69 66 69 63 20  |.$.(...Specific |
00000060  55 6E 69 71 75 65 20 46 69 6C 74 65 72 18 05 20  |Unique Filter.. |
00000070  02                                               |.|
~~~

# Identify the Data

Unlike many binary serialization or container formats, Protocol Buffers (protobufs) do not embed a canonical file 
signature or “[magic bytes](https://en.wikipedia.org/wiki/List_of_file_signatures)” sequence that uniquely identifies the payload 
type. As a result, protobuf blobs cannot be reliably classified through conventional file-signature analysis such as the `file` command; as demonstrated below.

~~~sh
file specific_unique_filter.bin 
~~~

~~~text
specific_unique_filter.bin: data
~~~

However, the protobuf wire format has several recognizable structural characteristics that make it identifiable to 
anyone familiar with protobuf encoding semantics. These include recurring field tags encoded as 
`(field_number << 3) | wire_type`, length-delimited UTF-8 string segments, varint-encoded integers, and predictable 
fixed-width primitive encodings (`fixed32`, `fixed64`). Repeated tag/value patterns and valid wire-type transitions are 
often sufficient to distinguish protobuf data from arbitrary binary blobs.

For analysts unfamiliar with protobuf internals, heuristic decoding is still feasible. Providing the raw hexdump or 
extracted payload to an LLM-based analysis tool can often produce plausible protobuf interpretations, including 
candidate field boundaries, wire types, nested message structures, and inferred schema fragments.  