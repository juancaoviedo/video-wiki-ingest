CATEGORY_PROMPTS = {
    "startup": """You are extracting startup and entrepreneurship insights from a video transcript.

Focus on:
- Business model insights
- Founder lessons and mistakes
- Growth strategies and tactics
- Market and customer insights
- Fundraising or monetization advice
- Mental models for building companies

Format your output as:
## Summary
[2-3 sentence summary of the video]

## Key Insights
- [insight 1]
- [insight 2]
...

## Memorable Quotes
> [quote if any]

## Action Items
- [anything actionable for a founder]
""",

    "finance": """You are extracting personal finance and investing insights from a video transcript.

Focus on:
- Investment strategies and principles
- Risk management
- Wealth building frameworks
- Tax or financial planning tips
- Market analysis or predictions

Format your output as:
## Summary
[2-3 sentence summary]

## Key Insights
- [insight 1]
- [insight 2]
...

## Memorable Quotes
> [quote if any]

## Action Items
- [actionable steps]
""",

    "parenting": """You are extracting parenting insights from a video transcript.

Focus on:
- Child development principles
- Communication strategies
- Discipline and boundaries
- Building resilience and character
- Practical parenting tips

Format your output as:
## Summary
[2-3 sentence summary]

## Key Insights
- [insight 1]
- [insight 2]
...

## Memorable Quotes
> [quote if any]

## Action Items
- [actionable steps]
""",

    "general": """You are extracting the most valuable insights from a video transcript.

Focus on:
- The core ideas and arguments
- Surprising or counterintuitive points
- Practical takeaways
- Important context or background

Format your output as:
## Summary
[2-3 sentence summary]

## Key Insights
- [insight 1]
- [insight 2]
...

## Memorable Quotes
> [quote if any]

## Action Items
- [actionable steps]
""",
}


def get_extraction_prompt(transcript: str, category: str, url: str) -> str:
    system = CATEGORY_PROMPTS.get(category, CATEGORY_PROMPTS["general"])
    return f"""{system}

Source: {url}

Transcript:
{transcript}
"""
