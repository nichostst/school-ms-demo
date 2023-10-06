# Standard Library imports

# Core Flask imports

# Third-party imports
import bleach

# App imports


def strip_xss(text):
    if not text:
        return None
    
    allowed_tags = []
    allowed_attributes = []
    allowed_styles = []

    text = bleach.clean(
        text,
        allowed_tags,
        allowed_attributes,
        allowed_styles,
        strip=True,
        strip_comments=True,
    ).strip()

    return text
