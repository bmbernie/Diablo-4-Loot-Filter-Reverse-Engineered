# README

## Diablo 4 Loot Filter Reverse Engineered

Research project focused on understanding and documenting the Diablo IV loot filter wire protocol.

## Features

- Decode loot filter payloads
- Encode loot filter payloads
- Base64 import/export support
- Protocol experimentation and analysis

## Requirements

- Python
  - protobuf
- Go
  - protoscope

## Usage

Decode a filter:

```bash
python lootfilter_parser.py $base64_encoded_loot_filter
```
```
1: {
  2: "Minimum Viable Filter"
  3: 4
  4: 4
}
```
Encode a filter:

```bash
python lootfilter_write_test.py
```
```
EhVNaW5pbXVtIFZpYWJsZSBGaWx0ZXIYBCAB
```
## Status

Work in progress.

Currently focused on:
- protocol structure analysis
- serialization/deserialization
- string encoding behavior
- compatibility testing with the game client

## Disclaimer

This project is for educational and interoperability research purposes only.

Diablo IV and related assets are property of Blizzard Entertainment.