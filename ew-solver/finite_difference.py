import torch
import matplotlib.pyplot as plt
import math

# --- 1. Setup parameters and domain (1D) ---
def set_values():
    L = 1.0             # Length of the domain (e.g., 1.0 unit, could be any length scale)
    N = 100             # Number of grid points
    dx = L / N          # Spatial grid size
    nu = -1.0            # Diffusion coefficient in the EW equation
    dt = 0.000005         # Time step (must satisfy stability: nu*dt/dx^2 <= 0.5)
    num_steps = 100    # Number of time steps to simulate

    # Select device: GPU if available, else CPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # --- 2. Initial condition for h(x,0) ---
    # Example: sinusoidal surface height profile h(x) = sin(2πx/L)
    # We create a tensor for positions [0, 1, 2, ..., N-1] and map to spatial coordinate (i/N)*L
    indices = torch.arange(N, dtype=torch.float32)
    x = indices * (L / N)  # spatial coordinate values (0 to L-dx)
    h0 = torch.sin(2 * torch.pi * x / L)  # sine wave across the domain

    # Ensure the tensor is on the correct device (CPU or GPU)
    h = h0.to(device)
    return h, x, dx, nu, dt, num_steps, L

# --- 3. Function to compute Laplacian with periodic BC ---
def compute_laplacian(h_tensor, dx):
    # print("Height tensor: ", h_tensor, dx)
    # Use torch.roll for periodic wrapping: roll(-1) gives shift to right (i+1), roll(1) gives shift to left (i-1)
    h_right = torch.roll(h_tensor, shifts=-1, dims=0)  # neighbor to the right (i+1, with wrap)
    # print("Height right: ", h_right)
    h_left  = torch.roll(h_tensor, shifts=1, dims=0)   # neighbor to the left (i-1, with wrap)
    # Second difference (Laplacian) with periodic BC
    lap = (h_left - 2 * h_tensor + h_right) / (dx * dx)
    # print("Laplacian: ", lap)
    return lap

# --- 4. Time-stepping loop (Explicit Euler integration) ---
def time_loop(h: torch.tensor, num_steps: int, nu: float, dt: float, dx: float):
    final_h = h.clone()  # copy the initial height profile

    for step in range(num_steps):
        lap_h = compute_laplacian(final_h, dx)
        # Update rule: h^{n+1} = h^n + nu * dt * Laplacian(h^n)
        final_h = final_h + nu * dt * lap_h
        
    # After the loop, `h` contains the height profile at time t = num_steps * dt.
    # (For a diffusion process, this will tend toward a flat profile equal to the initial average height.)
    return final_h


def main():
    h, x, dx, nu, dt, num_steps, L = set_values()
    h_final = time_loop(h, num_steps, nu, dt, dx)

    # Exact solition is h(x,t) = sin(2πx/L) * exp(-4π^2 ν t / L^2)
    # We can compare the final height profile to the exact solution at time t = num_steps * dt
    h_exact = torch.sin(2 * torch.pi * x / L) * math.exp(-4 * torch.pi ** 2 * nu * num_steps * dt / L ** 2)
    plt.plot(x.cpu().numpy(), h.cpu().numpy(), label='Initial h(x)')
    plt.plot(x.cpu().numpy(), h_final.cpu().numpy(), label='Final h(x)')
    # plt.plot(x.cpu().numpy(), h_final.cpu().numpy(), label='Final h(x)', linestyle='', marker='o')
    plt.plot(x.cpu().numpy(), h_exact.cpu().numpy(), label='Exact h(x)')
    plt.xlabel('x')
    plt.ylabel('h(x)')
    plt.title('Height profile at t = {:.3f}'.format(num_steps * dt))
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()