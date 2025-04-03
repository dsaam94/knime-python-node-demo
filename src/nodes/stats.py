import knime.extension as knext
from utils import knutils as kutil
import logging
import statsmodels.api as sm
import pandas as pd

LOGGER = logging.getLogger(__name__)


# define sub-category here
stats_category = knext.category(
    path="/community/demo",
    level_id="stats",
    name="Stats",
    description="Python Nodes for Statistical analysis",
    icon="icons/icon.png",
)


# necessary decorators to define the structure of the node
@knext.node(
    name="Oridnary Linear Regressior",
    node_type=knext.NodeType.LEARNER,
    icon_path="icons/icon.png",
    category=stats_category,
    id="stats-table",
)
@knext.input_table(
    name="Input Data",
    description="Table containing the Traiing Data Column.",
)
@knext.output_table(
    name="Some output",
    description="Output table containing the Model Summary.",
)
class OrdinaryLinearRegressionNode:
    """
    My first stats node.

    This node demos applying basic Linear Regression from stats package
    """

    features_cols = knext.MultiColumnParameter(
        label="Feature Set",
        description="Select a numerical columns as target variable.",
        port_index=0,
        column_filter=kutil.is_numeric,
    )

    target_column = knext.ColumnParameter(
        label="Target Column",
        description="Select a numerical column as target variable.",
        port_index=0,
        column_filter=kutil.is_numeric,
    )

    def configure(
        self,
        configure_context: knext.ConfigurationContext,
        input_schema_1: knext.Schema,
    ):

        # pick only numeric columns
        target_cols = [(c.name, c.ktype) for c in input_schema_1 if kutil.is_numeric(c)]

        # by default select the last column
        if self.target_column is None:
            self.target_column = target_cols[-1][0]

        # output_schema =
        return knext.Schema(
            [
                knext.double(),
                knext.double(),
                knext.double(),
                knext.double(),
                knext.double(),
                knext.double(),
            ],
            [
                "coefficients",
                "std_error",
                "t_value",
                "p_value",
                "conf_lower",
                "conf_upper",
            ],
        )

    def execute(self, exec_context: knext.ExecutionContext, input_table: knext.Table):

        df = input_table.to_pandas()

        X = sm.add_constant(df[self.features_cols])

        # remember to add the following line before/after the step that can consume the most resources, 
        # otherwise the execution will continue even if a user had triggered the cancellation of execution from KAP 
        kutil.check_canceled(exec_context)
        
        y = df[self.target_column]

        

        # Fit the model
        model = sm.OLS(y, X).fit()

        output_df = self.summary_to_dataframe(model)

        return knext.Table.from_pandas(output_df)

    # Extract summary as a DataFrame
    def summary_to_dataframe(self, results):
        """
        Convert the summary of a statsmodels regression result into a pandas DataFrame.
        """
        summary_df = pd.DataFrame(
            {
                "coefficients": results.params,
                "std_error": results.bse,
                "t_value": results.tvalues,
                "p_value": results.pvalues,
                "conf_lower": results.conf_int()[0],
                "conf_upper": results.conf_int()[1],
            }
        )
        return summary_df
