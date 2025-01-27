# Chat Server with Python and OpenSSL

## Project Overview
This project implements a secure chat server using Python's `socket` and `ssl` libraries. The server enables real-time communication between multiple clients with support for an admin role to manage participants through commands such as kicking or banning users.

> This project was developed as a mini project for the course - Computer Networks

## Features

- **Secure Communication**: Messages are encrypted using SSL/TLS to ensure confidentiality and security.
- **Admin Privileges**: 
  - Admin users can execute commands to kick or ban participants.
  - Admin access requires a password.
- **Ban System**: Banned users are saved in a `bans.txt` file and are prevented from reconnecting.
- **Multi-Client Support**: Multiple clients can join the chat room and communicate in real-time.

## Tech Stack

- Python 3.x 
- OpenSSL - for generating SSL certificates.

## Project Structure
The project consists of the following files:

- server.py: Handles incoming client connections, broadcasts messages, and processes admin commands.
- client.py: Connects to the server, sends and receives messages, and provides admin capabilities if the user logs in as the admin.
- bans.txt: Stores the nicknames of banned users.

## Admin Commands
Once connected, admin users can execute the following commands:

- /kick <nickname>: Remove a user from the chat room.
- /ban <nickname>: Ban a user, preventing them from rejoining.
