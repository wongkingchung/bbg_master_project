# Audio Manipulator

A small Python tool that manipulates two audio files:

1. Splits a **familiar song** into a specified number of chunks.
2. Extracts a random chunk from an **unfamiliar song** with the same length as one familiar chunk.
3. Stuffs the unfamiliar chunk **between every consecutive pair** of familiar chunks, producing a pattern like:
   `S1c1 + S2cx + S1c2 + S2cx + S1c3 + ...`
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
| `-o`, `--output` | Output file path (default: `output.wav`). |
| `-s`, `--seed` | Random seed for reproducible random unfamiliar chunk selection. |

### Examples

Reproducible randomization:

```bash
python audio_manipulator.py familiar.wav unfamiliar.wav -n 4 -s 123 -o output.wav
```

Use MP3 files (requires ffmpeg):

```bash
python audio_manipulator.py familiar.mp3 unfamiliar.mp3 -n 5 -o mixed.mp3
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
