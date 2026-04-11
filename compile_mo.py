"""Compile .po files to .mo using Python's built-in msgfmt logic."""
import struct
import os
import array


def compile_po_to_mo(po_path, mo_path):
    messages = {}
    current_msgid = None
    current_msgstr = None
    in_msgid = False
    in_msgstr = False

    with open(po_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('msgid '):
                if current_msgid is not None and current_msgstr is not None:
                    messages[current_msgid] = current_msgstr
                in_msgid = True
                in_msgstr = False
                current_msgid = line[6:].strip('"')
                current_msgstr = None
            elif line.startswith('msgstr '):
                in_msgid = False
                in_msgstr = True
                current_msgstr = line[7:].strip('"')
            elif line.startswith('"') and line.endswith('"'):
                s = line[1:-1]
                if in_msgid:
                    current_msgid = (current_msgid or '') + s
                elif in_msgstr:
                    current_msgstr = (current_msgstr or '') + s
            elif not line or line.startswith('#'):
                if current_msgid is not None and current_msgstr is not None:
                    messages[current_msgid] = current_msgstr
                    current_msgid = None
                    current_msgstr = None
                in_msgid = False
                in_msgstr = False
        if current_msgid is not None and current_msgstr is not None:
            messages[current_msgid] = current_msgstr

    # Process escape sequences
    def unescape(s):
        return s.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')

    # Build sorted keys (empty string = header goes first)
    keys = sorted(messages.keys())

    # Build .mo binary
    offsets = []
    ids_data = bytearray()
    strs_data = bytearray()
    key_start_len = []
    val_start_len = []

    for key in keys:
        val = messages[key]
        kb = unescape(key).encode('utf-8')
        vb = unescape(val).encode('utf-8')
        key_start_len.append((len(ids_data), len(kb)))
        ids_data += kb + b'\x00'
        val_start_len.append((len(strs_data), len(vb)))
        strs_data += vb + b'\x00'

    n = len(keys)
    header_size = 28
    orig_table_off = header_size
    trans_table_off = header_size + n * 8
    ids_start = header_size + n * 16
    strs_start = ids_start + len(ids_data)

    output = struct.pack(
        'Iiiiiii',
        0x950412de,  # magic
        0,           # revision
        n,
        orig_table_off,
        trans_table_off,
        0, 0         # hash
    )

    for offset, length in key_start_len:
        output += struct.pack('ii', length, ids_start + offset)
    for offset, length in val_start_len:
        output += struct.pack('ii', length, strs_start + offset)

    output += bytes(ids_data) + bytes(strs_data)

    with open(mo_path, 'wb') as f:
        f.write(output)
    return n


if __name__ == '__main__':
    for lang in ['ru', 'tr', 'ar', 'en']:
        po = os.path.join('locale', lang, 'LC_MESSAGES', 'django.po')
        mo = os.path.join('locale', lang, 'LC_MESSAGES', 'django.mo')
        if os.path.exists(po):
            n = compile_po_to_mo(po, mo)
            print(f'{lang}: {n} messages compiled -> {mo}')
        else:
            print(f'{lang}: {po} not found')
