# Mushroom Collector 🍄

![pygame-logo](https://www.pygame.org/docs/_static/pygame_tiny.png)

Mushroom Collector is a game where AI controls a basket to collect falling mushrooms.
The goal is to collect non-poisonous mushrooms while avoiding poisonous ones.
This project implements the game using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm,
which evolves artificial neural networks to control the basket's movement based on the positions of the mushrooms.

- Poisonous mushrooms: 💀
- Non-poisonous mushrooms: 🍄

## Requirements
- Python 3.x
- pygame
- neat-python

## How to Play
1. Clone the repository to your local environment.
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the game: `python mushroom_collector.py`

## NEAT Configuration
The NEAT algorithm is configured using a configuration file (`neat-config.txt`).

## Running the NEAT Algorithm
To run the game with NEAT algorithm with the provided configuration file and evolve the neural networks, execute the `run()` function in the `mushroom_collector.py`.

```python
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    run(config_path)
```
### Example Scene (non-AI, manually played):
![game-gif](https://github.com/sudeatesoglu/mushroom_collector/assets/106230756/ef89d1e3-c0f3-48ee-9c88-4a90a8ef6b92)

! ***The project will continue to be developed...***
---
Images are from: <br>
<a href="https://www.flaticon.com/free-icons/mushroom" title="mushroom icons">Mushroom icons created by Freepik - Flaticon</a>
<br>
<a href="https://www.flaticon.com/free-icons/basket" title="basket icons">Basket icons created by Freepik - Flaticon</a>
<br>
Sounds effects are from:
<a href="https://pixabay.com/sound-effects/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=6735">Pixabay</a>
