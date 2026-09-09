scitex_scholar.citation_graph
=============================

Citation data is served by a running ``crossref-local`` HTTP API; this module
does not open crossref-local's data files itself. The endpoint is resolved
from the ``SCITEX_SCHOLAR_CROSSREF_API_URL`` environment variable (or the
Django setting of the same name in a host project), and when nothing is set
``CitationGraphBuilder`` falls back to crossref-local's own default endpoint.

.. automodule:: scitex_scholar.citation_graph
   :members:
   :undoc-members:
   :show-inheritance:
