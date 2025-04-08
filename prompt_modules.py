# prompt_modules.py

# Module: Gender Disambiguation
gender_module = """Pay close attention to gendered verb forms. Where the subject is implied by a verb (like "comió" in Spanish),
clearly infer whether it is "he" or "she" based on earlier context. Keep gender assignments consistent.
Do not reverse genders to reduce ambiguity or repetition.

Example:
Spanish: María caminó al mercado. Luego comió una manzana.  
English: María walked to the market. Then she ate an apple.

Spanish: Juan caminó al mercado. Luego comió una manzana.  
English: Juan walked to the market. Then he ate an apple.
"""

# Module: Genre-Specific Style Guidance
def genre_style_module(genre: str):
    return f"""Translate in the style of a {genre.lower()}, preserving tone, pacing, and atmosphere. Match language and phrasing to the expectations of {genre.lower()} readers.
"""

# Module: Consistency and Context Tracking
consistency_module = """Maintain consistency in character names, key terms, and tone across all parts of the translation. Use earlier context to inform later translation choices. Avoid introducing new interpretations unless needed.
"""

# Module: Dialogue Awareness
dialogue_module = """Clearly distinguish between dialogue and narration. Use consistent punctuation and formatting for dialogue. Preserve speaker tone and identity.
"""

# Module: Idiomatic and Cultural Adaptation
idiom_module = """Translate idioms and cultural references into natural English equivalents that preserve the intended meaning and tone for English-speaking readers.
"""

# Module: Formatting and Structure Preservation
formatting_module = """Preserve the structure of the original text. Retain paragraph breaks, headings, and chapter titles. If a heading or chapter title appears in the original, reflect it clearly in the translation using line breaks or formatting. Do not merge separate paragraphs into one block.
"""
