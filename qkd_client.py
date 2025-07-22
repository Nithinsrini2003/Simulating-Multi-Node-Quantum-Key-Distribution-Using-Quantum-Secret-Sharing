import socket
import numpy as np
import math
from datetime import datetime
import random
import hashlib

def generate_shared_keys(participants: int) -> tuple[np.ndarray, float]:
    phases = np.random.uniform(0, 2 * np.pi, participants)
    combined_key = np.sum(phases) % (2 * np.pi)
    return phases, combined_key

def create_hyperbolic_matrix(theta):
    return np.array([[math.cosh(theta), math.sinh(theta)],
                     [math.sinh(theta), math.cosh(theta)]])

def chaotic_map(t, r=3.8):
    return r * t * (1 - t)

def fractal_transformation(E_t, S):
    return E_t * S

def encrypt(plaintext, key, initial_theta=0.5):
    P = np.array([ord(char) for char in plaintext], dtype=float)
    padding = 0
    if len(P) % 2 != 0:
        P = np.append(P, 0)
        padding = 1
    P = P.reshape(-1, 2).T
    M_0 = create_hyperbolic_matrix(initial_theta)
    E_0 = np.dot(M_0, P)
    t = datetime.now().timestamp() % 1
    M_t = create_hyperbolic_matrix(chaotic_map(t))
    E_t = np.dot(M_t, E_0)
    E_final = fractal_transformation(E_t, key)
    return E_final.flatten(), padding, t

def generate_quantum_state():
    return str(random.randint(0, 1))

def compute_hash(data):
    return hashlib.sha256(str(data).encode()).hexdigest()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

participants = 3
phases, shared_key = generate_shared_keys(participants)
print(f"Generated Phases: {phases}")
print(f"Shared Key: {shared_key}")

plaintext = input("Enter the plaintext message: ")
encrypted_message, padding, t = encrypt(plaintext, shared_key)

print(f"Plaintext: {plaintext}")
print(f"Padding: {padding}")
print(f"Timestamp (t): {t}")
print(f"Encrypted Message: {encrypted_message}")

quantum_state = generate_quantum_state()
print(f"Generated Quantum State: {quantum_state}")

client_socket.sendall(encrypted_message.tobytes())
client_socket.sendall(np.array([shared_key], dtype=np.float64).tobytes())
client_socket.sendall(np.array([padding], dtype=np.int32).tobytes())
client_socket.sendall(np.array([t], dtype=np.float64).tobytes())
client_socket.sendall(quantum_state.encode('utf-8'))

# Receive the challenge from the server
server_challenge = client_socket.recv(1024).decode('utf-8')
print(f"Received Challenge from Server: {server_challenge}")

# Compute and send the response to the server
client_response = compute_hash(server_challenge + quantum_state)
client_socket.sendall(client_response.encode('utf-8'))

# Show efficiency metrics
efficiency = 100 * (1 - np.abs(shared_key % 1))
print(f"Quantum Key Efficiency: {efficiency:.2f}%")

print("\n--- Quantum Cryptography Debug Information ---")
print(f"Quantum State Sent: {quantum_state}")
print(f"Challenge from Server: {server_challenge}")
print(f"Client Response: {client_response}")

print("Encrypted data sent.")
client_socket.close()
