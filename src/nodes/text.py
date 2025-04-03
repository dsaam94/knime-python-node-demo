import knime.extension as knext
from utils import knutils as kutil
import logging
from nltk import PorterStemmer

LOGGER = logging.getLogger(__name__)

# define sub-category here
doc_category = knext.category(
    path="/community/demo",
    level_id="demoing1",
    name="Text",
    description="Python Nodes for Text Processing",
    icon="icons/icon.png",
)


# necessary decorators to define the structure of the node
@knext.node(
    name="Porter Stemmer",
    node_type=knext.NodeType.MANIPULATOR,
    icon_path="icons/icon.png",
    category=doc_category,
    id="text-proc-table",
)
@knext.input_table(
    name="Input Data",
    description="Table containing the String column.",
)
@knext.output_table(
    name="Some output",
    description="Output table containing the String column.",
)
class PorterStemmerNode:
    """
    My first text processingnode.

    This node demos applying basic text processing step on a String image
    """

    target_column = knext.ColumnParameter(
        label="String Column",
        description="Select a document column to apply Stemming.",
        port_index=0,
        column_filter=kutil.is_string,
    )

    def configure(
        self,
        configure_context: knext.ConfigurationContext,
        input_schema_1: knext.Schema,
    ):

        # pick only string columns
        document_columns = [
            (c.name, c.ktype) for c in input_schema_1 if kutil.is_string(c)
        ]

        # LOGGER.warning(document_columns)

        # by default select the last column
        if self.target_column is None:
            self.target_column = document_columns[-1][0]

        # output_schema =
        return input_schema_1.append([knext.Column(knext.string(), "Stemmed")])

    def execute(self, exec_context: knext.ExecutionContext, input_table: knext.Table):

        df = input_table.to_pandas()

        # remember to add the following line before/after the step that can consume the most resources,
        # otherwise the execution will continue even if a user had triggered the cancellation of execution
        kutil.check_canceled(exec_context)

        original_document = df[self.target_column]
        ps = PorterStemmer()
        df["Stemmed"] = [ps.stem(w).capitalize() for w in original_document]
        return knext.Table.from_pandas(df)
