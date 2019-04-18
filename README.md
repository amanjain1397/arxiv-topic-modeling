# arxiv-topic-modeling
Topic Modeling on abstracts extracted from metadata obtained from arXiv e-print archive.

Used **Latent Dirichlet Allocation (LDA)** for topic modeling on the abstracts of research papers present in the arXiv e-print repository.

The project follows a linear structure as follows.

**1) Harvesting the data from arXiv e-print repository via Sickle**
arXiv is a registered OAI-PMH data-provider and provides metadata for all submissions which is updated each night shortly after new submissions are announced. Also harvests the new metadata that is updated on the archive.

**2) Preprocessing the data using NLTK**

**3) Using Gensim to create required dictionaries and corpuses from the data.** 
This dictionary and corpus can be updated when new metadata is harvested from the e-print archive.

**4) Latent Dirichlet Allocation (LDA) model (Gensim) used for topic modeling**. 
The model is retrained every time new doucments are harvested from the archive.

For a full working model, 'run.ipynb' is attached.
