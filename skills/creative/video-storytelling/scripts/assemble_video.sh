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
