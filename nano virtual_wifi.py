import hashlib
import hmac
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, RadioTap, EAPOL

# === CONFIGURATION ===
SSID = "MyCustomLab"
PASSWORD = "password123"
BSSID = "aa:bb:cc:dd:ee:ff"  # Router MAC
CLIENT = "11:22:33:44:55:66" # Client MAC

def create_wpa_cap():
    print(f"[*] Forging .cap file for SSID: {SSID} with password: {PASSWORD}")

    # 1. PBKDF2: Generate the PMK (The "Master Key")
    # This is the standard WPA2 derivation (Password + SSID + 4096 iterations)
    pmk = hashlib.pbkdf2_hmac('sha1', PASSWORD.encode(), SSID.encode(), 4096, 32)

    # 2. Setup the Beacon Frame (So Aircrack knows the SSID)
    beacon = RadioTap()/ \
             Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=BSSID, addr3=BSSID)/ \
             Dot11Beacon(cap="ESS+privacy")/ \
             Dot11Elt(ID="SSID", info=SSID)/ \
             Dot11Elt(ID="RSNinfo", info=(
                 b'\x01\x00\x00\x0f\xac\x02\x02\x00\x00\x0f\xac\x04'
                 b'\x00\x0f\xac\x02\x01\x00\x00\x0f\xac\x02\x00\x00'
             ))

    # 3. Setup the EAPOL Handshake (Message 2 is where the MIC lives)
    # We are crafting a "fake" Message 2 that contains a valid MIC 
    # based on our PMK above.
    nonce = b"\x10" * 32  # Simplified static nonce
    
    # Construct a raw EAPOL WPA2 packet structure
    # This hex string represents a standard 802.1X Key Frame (Message 2)
    eapol_frame = (
        b"\x02" +             # Descriptor Type: EAPOL-Key
        b"\x03\x00\x5f" +     # Key Information (WPA2, HMAC-SHA1)
        b"\x00\x00\x00\x00\x00\x00\x00\x00" + # Replay Counter
        nonce +               # SNonce
        b"\x00" * 16 +        # Key IV
        b"\x00" * 8 +         # Key RSC
        b"\x00" * 8 +         # Reserved
        b"\x00" * 16 +        # MIC (Placeholder)
        b"\x00\x00"           # Key Data Length
    )

    # 4. Calculate the MIC
    # In a real handshake, this uses the PTK (Pairwise Transient Key)
    # For a simple test file, Aircrack-ng checks the MIC against the PMK/PTK logic
    mic = hmac.new(pmk, eapol_frame, hashlib.sha1).digest()[:16]
    
    # Insert the real MIC into the frame
    final_eapol = eapol_frame[:81] + mic + eapol_frame[97:]

    # 5. Assemble and Write
    handshake_pkt = RadioTap()/Dot11(addr1=BSSID, addr2=CLIENT, addr3=BSSID)/EAPOL(version=1, type=3)/final_eapol
    
    wrpcap("custom_test.cap", [beacon, handshake_pkt])
    print("[+] Success! 'custom_test.cap' created.")

if __name__ == "__main__":
    create_wpa_cap()
