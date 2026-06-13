# Audio Manipulator

A small Python tool that manipulates two audio files:

1. Splits a **familiar song** into a specified number of chunks.
2. Extracts a random chunk from an **unfamiliar song** with the same length as one familiar chunk.
3. Inserts ("stuffs") the unfamiliar chunk among the familiar chunks.
4. Exports the mixed audio to a file.

## Setup

Activate the virtual environment and install dependencies:

```bash
bbg_master_project/Scripts/python.exe -m pip install -r requirements.txt
```

## Usage

```bash
python audio_manipulator.py familiar.wav unfamiliar.wav -n 4 -o output.wav
```

### Options

| Option | Description |
|--------|-------------|
| `familiar` | Path to the familiar song. |
| `unfamiliar` | Path to the unfamiliar song. |
| `-n`, `--num-chunks` | Number of chunks to split the familiar song into (default: 4). |
| `-p`, `--position` | Index at which to insert the unfamiliar chunk. `0` = before the first chunk, `N` = after the last chunk. If omitted, a random position is used. |
| `-o`, `--output` | Output file path (default: `output.wav`). |
| `-s`, `--seed` | Random seed for reproducible random chunk/position selection. |

### Examples

Insert at a specific position:

```bash
python audio_manipulator.py familiar.mp3 unfamiliar.mp3 -n 5 -p 2 -o mixed.mp3
```

Reproducible randomization:

```bash
python audio_manipulator.py familiar.wav unfamiliar.wav -n 4 -s 123 -o output.wav
```

## Notes

- `pydub` is used for audio I/O and manipulation.
- WAV files work out of the box.
- For MP3, M4A, or other compressed formats, install **ffmpeg** and ensure it is available on your system PATH.

## Testing

Generate synthetic test audio and run the manipulator:

```bash
python generate_test_audio.py
python audio_manipulator.py familiar.wav unfamiliar.wav -n 4 -s 42 -o output.wav
```
