from scapy.all import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import time

TARGET_IP = "chamber-of-echos.challenges.beginners.seccon.jp"
KEY = b"ThisIsASecretKey"
BLOCK_SIZE = 16
RETRY_COUNT = 100
SNIFF_TIMEOUT = 10

received_chunks = set()

def decrypt_block(enc_block: bytes) -> str:
    cipher = AES.new(KEY, AES.MODE_ECB)
    decrypted = cipher.decrypt(enc_block)
    try:
        return unpad(decrypted, BLOCK_SIZE).decode(errors="ignore")
    except ValueError:
        return decrypted.decode(errors="ignore")

def packet_handler(pkt):
    if IP in pkt and ICMP in pkt and Raw in pkt:
        if pkt[IP].src == TARGET_IP and pkt[ICMP].type == 0:  # Echo Reply
            received_chunks.add(bytes(pkt[Raw].load))

def send_pings():
    for seq in range(RETRY_COUNT):
        pkt = IP(dst=TARGET_IP)/ICMP(type=8, id=0x1234, seq=seq)
        send(pkt, verbose=0)
        time.sleep(0.02)

def main():
    print(f"[+] Sending {RETRY_COUNT} ICMP Echo Requests to {TARGET_IP}...")
    send_pings()

    print(f"[+] Sniffing for {SNIFF_TIMEOUT} seconds (without BPF filter)...")
    sniff(timeout=SNIFF_TIMEOUT, prn=packet_handler)

    print(f"[+] Collected {len(received_chunks)} unique encrypted chunks.")

    decrypted_parts = []
    for chunk in received_chunks:
        plain = decrypt_block(chunk)
        if len(plain) >= 2 and plain[1] == '|':
            try:
                idx = int(plain[0])
                text = plain[2:]
                decrypted_parts.append((idx, text))
            except ValueError:
                continue

    decrypted_parts.sort(key=lambda x: x[0])
    flag = "".join(part[1] for part in decrypted_parts)
    print("[+] Recovered Flag:")
    print(flag)

if __name__ == "__main__":
    main()
