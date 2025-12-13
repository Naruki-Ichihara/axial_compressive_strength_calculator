# Core modules
from vmm.insegt.models.kmdict import KMTree, DictionaryPropagator
from vmm.insegt.models.gaussfeat import GaussFeatureExtractor, get_gauss_feat_im
import vmm.insegt.models.utils as utils

# Optional modules (may require additional dependencies)
try:
    from vmm.insegt.models.skbasic import sk_basic_segmentor
except ImportError:
    sk_basic_segmentor = None

try:
    from vmm.insegt.models.featsegt import gauss_features_segmentor
except ImportError:
    gauss_features_segmentor = None
