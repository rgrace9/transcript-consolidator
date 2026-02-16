# Interview Transcript Consolidator

A Python tool that consolidates consecutive speaking segments in interview transcripts, making them easier to read and analyze for qualitative research.

## Problem It Solves

Interview transcripts from Zoom, Teams, Otter.ai and other platforms often fragment speech into many small segments:

```.vtt
42
00:15:12.340 --> 00:15:14.200
ODYSSEUS: Well, that's interesting.

43
00:15:15.100 --> 00:15:18.750
ODYSSEUS: The journey to Ithaca was quite long, you know.

44
00:15:19.200 --> 00:15:25.890
ODYSSEUS: I encountered many challenges with the sirens and cyclops along the way.
```

This tool consolidates them into readable blocks:

```.vtt
00:15:12.340 --> 00:15:25.890
ODYSSEUS: Well, that's interesting.
The journey to Ithaca was quite long, you know.
I encountered many challenges with the sirens and cyclops along the way.
```

## Quick Start

**Requirements:**

- Python 3.6 or later
- No additional packages needed

## Basic Usage

```python
# Single file
python consolidator.py odysseus_call.vtt


# Save to specific file  name
python consolidator.py odysseus_call.vtt -o odysseus_transcript_consolidated.txt
```

Everything is run locally. Does not require wifi.

## Input Format

Works with transcript formats that include:

- Timestamp lines: HH:MM:SS.mmm --> HH:MM:SS.mmm
- Speaker identification: SPEAKER_NAME: text content
- Optional chapter/segment numbers
