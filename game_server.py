import socket
import time

SERVER_IP = "10.0.0.2"
SERVER_PORT = 9999

# Stores the latest sequence number received from each player
players = {}

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

print("=================================")
print("   MULTIPLAYER GAME SERVER")
print("=================================")
print(f"Listening on {SERVER_IP}:{SERVER_PORT}")
print("Waiting for players...\n")

while True:
    # Receive UDP packet
    data, address = sock.recvfrom(1024)

    message = data.decode().strip()
    parts = message.split(",")

    # Expected format:
    # PLAYER_ID,SEQUENCE,X,Y,SEND_TIME

    if len(parts) != 5:
        print("Invalid packet:", message)
        continue

    try:
        player_id = parts[0]
        sequence = int(parts[1])
        x = float(parts[2])
        y = float(parts[3])
        send_time = float(parts[4])
    except ValueError:
        print("Invalid data:", message)
        continue

    receive_time = time.time()

    # Calculate one-way application latency
    latency = (receive_time - send_time) * 1000

    # --------------------------------
    # NEW PLAYER
    # --------------------------------
    if player_id not in players:
        players[player_id] = sequence

        print(f"[REGISTER] {player_id} from {address}")

    # --------------------------------
    # EXISTING PLAYER
    # --------------------------------
    else:
        last_sequence = players[player_id]

        # Packet loss detection
        if sequence > last_sequence + 1:
            lost = sequence - last_sequence - 1

            print(
                f"[PACKET LOSS] {player_id}: "
                f"{lost} packet(s) missing"
            )

        # Out-of-order / duplicate packet
        elif sequence <= last_sequence:
            print(
                f"[OUT OF ORDER] {player_id}: "
                f"sequence {sequence}"
            )

        # Update latest sequence number
        players[player_id] = max(last_sequence, sequence)

    # --------------------------------
    # DISPLAY GAME STATE
    # --------------------------------

    print(
        f"[GAME] {player_id} | "
        f"Seq={sequence} | "
        f"Position=({x:.1f},{y:.1f}) | "
        f"Latency={latency:.2f} ms"
    )
