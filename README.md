# MACSS_40550_Assignment1

## Summary
Our model was modified from [Schelling's segregation model](https://github.com/jmclip/MACSS-40550-ABM/tree/main/2_Schelling/mesa_schelling), based on `mesa 2.0`. The Schelling isolation model is a classic agent-based model that shows that even a slight preference for similar neighbors can lead to a higher degree of isolation than we intuitively expect. In this model, agents are represented by red and blue colors and placed on a square grid where each cell can hold at most one agent.  Agents assess their satisfaction based on the colors of their up to eight immediate neighbors.  They prefer to be surrounded by neighbors of their color. Additionally, there are two city centers on the grid, and agents also consider their happiness based on whether their distance from either city center falls within a specific range.  Unhappy agents will relocate to a vacant cell in each iteration of the model to find satisfaction.  This process continues until agents are satisfied.

## Changes been made
Add two city centers located at the top-left and bottom-right corners, which can move diagonally.\
Add one parameter: the distance to the closest city center, which can be computed to affect household happiness.\
This model can be transferred to the original Schelling model by setting the `distance to city center` parameter to a considerable number because, under that condition, all agents will be happy with their distance to the city center. Therefore, the distance constraint disappears.

## Installation
     pip install -r requirements.txt
## Files
`agents.py` 



## How to run
1. To install dependencies, use pip and the requirements.txt file in this directory

2. To run the model interactively, run Python `run.py` in this directory.

## Group members (Alphabetical order)
Gregory Ho, Jiaxuan Zhang, Thomas Yan
