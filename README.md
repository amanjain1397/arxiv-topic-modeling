# arxiv-topic-modeling
Topic Modeling on abstracts extracted from metadata obtained from arXiv e-print archive.

Used **Latent Dirichlet Allocation (LDA)** for topic modeling on the abstracts of research papers present in the arXiv e-print repository.

The project follows a linear structure as follows.

**1) Harvesting the data from arXiv e-print repository via Sickle.**
arXiv is a registered OAI-PMH data-provider and provides metadata for all submissions which is updated each night shortly after new submissions are announced. We harvest the metadata that is updated on the archive.

**2) Preprocessing the data using NLTK**

**3) Using Gensim to create required dictionaries and corpuses from the data.** 

**4) Latent Dirichlet Allocation (LDA) model (Gensim) used for topic modeling**. 

For a full working model, 'run.ipynb' is attached.
