# Multiplayer Game Communication Network

## Project 17 – SDN Socket Programming

### 1. Overview

This project implements a multiplayer game communication network using UDP socket programming and Software Defined Networking (SDN).

The system supports multiple players communicating with a central game server through a Mininet-based network. An SDN controller identifies game traffic and assigns UDP game packets to a high-priority queue.

### 2. Technologies Used

- Python 3
- UDP Socket Programming
- Mininet
- Open vSwitch
- OpenFlow 1.3
- OS-Ken SDN Controller
- Linux traffic control (tc)

### 3. Network Topology

```text
        Player 1 (h1)
              |
              |
        +-----------+
        |   OVS s1  |
        +-----------+
          |       |
          |       |
     Server(h2) Player 2(h3)

             |
       SDN Controller
        OS-Ken 4.2.2
