# Video Assembly Reference

## Overview

Video assembly combines generated images and audio narration into a final MP4 video file. The process uses ffmpeg to create equal-duration frames from images, concatenate audio files, and merge everything into a synchronized video.

## Pipeline Overview

```
┌─────────────────┐
│ Generated Images│  scene_000.png, scene_001.png, ..., scene_005.png
│  (6 images)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Generated Audio │  scene_000.mp3, scene_001.mp3, ..., scene_005.mp3
│  (6 audio files)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Concatenate    │  merged_audio.mp3 (all audio combined)
│     Audio       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Calculate      │  total_duration / num_images = seconds_per_image
│  Timing         │  Example: 102s / 6 images = 17s per image
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Create Video   │  For each image, show for calculated duration
│  from Images    │  30 fps, equal time per image
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Merge Audio    │  Combine image video with merged audio
│  and Video      │  Sync timing, add audio track
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Final Output   │  final_video.mp4
│                 │  H.264 video, AAC audio, optimized
└─────────────────┘
```

## Bash Script

The complete video assembly script is embedded in the skill:

```bash
#!/bin/bash
# assemble_video.sh
# Combines images and audio into final MP4 video

set -e  # Exit on error

# Configuration
OUTPUT_DIR=${1:-"./output"}
FINAL_VIDEO=${2:-"final_video.mp4"}
FPS=30

echo "🎬 Video Assembly Starting..."
echo "Output directory: $OUTPUT_DIR"
echo "Final video: $FINAL_VIDEO"

# Step 1: Verify all required files exist
echo ""
echo "📋 Step 1: Verifying files..."

IMAGE_COUNT=$(ls -1 "$OUTPUT_DIR"/scene_*.png 2>/dev/null | wc -l | tr -d ' ')
AUDIO_COUNT=$(ls -1 "$OUTPUT_DIR"/scene_*.mp3 2>/dev/null | wc -l | tr -d ' ')

echo "  Found $IMAGE_COUNT images"
echo "  Found $AUDIO_COUNT audio files"

if [ "$IMAGE_COUNT" -eq 0 ]; then
    echo "❌ Error: No scene images found in $OUTPUT_DIR"
    exit 1
fi

if [ "$AUDIO_COUNT" -eq 0 ]; then
    echo "❌ Error: No scene audio found in $OUTPUT_DIR"
    exit 1
fi

if [ "$IMAGE_COUNT" -ne "$AUDIO_COUNT" ]; then
    echo "⚠️  Warning: Image count ($IMAGE_COUNT) != Audio count ($AUDIO_COUNT)"
fi

# Step 2: Create audio file list for concatenation
echo ""
echo "🎵 Step 2: Preparing audio concatenation..."

AUDIO_LIST="$OUTPUT_DIR/audio_files.txt"
> "$AUDIO_LIST"  # Clear file

for audio in "$OUTPUT_DIR"/scene_*.mp3; do
    echo "file '$(basename "$audio")'" >> "$AUDIO_LIST"
done

echo "  Created audio file list: $AUDIO_LIST"

# Step 3: Concatenate all audio files
echo ""
echo "🎵 Step 3: Concatenating audio..."

MERGED_AUDIO="$OUTPUT_DIR/merged_audio.mp3"
ffmpeg -f concat -safe 0 -i "$AUDIO_LIST" -c copy "$MERGED_AUDIO" -y -loglevel error

if [ ! -f "$MERGED_AUDIO" ]; then
    echo "❌ Error: Failed to create merged audio"
    exit 1
fi

echo "  Created merged audio: $MERGED_AUDIO"

# Step 4: Get total audio duration
echo ""
echo "⏱️  Step 4: Calculating timing..."

TOTAL_DURATION=$(ffprobe -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 "$MERGED_AUDIO")

echo "  Total audio duration: ${TOTAL_DURATION}s"

# Calculate seconds per image (equal distribution)
SECONDS_PER_IMAGE=$(echo "scale=2; $TOTAL_DURATION / $IMAGE_COUNT" | bc)

echo "  Seconds per image: ${SECONDS_PER_IMAGE}s"
echo "  Total images: $IMAGE_COUNT"

# Step 5: Create image list with durations
echo ""
echo "🖼️  Step 5: Creating image sequence..."

IMAGE_LIST="$OUTPUT_DIR/image_files.txt"
> "$IMAGE_LIST"  # Clear file

for image in "$OUTPUT_DIR"/scene_*.png; do
    echo "file '$(basename "$image")'" >> "$IMAGE_LIST"
    echo "duration $SECONDS_PER_IMAGE" >> "$IMAGE_LIST"
done

# Add last image again (ffmpeg concat quirk)
LAST_IMAGE=$(ls -1 "$OUTPUT_DIR"/scene_*.png | tail -1)
echo "file '$(basename "$LAST_IMAGE")'" >> "$IMAGE_LIST"

echo "  Created image file list: $IMAGE_LIST"

# Step 6: Create video from images
echo ""
echo "🎬 Step 6: Creating video from images..."

TEMP_VIDEO="$OUTPUT_DIR/temp_video.mp4"
ffmpeg -f concat -safe 0 -i "$IMAGE_LIST" \
    -vf "fps=$FPS,format=yuv420p,scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2" \
    -c:v libx264 -preset medium -crf 23 \
    "$TEMP_VIDEO" -y -loglevel error

if [ ! -f "$TEMP_VIDEO" ]; then
    echo "❌ Error: Failed to create temp video"
    exit 1
fi

echo "  Created temp video: $TEMP_VIDEO"

# Step 7: Merge video and audio
echo ""
echo "🎬 Step 7: Merging video and audio..."

ffmpeg -i "$TEMP_VIDEO" -i "$MERGED_AUDIO" \
    -c:v copy -c:a aac -b:a 192k -shortest \
    "$OUTPUT_DIR/$FINAL_VIDEO" -y -loglevel error

if [ ! -f "$OUTPUT_DIR/$FINAL_VIDEO" ]; then
    echo "❌ Error: Failed to create final video"
    exit 1
fi

echo "  Created final video: $OUTPUT_DIR/$FINAL_VIDEO"

# Step 8: Get final video info
echo ""
echo "📊 Step 8: Final video information..."

VIDEO_DURATION=$(ffprobe -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 "$OUTPUT_DIR/$FINAL_VIDEO")
VIDEO_SIZE=$(du -h "$OUTPUT_DIR/$FINAL_VIDEO" | cut -f1)

echo "  Duration: ${VIDEO_DURATION}s"
echo "  File size: $VIDEO_SIZE"
echo "  Resolution: 1080x1080"
echo "  Frame rate: ${FPS} fps"
echo "  Video codec: H.264"
echo "  Audio codec: AAC"

# Step 9: Cleanup temporary files
echo ""
echo "🧹 Step 9: Cleaning up..."

rm -f "$AUDIO_LIST"
rm -f "$IMAGE_LIST"
rm -f "$MERGED_AUDIO"
rm -f "$TEMP_VIDEO"

echo "  Removed temporary files"

# Complete
echo ""
echo "✅ Video assembly complete!"
echo "📹 Final video: $OUTPUT_DIR/$FINAL_VIDEO"
echo ""
```

## Usage

### Basic Usage

```bash
# From output directory containing scene_*.png and scene_*.mp3
cd output
bash ../scripts/assemble_video.sh ./ my_story.mp4
```

### From Python

```python
import subprocess
from pathlib import Path

def assemble_video(output_dir: str, final_video: str = "final_video.mp4"):
    """
    Assemble video from generated images and audio

    Args:
        output_dir: Directory containing scene_*.png and scene_*.mp3
        final_video: Output video filename
    """
    script_path = Path(__file__).parent / "scripts" / "assemble_video.sh"

    result = subprocess.run(
        ["bash", str(script_path), output_dir, final_video],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Video assembly failed: {result.stderr}")

    print(result.stdout)
    return Path(output_dir) / final_video

# Usage
video_path = assemble_video("./output", "pyter_story.mp4")
print(f"Video created: {video_path}")
```

### With Custom Settings

```bash
# Custom FPS (edit script)
FPS=60 bash assemble_video.sh ./output high_fps_video.mp4

# Different output directory
bash assemble_video.sh /path/to/scenes final.mp4

# Current directory
bash assemble_video.sh . story.mp4
```

## Technical Details

### Image Processing

**Scaling and Padding:**
```bash
-vf "fps=$FPS,format=yuv420p,scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2"
```

**Breakdown:**
- `fps=$FPS` - Set frame rate (30 fps)
- `format=yuv420p` - Color format for compatibility
- `scale=1080:1080:force_original_aspect_ratio=decrease` - Fit to 1080x1080
- `pad=1080:1080:(ow-iw)/2:(oh-ih)/2` - Center with padding if needed

**Why These Settings:**
- Ensures all images fit 1080x1080 square format
- Maintains aspect ratio (no stretching)
- Centers image with black padding if needed
- Compatible with most video players

### Audio Concatenation

**File List Format (audio_files.txt):**
```
file 'scene_000.mp3'
file 'scene_001.mp3'
file 'scene_002.mp3'
file 'scene_003.mp3'
file 'scene_004.mp3'
file 'scene_005.mp3'
```

**ffmpeg Command:**
```bash
ffmpeg -f concat -safe 0 -i audio_files.txt -c copy merged_audio.mp3
```

**Why This Approach:**
- `-f concat` - Use concat demuxer
- `-safe 0` - Allow absolute paths
- `-c copy` - Copy codec (no re-encoding, fast)
- Preserves audio quality
- No gaps between clips

### Duration Calculation

**Using bc for Precision:**
```bash
TOTAL_DURATION=102.5
IMAGE_COUNT=6
SECONDS_PER_IMAGE=$(echo "scale=2; $TOTAL_DURATION / $IMAGE_COUNT" | bc)
# Result: 17.08 seconds per image
```

**Why Equal Distribution:**
- Simplest approach
- Consistent pacing
- Predictable viewing experience
- Matches total audio duration exactly

**Alternative (Custom Durations):**
```bash
# Could customize per scene if needed
DURATIONS=(15 18 20 17 16 16.5)  # Custom per scene
```

### Video Encoding

**H.264 Settings:**
```bash
-c:v libx264 -preset medium -crf 23
```

**Breakdown:**
- `libx264` - H.264 codec (universal compatibility)
- `-preset medium` - Balance speed/compression
- `-crf 23` - Constant Rate Factor (quality: 0=best, 51=worst)

**Quality vs File Size:**
- CRF 18: Very high quality, large files
- CRF 23: Good quality, reasonable size (recommended)
- CRF 28: Lower quality, small files

**Audio Encoding:**
```bash
-c:a aac -b:a 192k
```

**Breakdown:**
- `aac` - AAC codec (universal compatibility)
- `-b:a 192k` - Bitrate 192 kbps (high quality)

### Sync and Merging

**Final Merge:**
```bash
ffmpeg -i temp_video.mp4 -i merged_audio.mp3 \
    -c:v copy -c:a aac -b:a 192k -shortest \
    final_video.mp4
```

**Breakdown:**
- `-c:v copy` - Copy video (no re-encode)
- `-c:a aac` - Encode audio as AAC
- `-shortest` - End when shortest stream ends (prevents black frames)

## Troubleshooting

### Error: No such file or directory

**Problem:** Script can't find images or audio files

**Solution:**
```bash
# Verify files exist
ls -la output/scene_*.png
ls -la output/scene_*.mp3

# Check naming pattern
# Should be: scene_000.png, scene_001.png, etc.
#            scene_000.mp3, scene_001.mp3, etc.
```

### Error: Audio/video desynchronization

**Problem:** Audio and video don't match

**Solution:**
- Check that image count matches audio count
- Verify all audio files have content (not 0 bytes)
- Ensure no corrupt audio files
- Use `-shortest` flag (already in script)

### Error: ffmpeg not found

**Problem:** ffmpeg not installed

**Solution:**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Verify installation
ffmpeg -version
ffprobe -version
```

### Error: Video quality is poor

**Problem:** Video looks compressed or pixelated

**Solution:**
```bash
# Lower CRF value (higher quality)
-crf 18  # Instead of -crf 23

# Use slower preset (better compression)
-preset slow  # Instead of -preset medium

# Higher bitrate
-b:v 5M  # Explicit bitrate instead of CRF
```

### Error: File size too large

**Problem:** Final video is too big

**Solution:**
```bash
# Higher CRF value (lower quality, smaller file)
-crf 28  # Instead of -crf 23

# Lower audio bitrate
-b:a 128k  # Instead of -b:a 192k

# Lower resolution (if acceptable)
scale=720:720  # Instead of 1080:1080
```

### Error: Images don't fill frame

**Problem:** Black bars around images

**Solution:**
- Images should be generated at 1080x1080 (specified in STYLE_LOCK)
- If different size, adjust scale parameter
- Check image aspect ratio

```bash
# Force stretch (not recommended, distorts)
scale=1080:1080

# Better: Generate images at correct size
# In STYLE_LOCK: "Aspect ratio: 1080×1080 (square)"
```

## Advanced Techniques

### Custom Image Durations

Modify script to support custom per-scene durations:

```bash
# In image_files.txt, use different durations
file 'scene_000.png'
duration 12.0
file 'scene_001.png'
duration 18.5
file 'scene_002.png'
duration 20.0
# etc.
```

### Transitions Between Scenes

Add crossfade transitions:

```bash
# Simple crossfade (requires complex filter)
ffmpeg -i scene_000.png -i scene_001.png \
    -filter_complex "[0][1]xfade=transition=fade:duration=1:offset=5" \
    output.mp4
```

**Note:** Crossfades are complex with concat. Simpler to use straight cuts (default).

### Background Music

Add background music track:

```bash
# Mix narration with background music
ffmpeg -i merged_audio.mp3 -i background_music.mp3 \
    -filter_complex "[0:a][1:a]amix=inputs=2:duration=shortest:dropout_transition=2" \
    -c:a aac final_audio.mp3

# Then use final_audio.mp3 in video merge
```

### Subtitles/Captions

Add text subtitles:

```bash
# Create subtitles.srt file
# Then burn into video
ffmpeg -i final_video.mp4 -vf "subtitles=subtitles.srt" \
    -c:a copy final_with_subs.mp4
```

### Resolution Variants

Create multiple resolutions:

```bash
# 1080p (square)
scale=1080:1080

# 720p (square, smaller file)
scale=720:720

# 4K (square, very large)
scale=2160:2160

# Widescreen 1080p
scale=1920:1080
```

## Performance Optimization

### Parallel Processing

Process multiple videos simultaneously:

```bash
# In separate terminals or background jobs
bash assemble_video.sh story1_output story1.mp4 &
bash assemble_video.sh story2_output story2.mp4 &
bash assemble_video.sh story3_output story3.mp4 &
wait  # Wait for all to complete
```

### Faster Encoding

Use faster preset for quick previews:

```bash
# Fast preview (lower quality)
-preset ultrafast -crf 28

# Slower production (best quality)
-preset slow -crf 18
```

### Hardware Acceleration

Use GPU encoding if available:

```bash
# NVIDIA GPU (h264_nvenc)
-c:v h264_nvenc -preset fast -b:v 5M

# macOS VideoToolbox (h264_videotoolbox)
-c:v h264_videotoolbox -b:v 5M

# AMD GPU (h264_amf)
-c:v h264_amf -b:v 5M
```

**Note:** Availability depends on system hardware and ffmpeg build.

## File Size Estimates

Typical file sizes for 100-second video:

**High Quality (CRF 18):**
- Video: ~15-20 MB
- Audio (192k): ~2.4 MB
- Total: ~17-22 MB

**Medium Quality (CRF 23, default):**
- Video: ~8-12 MB
- Audio (192k): ~2.4 MB
- Total: ~10-15 MB

**Low Quality (CRF 28):**
- Video: ~4-6 MB
- Audio (128k): ~1.6 MB
- Total: ~6-8 MB

## Output Specifications

**Final Video Format:**
- Container: MP4
- Video Codec: H.264 (libx264)
- Audio Codec: AAC
- Resolution: 1080x1080 (square)
- Frame Rate: 30 fps
- Video Quality: CRF 23 (medium-high)
- Audio Bitrate: 192 kbps
- Color Space: YUV420p

**Compatibility:**
- ✅ Web browsers (Chrome, Firefox, Safari)
- ✅ Mobile devices (iOS, Android)
- ✅ Social media (Instagram, TikTok, YouTube)
- ✅ Video players (VLC, QuickTime, Windows Media Player)
- ✅ Video editors (Premiere, Final Cut, DaVinci Resolve)

## Resources

- **ffmpeg Documentation**: https://ffmpeg.org/documentation.html
- **H.264 Encoding Guide**: https://trac.ffmpeg.org/wiki/Encode/H.264
- **AAC Encoding Guide**: https://trac.ffmpeg.org/wiki/Encode/AAC
- **Concat Demuxer**: https://trac.ffmpeg.org/wiki/Concatenate

## Related Files

- `scripts/assemble_video.sh` - The actual bash script
- `SKILL.md` - Main skill with Python integration
- `narrative-design.md` - Story structure and pacing
- `style-locks.md` - Visual consistency guidelines
