from typing import List, Any, Optional

from pydantic import BaseModel, Field, validator

from app import api_settings, api_config


class ErrorMessage(BaseModel):
    detail: str = Field(description="Human-readable error message.")


class Request(BaseModel):
    text: str = Field(...,
                      description="Original text input. May contain multiple sentences.",
                      example="Tere!",
                      max_length=api_settings.max_input_length)
    speaker: str = Field(...,
                         example="mari",
                         description="Name of speaker (not case-sensitive).")
    speed: float = Field(default=1,
                         description="Output audio speed multiplier.",
                         ge=0.5,
                         le=2)

    def __init__(self, **data: Any):
        super(Request, self).__init__(**data)

    @validator('speaker')
    def check_speaker(cls, v):
        v = v.lower()
        if v in api_config.alt_names:
            v = api_config.alt_names[v]
        if v not in api_config.speakers:
            raise ValueError(f"Unknown speaker '{v}'.")
        return v


class ResponseContent(BaseModel):
    text: str = Field(...,
                      description="Original text input. May contain multiple sentences.",
                      example="Muinasjutt 3 karust."
                      )
    normalized_text: str = Field(...,
                                 description="List of normalized input sentences."
                                             "This is the final input to the synthesis model."
                                             "May be padded by whitespace to align with the pause durations in the"
                                             "duration values.",
                                 example=" muinasjutt kolmest karust. ")

    duration_frames: Optional[List[float]] = Field(...,
                                                   description="A list of predicted duration values for each input "
                                                               "character from 'normalized_text'. The duration is "
                                                               "calculated as the number of mel-spectrogram frames.",
                                                   example=[43, 12, 8, 5, 5, 8, 3, 8, 5, 6, 6, 0, 8, 8, 5, 5, 5, 5, 5,
                                                            0, 5, 5, 5, 8, 10, 12, 0, 43]
                                                   )
    sampling_rate: Optional[int] = Field(...,
                                         description="Audio sampling rate in Hz.",
                                         example=22050
                                         )
    win_length: Optional[int] = Field(...,
                                      description="Number of samples per window.",
                                      example=1024
                                      )
    hop_length: Optional[int] = Field(...,
                                      description="Hop length (number of samples between successive windows).",
                                      example=256
                                      )
    audio: bytes = Field(...,
                         description="Base64 encoded raw binary audio.")


class Speaker(BaseModel):
    name: str = Field(...,
                      example="kylli",
                      description="Speaker's name.")
    languages: List[str] = Field(...,
                                 example=["est"],
                                 description="A list of supported languages for this speaker")


class Config(BaseModel):
    speakers: List[Speaker] = Field(...,
                                    description="A list of supported speakers and their configurations.")
