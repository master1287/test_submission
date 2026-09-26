# Week 2 — The Sandbox

Cellular automata with falling sand and water.

- **Spec:** [`week2.pdf`](./week2.pdf) — read it first, it is the authority.
- **Template:** [`temp.py`](./temp.py) — runs as-is, but the physics is missing.
  One `NotImplementedError` in `SandSim.update()`: sand fall/slide and water
  spread. Fire, smoke, and wood are the bonus.
- **Setup:** see the [root README](../README.md).

**Due: EOD, 23rd September 2026.**

## Your brief goes here

**Replace this file with your assignment brief.** It must contain your answers to
**Question 1** and **Question 2**.

Q1.Why does the swap grid start as a copy of the current state, rather than being
filled with zeros? What would happen to a grain that does not move if G′ started empty?

A1. The swap grid starts as a copy of the current state so as to preserve the stationary objects. If G' started empty, the sand particle in G would be overwritten
by 0 and hence completely vanish.

Q2.Remove the randomised column order and replace it with a fixed left-to-right
scan. Run the simulation for a few hundred ticks. What happens to the shape of a sand pile?
Why?

A2. The sand pile will clump towards the left. This is because as it updates cells from left to right, a sand particle on the left has to wait for the entire loop to end for it to be updated again. However, a sand particle on the right is updated instantaneously as the scanning goes from left to right. Hence, it will form a triangle from left to right.

Half a page is plenty.