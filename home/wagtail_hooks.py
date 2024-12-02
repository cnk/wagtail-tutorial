from wagtail.admin.rich_text.converters.editor_html import WhitelistRule
from wagtail.core import hooks
from wagtail.whitelist import allow_without_attributes
from wagtail_hallo.plugins import HalloPlugin


###################
# Hallo.js Plugins
###################
@hooks.register('register_rich_text_features')
def register_hallo_plugins(features):
    features.register_editor_plugin(
        'hallo',
        'edithtml-hallo',
        HalloPlugin(
            name='edithtml',
            js=['js/hallo-edit-html.js'],
        )
    )
    features.default_features.append('edithtml-hallo')

    features.register_editor_plugin(
        'hallo',
        'subscript-hallo',
        HalloPlugin(
            name='subscript',
            js=['js/hallo-sub-script.js']
        )
    )
    features.default_features.append('subscript-hallo')

    features.register_converter_rule('editorhtml', 'subscript-hallo', [
        WhitelistRule('sub', allow_without_attributes),
    ])

    features.register_editor_plugin(
        'hallo',
        'superscript-hallo',
        HalloPlugin(
            name='superscript',
            js=['js/hallo-super-script.js']
        )
    )
    features.default_features.append('superscript-hallo')

    features.register_converter_rule('editorhtml', 'superscript-hallo', [
        WhitelistRule('sup', allow_without_attributes),
    ])


@hooks.register('register_rich_text_features', order=9999)
def whitelister_allow_tables(features):
    """
    Removes most of Wagtail's overly restrictive HTML filtering.

    DEV NOTE: We use order=9999 in the hook registration because of how features.register_converter_rule() works.
    It replaces any existing instance of a rule with the most recently registered instance. This means that the last
    hook which calls features.register_converter_rule('editorhtml', 'link', ...) "wins".
    """
    safe_tags = [
        "table", "tbody", "td", "tfoot", "th", "thead", "tr",
    ]

    for safe_tag in safe_tags:
        features.register_converter_rule('editorhtml', safe_tag, [WhitelistRule(safe_tag, allow_without_attributes)])
