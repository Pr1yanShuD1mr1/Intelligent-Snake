

# Intelligent Snake
Intelligent Snake represent a significant evolution of the classic snake game, moving beyond simple procedural logic to implement a sophisticated artificial intelligence (AI) framework.
where snake's behavior is characterized by its ability to learn, adapt, and develop emergent strategies for survival and score maximization.



## Tech Stack
- Python 3.x
- PyTorch
- tkinter
- matplotlib



## How It Works
1. **The Environment**
   - State: representation of the board
   - Action: move up/down/left/right
   - Reward: shaping feedback

2. **The Agent**
   - Uses a neural network
   - DQN: learns Q-values, buffer, target network

3. **Training Loop**
   - Agent plays episodes
   - Stores transitions
   - Trains from sampled minibatches
   - Periodically saves model and evaluates



## Project Structure
```text
intelligent-snake/
│
├── README.md
├── requirements.txt
│
├── src/
│   ├── ae.py    # Snake environment
│   ├── ar.py    # Reinforcement learning agent (DQN)
│   ├── nn.py    # Neural network architecture
│   ├── tg.py    # Training entry point
│   ├── gr.py    # Graph utilities for logging
│   └── ev.py    # Evaluation / interactive play mode
│
└── model/   # Directory for saved model checkpoints
```





