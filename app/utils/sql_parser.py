import re


def extract_sql(text: str) -> str:

    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL,
    )

    text = re.sub(
        r"```sql",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = text.replace("```", "")

    return text.strip()
