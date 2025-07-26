
import re
from pathlib import Path

def extract_immediates(text: str):
    immediates = []

    # 1) AT&T syntax like: cmpb $0x63, %al  or  cmp $0x63,%al
    patt_att_imm_al = re.compile(r'\bcmp[b]?\s+\$?0x([0-9a-fA-F]+)\s*,\s*%?al\b')
    # 2) AT&T syntax reversed: cmp %al, $0x63  (rare, but handle it)
    patt_att_al_imm = re.compile(r'\bcmp[b]?\s+%?al\s*,\s*\$?0x([0-9a-fA-F]+)\b')
    # 3) Intel syntax like: cmp al, 0x63
    patt_intel_al_imm = re.compile(r'\bcmp\s+al\s*,\s*0x([0-9a-fA-F]+)\b')
    # 4) Intel syntax reversed: cmp 0x63, al
    patt_intel_imm_al = re.compile(r'\bcmp\s+0x([0-9a-fA-F]+)\s*,\s*al\b')

    # 5) Raw hex bytes for `cmp al, imm8` which is: 0x3C <imm8>
    #    We try to capture "3c xx" across common dump spacings.
    patt_hex_cmp_al = re.compile(r'(?i)(?<![0-9a-fA-F])3c[\s]*([0-9a-fA-F]{2})(?![0-9a-fA-F])')

    # Collect in file order; keep all to allow later heuristics.
    for m in patt_att_imm_al.finditer(text):
        immediates.append(int(m.group(1), 16))
    for m in patt_att_al_imm.finditer(text):
        immediates.append(int(m.group(1), 16))
    for m in patt_intel_al_imm.finditer(text):
        immediates.append(int(m.group(1), 16))
    for m in patt_intel_imm_al.finditer(text):
        immediates.append(int(m.group(1), 16))
    for m in patt_hex_cmp_al.finditer(text):
        immediates.append(int(m.group(1), 16))

    return immediates

def to_printable(byte_val: int) -> str:
    try:
        ch = chr(byte_val)
        # Keep typical printable ASCII; replace others with escaped form
        if 32 <= byte_val <= 126:
            return ch
        return f'\\x{byte_val:02x}'
    except Exception:
        return f'\\x{byte_val:02x}'

def find_flag_candidates(s: str):
    # Common CTF flag shapes; adjust as needed
    patterns = [
        r'ctf[a-z0-9]*\{[^}\n]{3,200}\}',
        r'flag\{[^}\n]{3,200}\}',
        r'ctf4b\{[^}\n]{3,200}\}',
    ]
    found = set()
    for p in patterns:
        for m in re.finditer(p, s, flags=re.IGNORECASE):
            found.add(m.group(0))
    # sort stable: shorter first, then lexicographic
    return sorted(found, key=lambda x: (len(x), x.lower()))

def main(infile: str = "disasm.txt", out_flags: str = "/mnt/data/extracted_flags.txt"):
    path = Path(infile)
    if not path.exists():
        print(f"[!] Disassembly file not found: {path}")
        return

    text = path.read_text(errors="ignore")

    imms = extract_immediates(text)
    print(f"[i] Extracted {len(imms)} immediate bytes from CMP-with-AL patterns.")

    raw = ''.join(to_printable(b) for b in imms)
    print("[i] Preview of concatenated bytes (first 200 chars):")
    print(raw[:200])

    # Try to identify plausible flags inside the concatenated stream
    candidates = find_flag_candidates(raw)
    if candidates:
        print("\n[✓] Flag-like candidates found:")
        for c in candidates:
            print("  ", c)
        # save them
        Path(out_flags).write_text('\n'.join(candidates), encoding='utf-8')
        print(f"\n[i] Saved candidates to: {out_flags}")
    else:
        print("\n[!] No obvious flag-shaped substring found in the concatenated stream.")
        print("    You can open the generated preview and search manually, or refine the regex.")

if __name__ == "__main__":
    main()
