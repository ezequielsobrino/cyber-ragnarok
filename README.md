# LLM Arena: AI Model Battle Platform

A platform for orchestrating and visualizing competitive matches between Large Language Models (LLMs) across various games and challenges. Currently featuring Tic Tac Toe battles, with planned expansion to chess, checkers, and more strategic games.

## 🎮 Current Games

### Tic Tac Toe
- Strategic decision-making showcase
- Perfect for testing basic game theory understanding
- Quick matches for rapid model comparison
- Ideal baseline for evaluation

### Planned Expansions
- ⚪ Checkers
- ♟️ Chess
- 🎲 Connect Four
- 🎯 Reversi/Othello

## 🤖 Supported LLM Models

Currently supported models via Groq API:
- LLaMA 3.1 70B Versatile
- LLaMA 3.1 8B Instant

Future support planned for:
- Claude models
- GPT models
- Mistral variants
- Custom/local models

## ✨ Key Features

### Battle System
- Model vs Model competitions
- Tournament system with multiple rounds
- Automatic move validation and game state management
- Detailed move analysis and strategy logging

### Analysis & Visualization
- Video generation of matches
- Real-time strategy analysis
- Performance metrics tracking

### Extensibility
- Modular game implementation system
- Standardized LLM interface
- Pluggable visualization components
- Customizable tournament formats

## 🛠️ Technical Architecture

```
cyber-ragnarok/
├── games/              # Game implementations
│   ├── base.py         # Base game interface
│   ├── tic_tac_toe.py  # TicTacToe implementation
│   └── future/         # Place for new game implementations
├── brains/             # LLM integration
│   ├── base.py         # Base LLM interface
│   └── providers/      # Different LLM providers
└── main.py             # Video generation
```

## 🚀 Getting Started

1. **Installation**
```bash
git clone https://github.com/yourusername/llm-arena
cd llm-arena
pip install -r requirements.txt
```

2. **Configuration**
```bash
# Create .env file with your API keys
GROQ_API_KEY=your_key_here
# Add additional API keys as needed
```

3. **Run a Tournament**
```bash
python run_tournament.py --game tic_tac_toe --model1 llama-70b --model2 llama-8b --games 5
```

## 🎯 Adding New Games

1. Implement the base game interface:
```python
class NewGame(BaseGame):
    def get_valid_moves(self):
        # Implementation
    
    def make_move(self, move):
        # Implementation
    
    def is_game_over(self):
        # Implementation
```

2. Create a game-specific brain interface:
```python
class NewGameBrain(BaseBrain):
    def analyze_position(self):
        # Implementation
    
    def get_move(self):
        # Implementation
```

3. Add visualization support:
```python
class NewGameRenderer(BaseRenderer):
    def render_state(self):
        # Implementation
    
    def render_move(self):
        # Implementation
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- Groq team for API access
- Open source game implementation references
- pygame and OpenCV communities
- LLM provider teams

## 📬 Support

- GitHub Issues for bugs and features
- Discussions for general questions