import streamlit as st
import string
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quantum Password Cracking Simulator")

st.title("🔐 Quantum Password Cracking Simulator")
st.write("Compare Classical Brute Force vs Grover Quantum Search")

characters = string.ascii_uppercase + string.digits

# --------------------------
# USER INPUT
# --------------------------

password = st.text_input("Enter Password (A-Z or 0-9 only)", "A1B")

mode = st.radio(
    "Choose Simulation Mode",
    ["Classical Search", "Quantum Search", "Both"]
)

# --------------------------
# CLASSICAL SIMULATION
# --------------------------

def classical_crack(password):

    length = len(password)

    search_space = len(characters) ** length

    # average case attempts
    attempts = search_space // 2

    simulated_time = attempts / 10000000

    return attempts, simulated_time


# --------------------------
# QUANTUM GROVER SIMULATION
# --------------------------

def grover_iterations(N):
    return int(np.pi/4 * np.sqrt(N))


def quantum_crack(password_length):

    N = len(characters) ** password_length
    iterations = grover_iterations(N)

    return iterations


# --------------------------
# RUN SIMULATION
# --------------------------

if st.button("Run Simulation"):

    if password == "":
        st.warning("Enter a password first")
    else:

        st.subheader("Target Password")
        st.write(password)

        length = len(password)

        search_space = len(characters) ** length

        st.write("Total Password Space:", search_space)

        # --------------------------
        # CLASSICAL ONLY
        # --------------------------

        if mode == "Classical Search":

            attempts, classical_time = classical_crack(password)

            st.subheader("Classical Search Result")

            st.write("Attempts:", attempts)
            st.write("Estimated Time:", round(classical_time,4),"seconds")

        # --------------------------
        # QUANTUM ONLY
        # --------------------------

        elif mode == "Quantum Search":

            quantum_iter = quantum_crack(length)

            st.subheader("Quantum Search Result")

            st.write("Grover Iterations:", quantum_iter)

        # --------------------------
        # BOTH COMPARISON
        # --------------------------

        elif mode == "Both":

            attempts, classical_time = classical_crack(password)

            quantum_iter = quantum_crack(length)

            col1, col2 = st.columns(2)

            with col1:

                st.write("### Classical Search")
                st.write("Attempts:", attempts)
                st.write("Estimated Time:", round(classical_time,4),"seconds")

            with col2:

                st.write("### Quantum Search")
                st.write("Grover Iterations:", quantum_iter)

            speedup = attempts / quantum_iter

            st.success(f"Quantum Speedup ≈ {round(speedup,2)}x")

            # --------------------------
            # GRAPH
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
