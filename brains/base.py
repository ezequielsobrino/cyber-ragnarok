from dataclasses import dataclass

@dataclass
class BrainResponse:
    move: tuple
    raw_content: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost: float
    response_time: float
    is_fallback: bool