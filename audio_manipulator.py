"""
Audio Manipulator

Manipulates two audio files:
1. Splits a familiar song into a specified number of chunks.
2. Extracts a random chunk from an unfamiliar song with the same length as one familiar chunk.
3. Inserts the unfamiliar chunk among the split familiar chunks.
4. Exports the resulting audio to a file.

Dependencies:
    pip install pydub

Note:
    For MP3/M4A support, pydub requires ffmpeg or libav installed and on PATH.
    WAV files work without any external codec.
"""

import argparse
import random
from pathlib import Path

try:
    from pydub import AudioSegment
except ImportError as exc:
    raise ImportError(
        "pydub is required. Install it with: pip install pydub"
    ) from exc


def load_audio(path: str) -> AudioSegment:
    """Load an audio file from path."""
    audio_path = Path(path)
    if not audio_path.is_file():
        raise FileNotFoundError(f"Audio file not found: {path}")
    return AudioSegment.from_file(str(audio_path))


def split_song(audio: AudioSegment, num_chunks: int) -> list[AudioSegment]:
    """
    Split an audio segment into `num_chunks` chunks of equal length.
    Any leftover milliseconds at the end are appended to the last chunk.
    """
    if num_chunks <= 0:
        raise ValueError("Number of chunks must be greater than 0.")

    total_length = len(audio)  # milliseconds
    chunk_length = total_length // num_chunks

    if chunk_length == 0:
        raise ValueError(
            f"Cannot split {total_length}ms audio into {num_chunks} chunks. "
            "Each chunk would be empty."
        )

    chunks = []
    for i in range(num_chunks):
        start = i * chunk_length
        # Make the last chunk capture any remaining audio.
        end = total_length if i == num_chunks - 1 else (i + 1) * chunk_length
        chunks.append(audio[start:end])

    return chunks


def extract_random_chunk(audio: AudioSegment, chunk_length_ms: int) -> AudioSegment:
    """
    Extract a random chunk of `chunk_length_ms` from `audio`.
    The chunk is chosen so that it fits entirely within the audio.
    """
    if chunk_length_ms <= 0:
        raise ValueError("Chunk length must be greater than 0 ms.")

    audio_length = len(audio)
    if audio_length < chunk_length_ms:
        raise ValueError(
            f"Unfamiliar song ({audio_length}ms) is shorter than the requested "
            f"chunk length ({chunk_length_ms}ms)."
        )

    max_start = audio_length - chunk_length_ms
    start = random.randint(0, max_start)
    end = start + chunk_length_ms
    return audio[start:end]


def stuff_chunk(
    familiar_chunks: list[AudioSegment],
    unfamiliar_chunk: AudioSegment,
    insert_position: int | None = None,
) -> AudioSegment:
    """
    Insert `unfamiliar_chunk` into `familiar_chunks`.

    Args:
        familiar_chunks: List of AudioSegment chunks from the familiar song.
        unfamiliar_chunk: The chunk to insert.
        insert_position: Index at which to insert. If None, a random position
            (including before the first and after the last chunk) is chosen.

    Returns:
        A single AudioSegment with the unfamiliar chunk inserted.
    """
    if not familiar_chunks:
        raise ValueError("Familiar song must have at least one chunk.")

    if insert_position is None:
        insert_position = random.randint(0, len(familiar_chunks))
    elif not (0 <= insert_position <= len(familiar_chunks)):
        raise ValueError(
            f"Insert position must be between 0 and {len(familiar_chunks)}."
        )

    combined_chunks = familiar_chunks.copy()
    combined_chunks.insert(insert_position, unfamiliar_chunk)
    return sum(combined_chunks[1:], combined_chunks[0])


def main():
    parser = argparse.ArgumentParser(
        description="Split a familiar song into chunks, stuff a random chunk from an unfamiliar song in between, and export the result."
    )
    parser.add_argument("familiar", help="Path to the familiar song audio file.")
    parser.add_argument("unfamiliar", help="Path to the unfamiliar song audio file.")
    parser.add_argument(
        "-n",
        "--num-chunks",
        type=int,
        default=4,
        help="Number of chunks to split the familiar song into (default: 4).",
    )
    parser.add_argument(
        "-p",
        "--position",
        type=int,
        default=None,
        help="Position at which to insert the unfamiliar chunk (0 = before first chunk, N = after last chunk). If omitted, a random position is chosen.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.wav",
        help="Output file path (default: output.wav).",
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducible random chunk/position selection.",
    )

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    familiar = load_audio(args.familiar)
    unfamiliar = load_audio(args.unfamiliar)

    familiar_chunks = split_song(familiar, args.num_chunks)
    chunk_length_ms = len(familiar_chunks[0])

    unfamiliar_chunk = extract_random_chunk(unfamiliar, chunk_length_ms)
    result = stuff_chunk(familiar_chunks, unfamiliar_chunk, args.position)

    output_path = Path(args.output)
    print(f"Familiar song length: {len(familiar)}ms")
    print(f"Split into {len(familiar_chunks)} chunks of ~{chunk_length_ms}ms each")
    print(f"Unfamiliar chunk extracted: {len(unfamiliar_chunk)}ms")
    print(f"Insert position: {args.position if args.position is not None else 'random'}")
    print(f"Result length: {len(result)}ms")
    print(f"Exporting to: {output_path.resolve()}")

    fmt = output_path.suffix.lstrip(".").lower() or "wav"
    result.export(str(output_path), format=fmt)
    print("Done.")


if __name__ == "__main__":
    main()
