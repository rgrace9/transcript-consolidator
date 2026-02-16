#!/usr/bin/env python3
"""
Zoom Transcript Consolidator

This script consolidates consecutive speaking segments from the same person
in a Zoom transcript file and updates timestamps to show the full range.
"""

import re
import argparse
from typing import List, Tuple, Optional

class TranscriptSegment:
    def __init__(self, start_time: str, end_time: str, speaker: str, text: str, chapter_num: Optional[str] = None):
        self.start_time = start_time
        self.end_time = end_time
        self.speaker = speaker
        self.text = text.strip()
        self.chapter_num = chapter_num
    
    def __str__(self):
        return f"{self.start_time} --> {self.end_time}\n{self.speaker}: {self.text}"

def parse_transcript_file(file_path: str) -> List[TranscriptSegment]:
    """Parse the transcript file and extract segments."""
    segments = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by double newlines to get individual segments
    blocks = content.strip().split('\n\n')
    
    for block in blocks:
        if not block.strip():
            continue
            
        lines = block.strip().split('\n')
        
        # Skip blocks that don't have the expected format
        if len(lines) < 2:
            continue
        
        # Check if first line is a chapter number
        chapter_num = None
        timestamp_line = None
        speaker_text_lines = []
        
        for i, line in enumerate(lines):
            # Check if it's a chapter number (just digits)
            if re.match(r'^\d+$', line.strip()):
                chapter_num = line.strip()
                continue
            
            # Check if it's a timestamp line
            if '-->' in line:
                timestamp_line = line.strip()
                speaker_text_lines = lines[i+1:]
                break
        
        if not timestamp_line or not speaker_text_lines:
            continue
        
        # Parse timestamp
        timestamp_match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})', timestamp_line)
        if not timestamp_match:
            continue
        
        start_time, end_time = timestamp_match.groups()
        
        # Parse speaker and text
        full_text = '\n'.join(speaker_text_lines)
        
        # Extract speaker (assuming format "SPEAKER_NAME: text")
        speaker_match = re.match(r'^([^:]+):\s*(.*)', full_text, re.DOTALL)
        if speaker_match:
            speaker = speaker_match.group(1).strip()
            text = speaker_match.group(2).strip()
        else:
            # If no speaker format found, treat entire text as content
            speaker = "UNKNOWN"
            text = full_text.strip()
        
        segments.append(TranscriptSegment(start_time, end_time, speaker, text, chapter_num))
    
    return segments

def consolidate_segments(segments: List[TranscriptSegment]) -> List[TranscriptSegment]:
    """Consolidate consecutive segments from the same speaker."""
    if not segments:
        return []
    
    consolidated = []
    current_segment = segments[0]
    
    for i in range(1, len(segments)):
        next_segment = segments[i]
        
        # If same speaker, consolidate
        if current_segment.speaker == next_segment.speaker:
            # Combine text with proper spacing
            if current_segment.text and next_segment.text:
                # Add space or newline between texts for readability
                current_segment.text += "\n" + next_segment.text
            elif next_segment.text:
                current_segment.text = next_segment.text
            
            # Update end time to the later segment's end time
            current_segment.end_time = next_segment.end_time
        else:
            # Different speaker, save current and start new
            consolidated.append(current_segment)
            current_segment = next_segment
    
    # Add the last segment
    consolidated.append(current_segment)
    
    return consolidated

def write_consolidated_transcript(segments: List[TranscriptSegment], output_path: str):
    """Write the consolidated transcript to a file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(segments):
            if i > 0:
                f.write('\n\n')
            f.write(str(segment))

def main():
    parser = argparse.ArgumentParser(description='Consolidate Zoom transcript segments by speaker')
    parser.add_argument('input_file', help='Input transcript file path')
    parser.add_argument('-o', '--output', help='Output file path (default: adds _consolidated to input filename)')
    
    args = parser.parse_args()
    
    # Parse input file
    print(f"Parsing transcript file: {args.input_file}")
    segments = parse_transcript_file(args.input_file)
    print(f"Found {len(segments)} segments")
    
    # Consolidate segments
    print("Consolidating consecutive segments from same speakers...")
    consolidated = consolidate_segments(segments)
    print(f"Consolidated to {len(consolidated)} segments")
    
    # Determine output file path
    if args.output:
        output_path = args.output
    else:
        input_parts = args.input_file.rsplit('.', 1)
        if len(input_parts) == 2:
            output_path = f"{input_parts[0]}_consolidated.{input_parts[1]}"
        else:
            output_path = f"{args.input_file}_consolidated"
    
    # Write consolidated transcript
    print(f"Writing consolidated transcript to: {output_path}")
    write_consolidated_transcript(consolidated, output_path)
    print("Done!")
    
    # Print summary
    print(f"\nSummary:")
    print(f"  Original segments: {len(segments)}")
    print(f"  Consolidated segments: {len(consolidated)}")
    print(f"  Reduction: {len(segments) - len(consolidated)} segments ({(len(segments) - len(consolidated))/len(segments)*100:.1f}%)")

if __name__ == "__main__":
    main()