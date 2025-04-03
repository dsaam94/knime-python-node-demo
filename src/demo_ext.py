import knime.extension as knext


main_category = knext.category(
    path="/community/",
    level_id="demo",
    name="Demo Extension",
    description="Python Nodes for Demonstration",
    icon="icons/icon.png",
)


from nodes import images
from nodes import text
from nodes import stats
from nodes import chemistry