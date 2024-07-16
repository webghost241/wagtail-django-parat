from parat.core.blocks import ContentFieldFactory
from parat.core.models.wagtail import AbstractStandardPage

from parat.core.blocks.parat_blocks import DynamicChildrenCardsBlock


class CompanyIndexPage(AbstractStandardPage):
    body = (
        ContentFieldFactory()
        .set_extra_blocks(
            [("dynamic_children_cards_block", DynamicChildrenCardsBlock())]
        )
        .get_general_body()
    )

    max_count = 1
    template = "company/company_index_page.html"
