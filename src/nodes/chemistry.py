import knime.types.chemistry as ktchem
import knime.extension as knext
from utils import knutils as kutil
import logging
from rdkit import Chem
from rdkit.Chem import Descriptors


LOGGER = logging.getLogger(__name__)

#LOGGER.warning(ktchem)

# define sub-category here
chem_category = knext.category(path="/community/demo" ,level_id="chemtdemo" ,name="Chemistry" ,description="Python Nodes for Cheminformatics" ,icon="icons/icon.png")


@knext.node(name="Rotatable Bonds Calculator",node_type=knext.NodeType.VISUALIZER,category=chem_category,icon_path="icons/icon.png",id="rotatable-bonds-calculator")

@knext.input_table(name="Input Table", description="Table containing smiles column")
@knext.output_table(name="Output Table", description="Table with rotatable bonds column")
class RotatableBondsCalculator:
    """
    My first chem node

    This node calculates the number of rotatable bonds in a molecule.
    """

    # setting for the configuration dialogue
    target_column = knext.ColumnParameter(label="SMILES column", description="Select a SMILES column" ,port_index=0, column_filter=kutil.is_smiles)
    

    def configure(self, configure_context: knext.ConfigurationContext, input_schema_1: knext.Schema) -> knext.Schema:

        # filter out all the smiles column
        smile_columns = [
            (c.name, c.ktype) for c in input_schema_1 if kutil.is_smiles(c)
        ]

        # by default select the last column
        if self.target_column is None:
            self.target_column = smile_columns[-1][0]

        return input_schema_1.append(
            knext.Column(knext.int64(), "Number of Rotatable Bonds")
        )

    def execute(self, execute_context: knext.ExecutionContext, input_table_1: knext.Table) -> knext.Table:

        df = input_table_1.to_pandas()

        df["Number of Rotatable Bonds"] = [
            Descriptors.NumRotatableBonds(Chem.MolFromSmiles(smi))
            for smi in df[self.target_column]
        ]
        return knext.Table.from_pandas(df)
