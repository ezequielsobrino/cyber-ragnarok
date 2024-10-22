# Cyber Ragnarok

A Python framework for creating AI model competitions through various games, generating entertaining and visually appealing battle videos. Currently featuring Tic-Tac-Toe battles between different Language Models (LLMs), with plans to expand to chess, checkers, and more games.

## Demo Video

[![Cyber Ragnarok Demo](https://img.youtube.com/vi/od9GdSF1vC4/0.jpg)](https://www.youtube.com/watch?v=od9GdSF1vC4)

Watch different AI models battle it out in Tic-Tac-Toe! Click the image above to see the action.

## Features

- 🎮 Multiple Game Support (extensible architecture)
  - Currently: Tic-Tac-Toe
  - Planned: Chess, Checkers, and more
- 🤖 LLM Integration
  - Battle different versions of language models
  - Compare decision-making capabilities
  - Analyze strategic thinking
- 🎥 Professional Tournament Videos
  - Round introductions
  - Live game animations
  - Score tracking
  - Winner announcements
  - Background music
- 📊 Performance Analytics
  - Win rates

## Project Structure

```
llm-battle-arena/
├── main.py                      # Main entry point
├── brains/                      # AI decision-making modules
│   └── tic_tac_toe_brain.py    # TicTacToe LLM integration
├── games/                       # Game implementations
│   └── tic_tac_toe.py          # TicTacToe game logic
├── tournament_video_maker.py    # Video generation system
└── requirements.txt
```

## Prerequisites

- Python 3.8+
- FFmpeg
- Required Python packages (see requirements.txt)
- Access to LLM APIs (configuration required)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/llm-battle-arena.git
cd llm-battle-arena
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your GROQ_API_KEY credentials in a `.env` file:
```env
GROQ_API_KEY=your_api_key_here
```

## Usage

1. Run a basic tournament:
```bash
python main.py
```

2. Configure tournament settings in `main.py`:
```python
# Example configuration
config = {
    "game": "tictactoe",
    "model1": "llama-3.1-70b-versatile",
    "model2": "llama-3.1-8b-instant",
    "num_games": 10
}
```

The output video will be saved as: `tournament_[model1]_vs_[model2]_[games]games.mp4`

## Extending the Framework

### Adding New Games

1. Create game logic in `games/your_game.py`
2. Implement AI integration in `brains/your_game_brain.py`
3. Add necessary visual assets in `assets/`
4. Update video maker to support new game visualization

Example:
```python
# games/chess.py
class ChessGame(BaseGame):
    def __init__(self):
        super().__init__()
        # Chess-specific implementation
```

### Supporting New LLMs

Add new model support in the brain implementations:

```python
# brains/tic_tac_toe_brain.py
class TicTacToeBrain:
    def add_model(self, model_name, model_config):
        # Implementation for new model support
```

## Logging

Detailed logs are generated for each tournament:
- Tournament progress
- Model decisions
- Game outcomes
- Performance metrics

Format: `tournament_YYYYMMDD_HHMMSS.log`

## Future Plans

- [ ] Chess implementation
- [ ] Checkers implementation
- [ ] Connect Four
- [ ] Real-time LLM decision visualization
- [ ] Tournament brackets
- [ ] Multi-model tournaments
- [ ] Performance analytics dashboard
- [ ] Web interface for tournament configuration

## License

This project is licensed under the MIT License - see the LICENSE file for details.