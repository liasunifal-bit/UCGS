# Fix: replace \\\\ ' with \\ ' at both positions around 'visualizar'
filepath = r"c:\Users\maria\Downloads\antigravity lias\back.end dashboard\site nevo.HTML"

with open(filepath, 'rb') as f:
    data = bytearray(f.read())

# Position 2201642-2201644: \\ \\ ' -> should be \\ '
# Position 2201655-2201657: \\ \\ ' -> should be \\ '

# Before 'visualizar': bytes at 2201642,2201643,2201644 = \\, \\, '
# We want: \\, '  (remove one backslash)

# After 'visualizar': bytes at 2201655,2201656,2201657 = \\, \\, '
# We want: \\, '  (remove one backslash)

# Remove byte at 2201643 (second backslash before 'visualizar')
# and byte at 2201656 (second backslash after 'visualizar')
# Note: after first removal, second position shifts by -1

# Remove at position 2201643 first
del data[2201643]
# After deletion, the second \\ is now at 2201654 (was 2201656, shifted by -1 for del, then -1 more)
del data[2201654]

with open(filepath, 'wb') as f:
    f.write(data)

# Verify
with open(filepath, 'rb') as f:
    v = f.read()

idx = v.find(b"openRiskmapModal", 2190000)
if idx >= 0:
    chunk = v[idx:idx+55]
    print(f"Result: {chunk}")
    # Check the bytes around visualizar
    offset = idx + len(b"openRiskmapModal(this, ")
    print(f"Bytes: {[v[offset+i] for i in range(20)]}")
    print("Expected: [92, 39, 118, ...visualizar..., 92, 39, 41]")
    if v[offset] == 92 and v[offset+1] == 39:
        print("SUCESSO! Escaping correto: \\' antes de visualizar")
    else:
        print("FALHA: escaping ainda incorreto")
