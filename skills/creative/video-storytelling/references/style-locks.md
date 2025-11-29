# Style Locks Reference

## Overview

Style locks are textual constraints that ensure visual and narrative consistency across multi-scene story sequences. They prevent visual drift, maintain character appearance, and create professional-looking coherent video narratives.

## Types of Locks

### 1. STYLE_LOCK (Global Visual Consistency)

The STYLE_LOCK defines global visual characteristics that apply to every scene in the story. It controls:

- **Aspect Ratio**: Image dimensions
- **Camera**: Lens focal length and perspective
- **Lighting**: Light sources, color temperature, mood
- **Color Palette**: Primary colors used throughout
- **Materials**: Surface finishes and textures
- **Background**: Environmental characteristics
- **Style**: Overall artistic approach
- **Post-processing**: Final image treatment

**Default STYLE_LOCK:**

```
Aspect ratio: 1080×1080 (square)
Camera: 50mm lens, eye-level perspective
Lighting: soft three-point lighting, warm key light (4500K)
Color palette: #0B5FFF, #FFB703, #FB8500, #023047, #8ECAE6
Materials: matte finish, no film grain or heavy bloom
Background: subtle gradient, clean composition
Style: semi-realistic cartoon with clear lines and gentle shading
Post: crisp focus, no vignette or text artifacts
```

### 2. CHARACTER_LOCK (Character Appearance)

CHARACTER_LOCK maintains consistent character appearance across all scenes. Define once per character:

```python
CHARACTER_LOCK = {
    "Pyter": """
        Species: cartoon python snake
        Colors: bright blue body (#0B5FFF) with yellow accents (#FFB703)
        Features: round friendly eyes, small smile, coiled body position
        Clothing: small developer beanie hat
        Size: medium-sized snake, about 3 feet visible
        Style: semi-realistic cartoon matching global style
    """
}
```

**Key Elements:**
- **Species/Type**: What the character is
- **Colors**: Exact colors (use hex codes for precision)
- **Features**: Distinctive characteristics
- **Clothing**: Consistent outfit or accessories
- **Size**: Relative scale
- **Style**: Should match global STYLE_LOCK

### 3. NEGATIVE_LOCK (Artifact Prevention)

NEGATIVE_LOCK specifies what to avoid in generated images to maintain quality:

**Default NEGATIVE_LOCK:**

```
Avoid: photorealism, heavy grain, excessive bloom, text overlays,
watermarks, vignette, lens distortion, blurry focus, cluttered
backgrounds, inconsistent lighting, mixed art styles
```

**Common Anti-Patterns:**
- Photorealism (when cartoon style desired)
- Text/watermarks in image
- Film grain and noise
- Excessive post-processing effects
- Cluttered compositions
- Mixed/inconsistent styles
- Blurry or out-of-focus elements

## Custom Style Locks

### Creating Custom STYLE_LOCK

When creating custom style locks, follow this structure:

```
Aspect ratio: [dimensions or ratio]
Camera: [focal length] lens, [perspective angle]
Lighting: [type] lighting, [color temperature], [mood]
Color palette: [hex codes or color names]
Materials: [surface finishes], [texture characteristics]
Background: [environment description]
Style: [artistic approach]
Post: [final processing characteristics]
```

**Example - Cinematic Style:**

```
Aspect ratio: 1920×1080 (16:9 widescreen)
Camera: 35mm lens, low angle dramatic perspective
Lighting: dramatic rim lighting, cool key light (6500K), high contrast
Color palette: #1A1A2E, #16213E, #0F3460, #E94560, #F39C12
Materials: realistic textures, subtle film grain
Background: cinematic depth of field, environmental storytelling
Style: photorealistic with cinematic color grading
Post: anamorphic bokeh, subtle vignette, color LUT applied
```

**Example - Children's Book Style:**

```
Aspect ratio: 1024×1024 (square)
Camera: straight-on view, friendly eye-level
Lighting: bright even lighting, cheerful warm tones (3800K)
Color palette: #FF6B6B, #4ECDC4, #FFE66D, #95E1D3, #F38181
Materials: flat colors, no gradients, simple shapes
Background: simple patterns, minimal detail
Style: flat design illustration, bold outlines
Post: vibrant saturation, sharp edges, no shadows
```

**Example - Noir/Mystery Style:**

```
Aspect ratio: 1080×1350 (4:5 portrait)
Camera: 85mm lens, slightly high angle
Lighting: hard side lighting, deep shadows, 5600K
Color palette: #000000, #2C2C2C, #F5F5F5, #8B0000
Materials: high contrast, sharp shadows
Background: urban environment, selective lighting
Style: high contrast black and white with color accent
Post: film noir grade, strong vignette, grain texture
```

### Creating Custom CHARACTER_LOCK

Template for consistent character definitions:

```python
CHARACTER_LOCK = {
    "CharacterName": """
        Species/Type: [what they are]
        Colors: [primary color] with [accent colors] (hex: #XXXXXX)
        Features: [distinctive characteristics]
        Clothing: [outfit description]
        Size: [relative scale]
        Age: [appearance age]
        Expression: [default expression]
        Style: [should match global STYLE_LOCK]
    """
}
```

**Example - Multiple Characters:**

```python
CHARACTER_LOCK = {
    "Detective Hayes": """
        Species: human male detective
        Colors: dark grey suit (#2C3E50), white shirt, red tie (#E74C3C)
        Features: stern expression, square jaw, short dark hair
        Clothing: 1940s-style trench coat and fedora
        Size: tall adult male (6'2")
        Age: middle-aged (45)
        Expression: serious, focused
        Style: noir illustration with realistic proportions
    """,

    "Luna the Cat": """
        Species: black cat
        Colors: pure black (#000000) with bright yellow eyes (#FFD700)
        Features: sleek body, alert ears, long whiskers
        Clothing: red collar with bell
        Size: small housecat
        Age: young adult
        Expression: curious, intelligent
        Style: semi-realistic cartoon matching detective
    """
}
```

### Creating Custom NEGATIVE_LOCK

Tailor negative locks to your style requirements:

**For Cartoon/Illustration:**
```
Avoid: photorealism, realistic skin textures, complex lighting,
heavy shadows, lens artifacts, depth of field blur, film grain,
HDR effects, lens flare, chromatic aberration
```

**For Photorealistic:**
```
Avoid: cartoon style, flat colors, outlines, simplified shapes,
unrealistic proportions, oversaturated colors, artificial lighting,
painterly effects, illustration techniques
```

**For Minimalist:**
```
Avoid: clutter, excessive detail, complex textures, gradients,
multiple colors, busy backgrounds, ornate patterns, realistic shading,
depth effects, atmospheric perspective
```

## Multi-Turn Consistency Strategy

### Scene 0 (Establishing Shot)

First scene sets the visual foundation:

```python
prompt_0 = f"""
{STYLE_LOCK}

{CHARACTER_LOCK['MainCharacter']}

Scene: [detailed scene description]

{NEGATIVE_LOCK}
"""
```

**No reference image needed** - this is the visual anchor.

### Scenes 1-N (Subsequent Scenes)

Reference previous scene for consistency:

```python
prompt_n = f"""
REFERENCE IMAGE: Maintain the exact visual style, character appearance,
and artistic treatment from the reference image.

{STYLE_LOCK}

{CHARACTER_LOCK['MainCharacter']}

Scene: [new scene description]

IMPORTANT: Keep the same art style, color palette, and character design
as the reference image. Only change the scene composition and action.

{NEGATIVE_LOCK}
"""
```

**Include reference_images parameter:**
```python
image = model.generate_content([
    prompt_n,
    reference_images[prev_scene]
])
```

## Best Practices

### 1. Specificity Over Generality

**Bad:** "Nice lighting"
**Good:** "Soft three-point lighting with warm 4500K key light"

**Bad:** "Blue color"
**Good:** "Bright blue (#0B5FFF) with yellow accents (#FFB703)"

### 2. Consistent Terminology

Use the same descriptive terms across all scenes:
- "Semi-realistic cartoon" (not "cartoon" in one scene, "illustrated" in another)
- "Matte finish" (consistently)
- "Eye-level perspective" (always)

### 3. Hex Codes for Color Precision

Always use hex codes in color palette:
```
Color palette: #0B5FFF, #FFB703, #FB8500, #023047, #8ECAE6
```

Not:
```
Color palette: blue, orange, yellow, dark blue, light blue
```

### 4. Layer Locks Properly

Order matters in the prompt:
1. STYLE_LOCK (global visual rules)
2. CHARACTER_LOCK (character-specific details)
3. Scene description (what's happening)
4. NEGATIVE_LOCK (what to avoid)

### 5. Reference Images Every Scene

After scene 0, always include reference to previous scene:
- Prevents style drift
- Maintains character consistency
- Ensures visual coherence

### 6. Test Your Locks

Generate 2-3 test scenes to verify:
- Color palette consistency
- Character appearance stability
- Style maintenance
- Negative lock effectiveness

## Common Issues and Solutions

### Issue: Character Appearance Changes

**Problem:** Character looks different in each scene

**Solution:**
- Make CHARACTER_LOCK more specific
- Include exact color hex codes
- Describe distinctive features in detail
- Reference previous scene image
- Add character description to NEGATIVE_LOCK avoidance

**Example Fix:**
```python
CHARACTER_LOCK = {
    "Pyter": """
        Species: cartoon python snake (NOT realistic python)
        Colors: EXACTLY bright blue body (#0B5FFF) with yellow accents (#FFB703)
        Features: ALWAYS round friendly eyes, small curved smile,
                  coiled body position showing 2-3 coils
        Clothing: small red developer beanie hat on head
        Size: medium-sized snake, exactly 3 feet of body visible
        Style: semi-realistic cartoon with clear black outlines
    """
}
```

### Issue: Style Drift Across Scenes

**Problem:** Visual style changes from scene to scene

**Solution:**
- Reference previous scene image
- Repeat STYLE_LOCK in every prompt
- Be more specific about artistic treatment
- Add unwanted styles to NEGATIVE_LOCK

**Example Fix:**
```
Style: semi-realistic cartoon with clear lines and gentle shading,
       consistent with Pixar/Disney character design principles

NEGATIVE_LOCK addition:
Avoid: anime style, realistic rendering, flat vector art,
       painterly effects, watercolor, sketch style
```

### Issue: Color Palette Inconsistency

**Problem:** Colors vary between scenes

**Solution:**
- Use hex codes instead of color names
- Specify colors in both STYLE_LOCK and CHARACTER_LOCK
- Reference previous scene for color matching

**Example Fix:**
```
Color palette: PRIMARY #0B5FFF, SECONDARY #FFB703, ACCENT #FB8500,
               DARK #023047, LIGHT #8ECAE6
               Use these exact colors, no substitutions.
```

### Issue: Unwanted Artifacts

**Problem:** Text, watermarks, or visual artifacts appear

**Solution:**
- Expand NEGATIVE_LOCK with specific unwanted elements
- Mention in scene description to avoid them
- Use stronger negative prompting

**Example Fix:**
```
NEGATIVE_LOCK:
Avoid: text overlays, watermarks, signatures, logos, UI elements,
       title cards, subtitles, frame borders, copyright marks,
       QR codes, URLs, social media icons
```

### Issue: Inconsistent Lighting

**Problem:** Lighting mood changes between scenes

**Solution:**
- Specify exact lighting setup in STYLE_LOCK
- Include color temperature (Kelvin)
- Describe light direction consistently
- Reference previous scene lighting

**Example Fix:**
```
Lighting: EXACTLY three-point lighting setup with:
          - Key light: 45° angle, 4500K warm, soft diffusion
          - Fill light: opposite side, 50% intensity
          - Rim light: behind subject, subtle highlight
          Maintain this exact setup in all scenes.
```

## Advanced Techniques

### Dynamic Locks

Adjust locks mid-story for intentional changes:

```python
# Daytime scenes
STYLE_LOCK_DAY = """..., warm 4500K lighting"""

# Nighttime scenes
STYLE_LOCK_NIGHT = """..., cool 6500K moonlight"""

# Apply appropriate lock based on scene
current_lock = STYLE_LOCK_NIGHT if scene['time'] == 'night' else STYLE_LOCK_DAY
```

### Character Expression Variations

Keep appearance locked but vary expression:

```python
base_character = """
    Species: cartoon python snake
    Colors: bright blue body (#0B5FFF) with yellow accents (#FFB703)
    Features: round eyes, coiled body position
    Clothing: small developer beanie hat
"""

expressions = {
    "happy": f"{base_character}\nExpression: wide smile, bright eyes",
    "focused": f"{base_character}\nExpression: concentrated look, slight frown",
    "excited": f"{base_character}\nExpression: open mouth smile, wide eyes"
}
```

### Scene-Specific Additions

Add scene details without breaking locks:

```python
prompt = f"""
{STYLE_LOCK}
{CHARACTER_LOCK['Pyter']}

Scene: {scene_description}

Additional scene elements:
- Computer desk with monitor (matches color palette)
- Subtle code on screen (not readable text)
- Warm desk lamp (consistent with 4500K lighting)

{NEGATIVE_LOCK}
"""
```

## Example: Complete Lock System

```python
# Global visual consistency
STYLE_LOCK = """
Aspect ratio: 1080×1080 (square)
Camera: 50mm lens, eye-level perspective
Lighting: soft three-point lighting, warm key light (4500K)
Color palette: #0B5FFF, #FFB703, #FB8500, #023047, #8ECAE6
Materials: matte finish, no film grain or heavy bloom
Background: subtle gradient, clean composition
Style: semi-realistic cartoon with clear lines and gentle shading
Post: crisp focus, no vignette or text artifacts
"""

# Character consistency
CHARACTER_LOCK = {
    "Pyter": """
        Species: cartoon python snake
        Colors: bright blue body (#0B5FFF) with yellow accents (#FFB703)
        Features: round friendly eyes, small smile, coiled body showing 2-3 coils
        Clothing: small red developer beanie hat
        Size: medium-sized snake, about 3 feet visible
        Style: semi-realistic cartoon matching global style
    """,

    "Bug": """
        Species: small cartoon bug/beetle
        Colors: orange-red body (#FB8500) with dark spots (#023047)
        Features: large expressive eyes, tiny antennae, 6 legs
        Clothing: none
        Size: very small, fits on Pyter's tail
        Style: semi-realistic cartoon matching global style
    """
}

# Artifact prevention
NEGATIVE_LOCK = """
Avoid: photorealism, heavy grain, excessive bloom, text overlays,
       watermarks, vignette, lens distortion, blurry focus,
       cluttered backgrounds, inconsistent lighting, mixed art styles,
       anime style, realistic textures, flat vector art
"""

# Usage in scene generation
def generate_scene(scene_num, description, previous_image=None):
    prompt = f"""
    {STYLE_LOCK}

    {CHARACTER_LOCK['Pyter']}
    {CHARACTER_LOCK['Bug']}

    Scene: {description}

    {NEGATIVE_LOCK}
    """

    if previous_image:
        prompt = f"REFERENCE IMAGE: Maintain exact visual style.\n\n{prompt}"
        return model.generate_content([prompt, previous_image])
    else:
        return model.generate_content([prompt])
```

## Resources

- Main SKILL.md for implementation examples
- narrative-design.md for story structure
- example-stories.md for complete walkthroughs
- character-profiles.md for character template examples
