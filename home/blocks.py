from django.utils.html import escape
from wagtail import blocks


class StatBlock(blocks.StructBlock):
    stat = blocks.CharBlock(
        help_text="The big statistic.",
        label="Statistic"
    )
    desc = blocks.CharBlock(
        label="Short Description",
        help_text=escape("The description underneath the big statistic. You may use these tags in this field: "
                         "<a>, <b>, <br>, <i>, <em>, <strong>, <sup>, <sub>")
    )


class StatsBlock(blocks.StructBlock):
    """
    This is the visible "Stats" block - an optional title + a strip of individual StatBlocks
    """

    STYLES = [
        ('h2', 'Heading 2'),
        ('h3', 'Heading 3'),
        ('h4', 'Heading 4'),
        ('h5', 'Heading 5'),
        ('h6', 'Heading 6 (all uppercase)'),
    ]

    title = blocks.CharBlock(
        required=False
    )
    title_style = blocks.ChoiceBlock(
        choices=STYLES,
        requried=True,
        default='h3'
    )
    title_centered = blocks.BooleanBlock(
        verbose_name='Center title',
        required=False,
        default=False,
        help_text='Check this box to center the title. Otherwise, it will be left-aligned.'
    )
    stats = blocks.ListBlock(
        StatBlock(),
        label="Statistics"
    )

    class Meta:
        template = 'home/blocks/stats-block.html'
        form_classname = 'stats-block struct-block'
        label = 'Stats'
        icon = 'fa-bar-chart'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        if len(value['stats']) < 4:
            # Add a class that tells the CSS to not bother with a carousel on devices larger than phones if there are
            # less than 4 images.
            context['extra_classes'] = 'short'
        return context
