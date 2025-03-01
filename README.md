# Continuum growth models PDE Solver v1.0: AI Engineer’s Approach

## Edwards-Wilkinson equation
The Edwards–Wilkinson (EW) equation is given by:

\[
\frac{\partial h(x,t)}{\partial t} = \nu \nabla^2 h(x,t)
\]

where:
- \(h(x,t)\) is the height at position \(x\) and time \(t\),
- \(\nu\) is the diffusion (or surface tension) coefficient,
- \(\nabla^2\) denotes the Laplacian, which in one spatial dimension is:

\[
\nabla^2 h(x,t) \approx \frac{h(x-\Delta x,t) - 2\,h(x,t) + h(x+\Delta x,t)}{\Delta x^2}.
\]
