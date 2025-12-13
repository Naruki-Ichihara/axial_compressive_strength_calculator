# InSegt - Interactive Segmentation
# Core modules (no GUI dependencies)
import vmm.insegt.models.utils as utils
from vmm.insegt.models.kmdict import KMTree, DictionaryPropagator
from vmm.insegt.models.gaussfeat import GaussFeatureExtractor

# GUI modules are NOT imported here to avoid QPixmap issues
# Import them directly when needed:
#   from vmm.insegt.annotators.insegtannotator import insegt, InSegtAnnotator
