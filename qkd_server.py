import socket
import numpy as np
import math
import hashlib

def create_hyperbolic_matrix(theta):
    return np.array([[math.cosh(theta), math.sinh(theta)],
                     [math.sinh(theta), math.cosh(theta)]])

def chaotic_map(t, r=3.8):
    return r * t * (1 - t)

def fractal_transformation(E_t, S):
    return E_t / S

def decrypt(E_final, key, padding, t, initial_theta=0.5):
    E_final = E_final.reshape(2, -1)
    E_t = fractal_transformation(E_final, key)
    M_t = create_hyperbolic_matrix(chaotic_map(t))
    M_t_inv = np.linalg.inv(M_t)
    E_0 = np.dot(M_t_inv, E_t)
    M_0 = create_hyperbolic_matrix(initial_theta)
    M_0_inv = np.linalg.inv(M_0)
    P = np.dot(M_0_inv, E_0)
    plaintext = ''.join(chr(int(round(char))) for char in P.flatten() if 0 <= char <= 127)
    if padding:
        plaintext+= plaintext[:padding]
    return plaintext

def compute_hash(data):
    return hashlib.sha256(str(data).encode()).hexdigest()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

print("Server is listening...")
conn, addr = server_socket.accept()
print(f"Connection from {addr}")

encrypted_data = conn.recv(2048)
E_final = np.frombuffer(encrypted_data, dtype=float)

key_data = conn.recv(8)
shared_key = np.frombuffer(key_data, dtype=np.float64)[0]

padding_data = conn.recv(4)
padding = np.frombuffer(padding_data, dtype=np.int32)[0]

t_data = conn.recv(8)
t = np.frombuffer(t_data, dtype=np.float64)[0]

# Receive quantum state
quantum_state = conn.recv(1024).decode('utf-8')
print(f"Received Quantum State: {quantum_state}")

# Generate a challenge for the client
challenge = "QuantumChallenge"  # Example challenge string
conn.sendall(challenge.encode('utf-8'))

# Decrypt the message
decrypted_message = decrypt(E_final, shared_key, padding, t)
print(f"Decrypted Message: {decrypted_message}")

# Show efficiency metrics
efficiency = 100 * (1 - np.abs(shared_key % 1))
print(f"Quantum Key Efficiency: {efficiency:.2f}%")

# Display more detailed information
print("\n--- Quantum Cryptography Debug Information ---")
print(f"Quantum State during communication: {quantum_state}")
print(f"Server Shared Key: {shared_key}")
print(f"Decrypted Message: {decrypted_message}")
print(f"Challenge Sent to Client: {challenge}")

conn.close()
server_socket.close()
