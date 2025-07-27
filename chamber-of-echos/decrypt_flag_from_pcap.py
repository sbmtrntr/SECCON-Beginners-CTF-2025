from scapy.all import rdpcap, Raw, IP, ICMP
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

PCAP_FILE = "echo_replies.pcap"
KEY_HEX = "546869734973415365637265744b6579"
KEY = bytes.fromhex(KEY_HEX)
BLOCK_SIZE = 16

def decrypt_chunk(enc_chunk: bytes) -> str:
    cipher = AES.new(KEY, AES.MODE_ECB)
    decrypted = cipher.decrypt(enc_chunk)
    try:
        return unpad(decrypted, BLOCK_SIZE).decode()
    except:
        return decrypted.decode(errors="ignore")

def main():
    packets = rdpcap(PCAP_FILE)
    chunks = set()

    for pkt in packets:
        if IP in pkt and ICMP in pkt and pkt[ICMP].type == 0 and Raw in pkt:
            chunks.add(bytes(pkt[Raw].load))

    print(f"[+] Collected {len(chunks)} unique encrypted chunks")

    decrypted_parts = []
    for chunk in chunks:
        plain = decrypt_chunk(chunk)
        # フォーマットは "i|<flag_part>"
        if len(plain) >= 2 and plain[1] == '|':
            try:
                idx = int(plain[0])
                decrypted_parts.append((idx, plain[2:]))
            except:
                pass

    decrypted_parts.sort(key=lambda x: x[0])
    flag = "".join(part[1] for part in decrypted_parts)

    print("[+] Recovered Flag:")
    print(flag)

if __name__ == "__main__":
    main()
