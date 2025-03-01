# Continuum growth models PDE Solver v1.0: AI Engineer’s Approach

## Edwards-Wilkinson equation
The **Edwards–Wilkinson (EW) equation** is a linear stochastic partial differential equation (PDE) used to describe surface growth and smoothing. In its deterministic form (i.e., without noise), it is equivalent to the heat (diffusion) equation:

\[
\frac{\partial h(x,t)}{\partial t} = \nu \nabla^2 h(x,t)
\]

where:

- \( h(x,t) \) is the height profile at position \( x \) and time \( t \),
- \( \nu \) is the diffusion coefficient (or surface tension),
- \( \nabla^2 \) is the Laplacian operator.

In one spatial dimension, the Laplacian can be approximated using finite differences as:

\[
\nabla^2 h(x,t) \approx \frac{h(x-\Delta x, t) - 2\,h(x,t) + h(x+\Delta x,t)}{\Delta x^2}.
\]

This equation models the smoothing (or diffusion) of the height profile over time.

