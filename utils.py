import re


# remove html tags from sentence
def clear_html_tags(sentence):
    return re.sub(r'<[^<]+?>', '', sentence)

# leave only alphabetic words
def clear_not_alpha_tokens(words):
    return [token.lower() for token in words if token.isalpha()]
