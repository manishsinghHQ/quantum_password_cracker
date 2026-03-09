import streamlit as st
import itertools
import string
import time
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quantum Password Cracking Simulator")

st.title("🔐 Quantum Password Cracking Simulator")

st.write("Compare Classical Brute Force vs Grover Quantum Search")

# User input
password = st.text_input("Enter Password (A-Z or 0-9 only)", "A1B")

characters = string.ascii_uppercase + string.digits


# --------------------------
# Classical Brute Force
# --------------------------

def classical_crack(target):

    length = len(target)
    attempts = 0
    start = time.time()

    for guess in itertools.product(characters, repeat=length):

        attempts += 1
        guess = ''.join(guess)

        if guess == target:
            break

    end = time.time()

    return attempts, end - start


# --------------------------
# Quantum Grover Simulation
# --------------------------

def grover_iterations(N):
    return int(np.pi/4 * np.sqrt(N))


def quantum_crack(password_length):

    N = len(characters) ** password_length
    iterations = grover_iterations(N)

    return iterations


# --------------------------
# Run Simulation
# --------------------------

if st.button("Run Simulation"):

    if password == "":
        st.warning("Enter a password first")
    else:

        st.subheader("Target Password")
        st.write(password)

        # Classical
        attempts, classical_time = classical_crack(password)

        # Quantum
        quantum_iter = quantum_crack(len(password))

        st.subheader("Results")

        col1, col2 = st.columns(2)

        with col1:
            st.write("### Classical Search")
            st.write("Attempts:", attempts)
            st.write("Time:", round(classical_time, 4), "seconds")

        with col2:
            st.write("### Quantum Search")
            st.write("Grover Iterations:", quantum_iter)

        speedup = attempts / quantum_iter

        st.success(f"Quantum Speedup ≈ {round(speedup,2)}x")

        # --------------------------
        # Graph
        # --------------------------

        st.subheader("Search Complexity Comparison")

        N = np.array([10,100,1000,10000,100000])

        classical = N
        quantum = np.sqrt(N)

        fig, ax = plt.subplots()

        ax.plot(N, classical, label="Classical O(N)")
        ax.plot(N, quantum, label="Quantum O(√N)")

        ax.set_xlabel("Password Space")
        ax.set_ylabel("Operations Needed")

        ax.legend()

        st.pyplot(fig)
