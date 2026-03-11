# 🐦 Flappy Bird AI — NEAT Evolution

A neural network that learns to play Flappy Bird from scratch using **NEAT** 
(NeuroEvolution of Augmenting Topologies) no hardcoded rules, no hand-tuned 
logic. Pure evolutionary learning.

## How It Works

Each generation spawns a population of birds, each controlled by a small neural 
network with random weights. Birds that survive longer reproduce and pass on their 
"genes" — gradually evolving a network that masters the game.

- **Inputs**: Bird Y position, distance to next pipe, gap position
- **Output**: Jump or don't jump
- **Evolution**: Fitness-based selection, crossover, and mutation via NEAT
- Reaches superhuman performance within ~30 generations
