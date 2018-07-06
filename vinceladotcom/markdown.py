import flask
import mistune # Markdown Parsing

MARKDOWN_PARSER = mistune.Markdown()

def parse_markdown(_str):
    return flask.Markup(MARKDOWN_PARSER(_str))