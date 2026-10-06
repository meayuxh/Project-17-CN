import socket
import time
import sys

PLAYER_ID = sys.argv[1] if len(sys.argv) > 1 else "P1"

SERVER_IP = "10.0.0.2"
SERVER_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Player {PLAYER_ID} started")
print(f"Sending game updates to {SERVER_IP}:{SERVER_PORT}")

sequence = 1

try:
    while True:
        x = sequence
        y = sequence * 2

        send_time = time.time()

        message = f"{PLAYER_ID},{sequence},{x},{y},{send_time}"

        sock.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

        print(f"[SEND] {message}")

        sequence += 1

        time.sleep(1)

except KeyboardInterrupt:
    print("\nPlayer stopped.")

finally:
    sock.close()
