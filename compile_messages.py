"""
Pure Python .po -> .mo compiler (no GNU gettext required).
Compiles all locale/*/LC_MESSAGES/django.po files.
"""
import struct
import os
import re

def parse_po(filepath):
    """Parse a .po file and return list of (msgid, msgstr) tuples."""
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    # Split into blocks separated by blank lines
    entries = []
    current_msgid = None
    current_msgstr = None
    in_msgid = False
    in_msgstr = False

    def unescape(s):
        """Unescape a .po string value."""
        # Remove surrounding quotes and handle escape sequences
        s = s.strip()
        if s.startswith('"') and s.endswith('"'):
            s = s[1:-1]
        s = s.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
        return s

    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip comments and empty lines between entries
        if line.startswith('#') or line == '':
            if in_msgstr and current_msgid is not None:
                # End of entry
                if current_msgid != '' or True:  # include header too
                    entries.append((current_msgid, current_msgstr))
                current_msgid = None
                current_msgstr = None
                in_msgid = False
                in_msgstr = False
            i += 1
            continue

        if line.startswith('msgid '):
            if in_msgstr and current_msgid is not None:
                entries.append((current_msgid, current_msgstr))
            current_msgid = unescape(line[6:])
            current_msgstr = None
            in_msgid = True
            in_msgstr = False

        elif line.startswith('msgstr '):
            current_msgstr = unescape(line[7:])
            in_msgid = False
            in_msgstr = True

        elif line.startswith('"') and in_msgid:
            current_msgid += unescape(line)

        elif line.startswith('"') and in_msgstr:
            current_msgstr += unescape(line)

        i += 1

    # Don't forget last entry
    if in_msgstr and current_msgid is not None:
        entries.append((current_msgid, current_msgstr))

    return entries


def compile_mo(entries, output_path):
    """
    Write a .mo file from a list of (msgid, msgstr) tuples.
    See GNU gettext .mo file format specification.
    """
    # Filter out entries with empty msgstr and skip fuzzy entries
    # Keep only entries where msgstr is non-empty (or it's the header with msgid='')
    valid = [(k, v) for k, v in entries if v is not None and (k == '' or v.strip() != '')]

    # Sort by msgid for binary search (required by spec)
    valid.sort(key=lambda x: x[0].encode('utf-8'))

    n = len(valid)
    # Header
    magic = 0x950412de  # little-endian magic number
    revision = 0
    # Offset positions:
    # After the header (7 * 4 bytes = 28 bytes), we store:
    # - n pairs of (length, offset) for original strings
    # - n pairs of (length, offset) for translated strings
    # - then the actual strings

    header_size = 28  # 7 integers * 4 bytes
    orig_table_offset = header_size
    trans_table_offset = orig_table_offset + n * 8
    strings_offset = trans_table_offset + n * 8

    # Encode all strings
    orig_encoded = [k.encode('utf-8') for k, v in valid]
    trans_encoded = [v.encode('utf-8') for k, v in valid]

    # Build string data blob
    offsets_orig = []
    offsets_trans = []
    blob = b''

    current_offset = strings_offset

    for s in orig_encoded:
        offsets_orig.append((len(s), current_offset))
        blob += s + b'\x00'
        current_offset += len(s) + 1

    for s in trans_encoded:
        offsets_trans.append((len(s), current_offset))
        blob += s + b'\x00'
        current_offset += len(s) + 1

    # Build the .mo file
    result = struct.pack('<I', magic)                    # magic
    result += struct.pack('<I', revision)                # revision
    result += struct.pack('<I', n)                       # number of strings
    result += struct.pack('<I', orig_table_offset)       # offset of originals table
    result += struct.pack('<I', trans_table_offset)      # offset of translations table
    result += struct.pack('<I', 0)                       # size of hash table (unused)
    result += struct.pack('<I', 0)                       # offset of hash table

    # Original string descriptors
    for length, offset in offsets_orig:
        result += struct.pack('<II', length, offset)

    # Translated string descriptors
    for length, offset in offsets_trans:
        result += struct.pack('<II', length, offset)

    # String data
    result += blob

    with open(output_path, 'wb') as f:
        f.write(result)

    print(f"  Compiled {n} entries -> {output_path}")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    locale_dir = os.path.join(base_dir, 'locale')

    for lang in os.listdir(locale_dir):
        po_path = os.path.join(locale_dir, lang, 'LC_MESSAGES', 'django.po')
        mo_path = os.path.join(locale_dir, lang, 'LC_MESSAGES', 'django.mo')
        if os.path.exists(po_path):
            print(f"Compiling {lang}...")
            entries = parse_po(po_path)
            compile_mo(entries, mo_path)

    print("\nAll .mo files compiled successfully!")


if __name__ == '__main__':
    main()
