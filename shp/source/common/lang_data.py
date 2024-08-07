"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
All special characters in the SHP markup and HTML data for the auto void tag
detection feature
"""

__all__ = ["LANG", "TOKEN_TYPE", "WHITESPACE", "HTML", "HTML_BUILD"]

from namespace import Namespace

LANG = Namespace.Kwargs(
    TAG=Namespace.Kwargs(
        Normal="$",
        Preform="%",
        Function="@",
        SpaceSuffix="_",
    ),
    ATTR=Namespace.Kwargs(
        Open="[",
        Close="]",
        Value="=",
    ),
    QUICKATTR=Namespace.Kwargs(
        ID="#",
        Class=".",
        FlagTrue="+",
        FlagFalse="!",
    ),
    SCOPE=Namespace.Kwargs(
        Open="{",
        Close="}",
    ),
    PATH=Namespace.Kwargs(
        ParentDir="<",
        Separator=".",
    ),
    Variable="?",
    Literal='"',
    Escape="\\",
    Comment="//",
)

# map characters to token types
TOKEN_TYPE = Namespace.Kwargs(
    Tag=LANG.TAG.Normal,
    TagPre=LANG.TAG.Preform,
    TagFunc=LANG.TAG.Function,
    AttrOpen=LANG.ATTR.Open,
    AttrClose=LANG.ATTR.Close,
    AttrValue=LANG.ATTR.Value,
    QuickID=LANG.QUICKATTR.ID,
    QuickClass=LANG.QUICKATTR.Class,
    QuickFlagTrue=LANG.QUICKATTR.FlagTrue,
    QuickFlagFalse=LANG.QUICKATTR.FlagFalse,
    ScopeOpen=LANG.SCOPE.Open,
    ScopeClose=LANG.SCOPE.Close,
    Literal=LANG.Literal,
    Variable=LANG.Variable,
)

WHITESPACE = [" ", "\r", "\n", "\t"]

HTML = Namespace.Kwargs(
    DoctypeDefault="HTML",
    Void=[
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    ],
    Preform=["pre"],
)

# not used for now
HTML_BUILD_NOT_MINIFIED = Namespace.Kwargs(
    Indent=' ' * 2,
    DoctypeClause='<!DOCTYPE {doctype}>',
    TagNameOpenStart='\n{indent}<{tag}',
    TagNameOpenEndScoped='>',
    TagNameOpenEndVoid='/>',
    TagNameClose='\n{indent}</{tag}>',
    TagAttribute=' {key}={value}',
    TagAttributeValueSep=' ',
    TagAttributeValueLiteral='"',
    Content='\n{indent}{content}',
    FilePrefix='<!-- Generated with SHP v2 -->\n',
    FileSuffix='\n'
)

# minified build ruleset, currently in use
HTML_BUILD = Namespace.Kwargs(
    Indent=" ",
    DoctypeClause="<!DOCTYPE {doctype}>",
    TagNameOpenStart="\n{indent}<{tag}",
    TagNameOpenEndScoped=">",
    TagNameOpenEndVoid="/>",
    TagNameClose="</{tag}>",
    TagAttribute=" {key}={value}",
    TagAttributeValueSep=" ",
    TagAttributeValueLiteral='"',
    Content="{content}",
    FilePrefix="<!-- Generated with SHP v2 -->\n",
    FileSuffix="\n",
)

# TODO
# Token with any escaped character is always set to Text type, this could be problematic in the future
