# Narrative Design Reference

## Overview

Effective video storytelling requires careful narrative design that balances visual coherence, emotional engagement, and pacing. This guide covers story structure, scene design, dialogue writing, and emotion management for AI-generated video narratives.

## Story Structure

### Default Structure (6 Scenes)

**Scene 0: Title Scene**
- Duration: 10-15 seconds
- Purpose: Establish story premise, introduce main character
- Visual: Character in signature pose or setting
- Audio: Story title and brief setup narration
- Emotion: Neutral to slightly positive

**Scenes 1-5: Story Arc**
- Duration: 15-20 seconds each
- Purpose: Build narrative progression
- Total story time: 75-100 seconds (1:15-1:40)

### Three-Act Structure (Recommended)

**Act 1 - Setup (Scenes 0-1):**
- Introduce protagonist and world
- Establish normal state
- Present inciting incident

**Act 2 - Conflict (Scenes 2-4):**
- Character faces challenges
- Rising tension and obstacles
- Attempts and failures
- Build toward climax

**Act 3 - Resolution (Scene 5):**
- Climax and resolution
- Character transformation
- Emotional payoff
- Satisfying conclusion

### Example: "Pyter's First Bug"

```python
story_structure = {
    "scene_0": {
        "act": "Title",
        "purpose": "Introduction",
        "description": "Pyter the Python snake sits at computer, ready to code",
        "emotion": "neutral",
        "arc_position": "setup"
    },
    "scene_1": {
        "act": "Act 1 - Setup",
        "purpose": "Normal world",
        "description": "Pyter coding happily, everything working smoothly",
        "emotion": "happy",
        "arc_position": "normal_state"
    },
    "scene_2": {
        "act": "Act 2 - Conflict",
        "purpose": "Inciting incident",
        "description": "Bug appears! Small orange bug sits on Pyter's keyboard",
        "emotion": "surprised",
        "arc_position": "problem_introduced"
    },
    "scene_3": {
        "act": "Act 2 - Conflict",
        "purpose": "Rising action",
        "description": "Pyter investigates the bug, looking confused and focused",
        "emotion": "focused",
        "arc_position": "investigation"
    },
    "scene_4": {
        "act": "Act 2 - Conflict",
        "purpose": "Climax",
        "description": "Pyter finds the solution, debugging the code",
        "emotion": "excited",
        "arc_position": "breakthrough"
    },
    "scene_5": {
        "act": "Act 3 - Resolution",
        "purpose": "Resolution",
        "description": "Code works! Pyter celebrates, bug is now a friend",
        "emotion": "triumphant",
        "arc_position": "success"
    }
}
```

## Scene Design

### Scene Components

Each scene should define:

1. **Visual Description** (50-100 words)
   - Character placement and pose
   - Environmental elements
   - Key visual focus
   - Camera angle/framing

2. **Narration Text** (50-80 words)
   - Advances the story
   - Character thoughts or dialogue
   - Scene context
   - Emotional subtext

3. **Emotion Tag** (single word)
   - Guides voice performance
   - Sets scene mood
   - Influences pacing

4. **Arc Position** (story progression)
   - Where in the narrative arc
   - Tension level
   - Energy direction

### Scene Template

```python
scene = {
    "number": 2,
    "title": "The Problem Appears",

    "visual": {
        "description": """
            Pyter sits at his desk, coiled around the chair. His eyes widen
            as he spots something on the keyboard. A small orange bug sits
            on the spacebar. Pyter's expression shifts from focused to
            surprised. The computer screen glows in background.
        """,
        "composition": "Medium shot, eye-level",
        "focus": "Pyter's surprised face and the bug",
        "lighting": "Warm desk lamp, slight dramatic shadow"
    },

    "narration": {
        "text": """
            Pyter was deep in his code when something caught his eye.
            A tiny orange bug sat right on his keyboard! He'd seen bugs
            in his code before, but never a real bug on his computer.
            This was going to be interesting.
        """,
        "emotion": "surprised",
        "character": "Pyter",
        "voice_id": "JBFqnCBsd6RMkjVDRZzb"  # George - narrative voice
    },

    "arc": {
        "act": 2,
        "position": "inciting_incident",
        "tension": "low-medium",
        "energy": "rising"
    }
}
```

### Visual Continuity Between Scenes

Maintain visual flow:

**Bad Transition:**
```
Scene 2: Pyter at desk, facing left
Scene 3: Pyter at desk, facing right (jarring jump)
```

**Good Transition:**
```
Scene 2: Pyter at desk, facing left, looking down at bug
Scene 3: Pyter at desk, still facing left, leaning closer to bug (smooth progression)
```

**Techniques:**
- Maintain consistent character orientation
- Progressive camera movement (slow zoom, pan)
- Logical spatial relationships
- Smooth action flow

## Dialogue and Narration

### Narration Length Guidelines

**Target: 50-80 words per scene**
- 15-20 seconds of audio
- Natural reading pace
- Not too rushed, not too slow

**Word Count Examples:**

**Too Short (30 words):**
```
Pyter was coding. A bug appeared. He was surprised. He looked at it.
```
*Problem: Feels rushed, no emotional depth*

**Good (60 words):**
```
Pyter was deep in his code when something caught his eye. A tiny orange
bug sat right on his keyboard! He'd seen bugs in his code before, but
never a real bug on his computer. This was going to be interesting.
```
*Perfect: Natural pacing, emotional context, story advancement*

**Too Long (120 words):**
```
Pyter the Python snake had been coding for hours at his computer desk,
writing line after line of beautiful Python code, when suddenly something
very unusual happened that completely interrupted his workflow and made
him stop what he was doing immediately. A small orange bug, the kind you
might find in a garden, had somehow made its way into his home office and
was now sitting directly on the spacebar of his keyboard...
```
*Problem: Too verbose, loses focus, narration feels slow*

### Writing Effective Narration

**Show, Don't Tell:**

**Bad:**
```
Pyter was very happy because he fixed the bug successfully.
```

**Good:**
```
Pyter's eyes lit up as the code compiled perfectly. Success! The bug
was fixed, and he learned something new.
```

**Active Voice:**

**Bad (Passive):**
```
The bug was found by Pyter after careful investigation.
```

**Good (Active):**
```
Pyter investigated carefully and found the bug hiding in line forty-two.
```

**Emotional Resonance:**

**Bad (Flat):**
```
Pyter debugged the code. It worked. He continued programming.
```

**Good (Engaging):**
```
With one final keystroke, Pyter's code sprang to life! His heart soared
as the program ran flawlessly. This was why he loved programming.
```

### Dialogue vs Narration

**Third-Person Narration (Recommended for Default):**
```python
narration = {
    "text": "Pyter examined the bug closely, wondering how it got there.",
    "character": "Pyter",
    "emotion": "curious"
}
```
*Advantages: Professional, clear story progression, easier consistency*

**First-Person Narration:**
```python
narration = {
    "text": "I couldn't believe my eyes. A real bug, right on my keyboard!",
    "character": "Pyter",
    "emotion": "surprised"
}
```
*Advantages: Personal connection, character voice, immediacy*

**Direct Dialogue (Multi-Character):**
```python
dialogue = [
    {
        "character": "Pyter",
        "text": "Well hello there, little bug. What brings you to my desk?",
        "emotion": "friendly"
    },
    {
        "character": "Bug",
        "text": "I heard you were looking for bugs! Here I am!",
        "emotion": "cheerful"
    }
]
```
*Advantages: Character interaction, dynamic, engaging*

## Emotion Tags

### Available Emotion Tags

ElevenLabs supports rich emotion tagging in narration:

**Primary Emotions:**
- `neutral` - Default, balanced tone
- `happy` - Joyful, upbeat, positive
- `sad` - Melancholic, somber, down
- `angry` - Frustrated, upset, intense
- `fearful` - Scared, anxious, worried
- `surprised` - Shocked, amazed, startled
- `disgusted` - Repulsed, negative reaction

**Nuanced Emotions:**
- `excited` - Enthusiastic, energetic, thrilled
- `focused` - Concentrated, serious, determined
- `curious` - Inquisitive, wondering, interested
- `triumphant` - Victorious, accomplished, proud
- `disappointed` - Let down, discouraged
- `amused` - Entertained, finding humor
- `thoughtful` - Reflective, pondering, considering
- `gentle` - Soft, kind, soothing

### Emotion Tag Usage

```python
# Scene-by-scene emotion progression
story_emotions = {
    "scene_0": "neutral",      # Introduction, setting stage
    "scene_1": "happy",        # Everything going well
    "scene_2": "surprised",    # Problem appears!
    "scene_3": "focused",      # Working on solution
    "scene_4": "excited",      # Breakthrough moment
    "scene_5": "triumphant"    # Victory and resolution
}
```

### Emotion Arc Examples

**Discovery Story Arc:**
```python
emotions = ["curious", "excited", "focused", "surprised", "amazed", "triumphant"]
```

**Overcoming Challenge:**
```python
emotions = ["neutral", "happy", "worried", "determined", "focused", "triumphant"]
```

**Learning Experience:**
```python
emotions = ["curious", "confused", "thoughtful", "focused", "excited", "happy"]
```

**Friendship Story:**
```python
emotions = ["neutral", "curious", "friendly", "amused", "happy", "gentle"]
```

## Pacing and Timing

### Scene Duration Strategy

**Title Scene (Scene 0):**
- Target: 10-15 seconds
- Narration: 30-50 words
- Purpose: Quick introduction
- Pace: Moderate

**Story Scenes (Scenes 1-5):**
- Target: 15-20 seconds each
- Narration: 50-80 words
- Purpose: Story development
- Pace: Natural conversational

**Total Video Length:**
- 6 scenes × ~17 seconds average = ~102 seconds (1:42)
- Comfortable viewing length
- Maintains engagement
- Complete story arc

### Audio-Visual Sync

The video assembly calculates equal time per image based on total audio:

```bash
# Example calculation
total_audio_duration = 102 seconds
num_images = 6
seconds_per_image = 102 / 6 = 17 seconds per image
```

**This means:**
- Don't worry about exact narration timing
- Focus on word count (50-80 words)
- Natural speech will be ~15-20 seconds
- Video will auto-adjust timing

### Pacing Variety

**Fast-Paced Action:**
```python
scene = {
    "narration": "Pyter spotted the bug and pounced! No time to waste!",
    "words": 45,  # Shorter for urgency
    "emotion": "excited"
}
```

**Slow Contemplative:**
```python
scene = {
    "narration": """
        Pyter sat quietly, studying the code line by line. Each function,
        each variable, told part of the story. Somewhere in these lines
        was the answer he was searching for.
    """,
    "words": 75,  # Longer for reflection
    "emotion": "thoughtful"
}
```

## Character Voice Assignment

### Default Voice Mapping

Based on character attributes:

```python
def assign_voice(character):
    """Auto-assign ElevenLabs voice based on character profile"""

    age = character.get('age', 'young')
    gender = character.get('gender', 'male')
    role = character.get('role', 'character')

    # Narrator voices (third-person narration)
    if role == 'narrator':
        if gender == 'male':
            return 'JBFqnCBsd6RMkjVDRZzb'  # George - narrative male
        else:
            return '21m00Tcm4TlvDq8ikWAM'  # Rachel - narrative female

    # Character voices (dialogue)
    if age == 'young':
        if gender == 'male':
            return 'TxGEqnHWrfWFTfGW9XjX'  # Josh - young energetic male
        else:
            return 'EXAVITQu4vr4xnSDxMaL'  # Bella - young expressive female
    elif age == 'middle':
        if gender == 'male':
            return 'VR6AewLTigWG4xSOukaG'  # Arnold - middle-aged male
        else:
            return 'MF3mGyEYCl7XYWbV9V6O'  # Elli - middle-aged female
    elif age == 'old':
        if gender == 'male':
            return 'ErXwobaYiN019PkySvjV'  # Antoni - older male
        else:
            return 'ThT5KcBeYPX3keUQqHPh'  # Dorothy - older female

    # Default fallback
    return 'JBFqnCBsd6RMkjVDRZzb'  # George
```

### Voice Characteristics

**George (`JBFqnCBsd6RMkjVDRZzb`):**
- Male narrator voice
- Warm, professional, clear
- Perfect for third-person narration
- Age: Adult male
- Best for: Story narration, audiobooks, professional content

**Rachel (`21m00Tcm4TlvDq8ikWAM`):**
- Female narrator voice
- Calm, soothing, clear
- Great for gentle narratives
- Age: Young adult female
- Best for: Calm narration, educational content, bedtime stories

**Josh (`TxGEqnHWrfWFTfGW9XjX`):**
- Young energetic male
- Upbeat, enthusiastic, friendly
- Perfect for youthful characters
- Age: Young adult
- Best for: Energetic characters, action, excitement

**Bella (`EXAVITQu4vr4xnSDxMaL`):**
- Young expressive female
- Bright, cheerful, dynamic
- Great for lively characters
- Age: Young adult
- Best for: Cheerful characters, lighthearted stories

### Multi-Character Dialogue

When multiple characters speak:

```python
dialogue_scenes = [
    {
        "character": "Pyter",
        "text": "Well hello there, little bug!",
        "emotion": "friendly",
        "voice_id": "JBFqnCBsd6RMkjVDRZzb"  # George
    },
    {
        "character": "Bug",
        "text": "Hi! I'm here to help you debug!",
        "emotion": "cheerful",
        "voice_id": "EXAVITQu4vr4xnSDxMaL"  # Bella
    }
]

# Use ElevenLabs text_to_dialogue API
audio = client.text_to_dialogue.convert(
    dialogue=dialogue_scenes
)
```

## Story Planning Workflow

### Step 1: Define Core Elements

```python
story_plan = {
    "title": "Pyter's First Bug",
    "theme": "Problem-solving and friendship",
    "protagonist": "Pyter the Python snake",
    "central_conflict": "Finding and fixing a bug",
    "resolution": "Bug becomes a friend",
    "tone": "Lighthearted, educational, positive",
    "target_length": "6 scenes, ~100 seconds"
}
```

### Step 2: Create Story Arc

```python
arc = [
    {"scene": 0, "beat": "Introduction", "tension": 0},
    {"scene": 1, "beat": "Normal world", "tension": 1},
    {"scene": 2, "beat": "Inciting incident", "tension": 3},
    {"scene": 3, "beat": "Rising action", "tension": 5},
    {"scene": 4, "beat": "Climax", "tension": 7},
    {"scene": 5, "beat": "Resolution", "tension": 2}
]
```

### Step 3: Define Characters

```python
characters = {
    "Pyter": {
        "role": "protagonist",
        "species": "python snake",
        "personality": "curious, friendly, determined",
        "goal": "write perfect code",
        "voice": "narrator",
        "age": "young",
        "gender": "male"
    },
    "Bug": {
        "role": "supporting",
        "species": "small beetle",
        "personality": "helpful, cheerful, innocent",
        "purpose": "teach Pyter about debugging",
        "voice": "character",
        "age": "young",
        "gender": "neutral"
    }
}
```

### Step 4: Write Scene Descriptions

```python
scenes = {
    "scene_0": {
        "visual": "Pyter at computer, ready to code",
        "narration": "Meet Pyter, a Python snake who loves to code...",
        "emotion": "neutral"
    },
    # ... continue for all scenes
}
```

### Step 5: Review Story Flow

Checklist:
- [ ] Clear beginning, middle, end
- [ ] Character motivation established
- [ ] Conflict introduced and resolved
- [ ] Emotional arc progresses naturally
- [ ] Visual continuity maintained
- [ ] Narration length consistent (50-80 words)
- [ ] Emotion tags varied and appropriate
- [ ] Each scene advances story

## Common Narrative Patterns

### The Hero's Journey (Simplified)

```python
scenes = {
    "scene_0": "Ordinary world - introduce hero",
    "scene_1": "Call to adventure - problem appears",
    "scene_2": "Facing challenge - hero struggles",
    "scene_3": "Gaining knowledge - learning moment",
    "scene_4": "Climax - using new knowledge",
    "scene_5": "Return transformed - hero succeeds"
}
```

### Problem-Solution

```python
scenes = {
    "scene_0": "Setup - normal state",
    "scene_1": "Problem identified",
    "scene_2": "First attempt fails",
    "scene_3": "New approach",
    "scene_4": "Solution discovered",
    "scene_5": "Success and learning"
}
```

### Transformation

```python
scenes = {
    "scene_0": "Character in initial state",
    "scene_1": "Catalyst for change",
    "scene_2": "Resistance to change",
    "scene_3": "Accepting change",
    "scene_4": "Embracing new state",
    "scene_5": "Transformed character"
}
```

### Discovery

```python
scenes = {
    "scene_0": "Setting out to explore",
    "scene_1": "First discovery",
    "scene_2": "Deeper investigation",
    "scene_3": "Surprising revelation",
    "scene_4": "Understanding emerges",
    "scene_5": "Knowledge applied"
}
```

## Best Practices

### Do's

✅ **Keep narration concise** (50-80 words per scene)
✅ **Use varied emotion tags** (avoid monotone)
✅ **Maintain visual continuity** (reference previous scenes)
✅ **Progress story logically** (clear cause and effect)
✅ **Show character emotion** (don't just tell)
✅ **End with resolution** (satisfying conclusion)
✅ **Test emotion tags** (listen to generated audio)
✅ **Plan before generating** (outline story first)

### Don'ts

❌ **Don't rush the story** (let scenes breathe)
❌ **Don't repeat descriptions** (each scene should advance)
❌ **Don't ignore emotion tags** (they dramatically affect delivery)
❌ **Don't make scenes too long** (>100 words feels slow)
❌ **Don't forget character consistency** (maintain personality)
❌ **Don't leave threads hanging** (resolve what you introduce)
❌ **Don't over-explain** (trust visual storytelling)
❌ **Don't mix tones** (maintain consistent story feel)

## Example: Complete Story Plan

```python
story = {
    "metadata": {
        "title": "Pyter's First Bug",
        "theme": "Problem-solving and friendship",
        "tone": "Lighthearted educational",
        "target_audience": "All ages",
        "duration": "~100 seconds"
    },

    "characters": {
        "Pyter": {
            "species": "python snake",
            "personality": "curious, friendly, determined",
            "voice_id": "JBFqnCBsd6RMkjVDRZzb",
            "colors": "#0B5FFF, #FFB703"
        },
        "Bug": {
            "species": "small beetle",
            "personality": "helpful, cheerful",
            "voice_id": "EXAVITQu4vr4xnSDxMaL",
            "colors": "#FB8500, #023047"
        }
    },

    "scenes": [
        {
            "number": 0,
            "title": "Meet Pyter",
            "visual": "Pyter at computer desk, coiled and ready",
            "narration": """
                Meet Pyter, a Python snake who loves to code. Today he's
                working on his most ambitious project yet, a program to
                help other snakes learn programming. Little does he know,
                an unexpected visitor is about to change everything.
            """,
            "emotion": "neutral",
            "arc_position": "introduction"
        },
        {
            "number": 1,
            "title": "Coding Time",
            "visual": "Pyter typing happily, screen glowing",
            "narration": """
                Pyter's code flowed smoothly, each line more elegant than
                the last. Functions nested perfectly, variables named just
                right. This was his happy place, where logic and creativity
                danced together in perfect harmony.
            """,
            "emotion": "happy",
            "arc_position": "normal_state"
        },
        {
            "number": 2,
            "title": "The Bug Appears",
            "visual": "Small orange bug on keyboard, Pyter surprised",
            "narration": """
                Pyter was deep in his code when something caught his eye.
                A tiny orange bug sat right on his keyboard! He'd seen bugs
                in his code before, but never a real bug on his computer.
                This was going to be interesting.
            """,
            "emotion": "surprised",
            "arc_position": "inciting_incident"
        },
        {
            "number": 3,
            "title": "Investigation",
            "visual": "Pyter examining bug closely, focused expression",
            "narration": """
                Pyter leaned in closer, studying the little creature. It had
                six legs and bright orange spots. Wait a minute... orange
                spots? Just like the error messages in his console! Could
                this bug be trying to help him find the bugs in his code?
            """,
            "emotion": "curious",
            "arc_position": "investigation"
        },
        {
            "number": 4,
            "title": "The Fix",
            "visual": "Pyter and bug working together, excited",
            "narration": """
                Together they found it! Line forty-two had a tiny typo that
                Pyter had missed a dozen times. The bug's cheerful presence
                had helped him see it with fresh eyes. Sometimes the best
                debugging tool is a new perspective!
            """,
            "emotion": "excited",
            "arc_position": "climax"
        },
        {
            "number": 5,
            "title": "Success",
            "visual": "Code running perfectly, Pyter and bug celebrating",
            "narration": """
                The program ran flawlessly! Pyter's code lit up the screen
                in beautiful success messages. He smiled at his new friend
                the bug, who had taught him that sometimes the best way to
                find bugs in your code is to find a real bug who cares.
            """,
            "emotion": "triumphant",
            "arc_position": "resolution"
        }
    ]
}
```

## Resources

- SKILL.md for implementation code
- style-locks.md for visual consistency
- video-assembly.md for technical pipeline
- example-stories.md for complete walkthroughs
- character-profiles.md for character templates
