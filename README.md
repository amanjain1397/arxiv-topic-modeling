# arxiv-topic-modeling
Topic Modeling on abstracts extracted from metadata obtained from arXiv e-print archive.

Used **Latent Dirichlet Allocation (LDA)** for topic modeling on the abstracts of research papers present in the arXiv e-print repository.

The project follows a linear structure as follows.

**1) Harvesting the data from arXiv e-print repository via Sickle.**
arXiv is a registered OAI-PMH data-provider and provides metadata for all submissions which is updated each night shortly after new submissions are announced. We harvest the metadata that is updated on the archive.

**2) Preprocessing the data using NLTK**

**3) Using Gensim to create required dictionaries and corpuses from the data.** 

**4) Latent Dirichlet Allocation (LDA) model (Gensim) used for topic modeling**. 

### Getting Started
- Clone this repo:
```bash
git clone https://github.com/amanjain1397/arxiv-topic-modeling.git
cd naamkaran
```
- Usage
```bash
python main.py --help
usage: main.py [-h] [--endpoint ENDPOINT] [--metadataPrefix METADATAPREFIX]
               [--harvestSet HARVESTSET] [--from_when FROM_WHEN]
               [--until_when UNTIL_WHEN] [--num_topics NUM_TOPICS]
               [--chunksize CHUNKSIZE] [--passes PASSES]
               [--visualisation VISUALISATION]

optional arguments:
  -h, --help            show this help message and exit
  --endpoint ENDPOINT   The endpoint of OAI interface (default:
                        http://export.arxiv.org/oai2)
  --metadataPrefix METADATAPREFIX
                        the prefix identifying the metadata format 
                        (default: oai_dc)
  --harvestSet HARVESTSET
                        a set for selective harvesting (default: cs)
  --from_when FROM_WHEN
                        the earliest timestamp of the records, format : yyyy/mm/dd 
                        (default: 2019-11-01)
  --until_when UNTIL_WHEN
                        the latest timestamp of the records, format: yyyy/mm/dd,
                        blank means today's date (default: '')
  --num_topics NUM_TOPICS
                        Number of topics to be found (default: 30)
  --chunksize CHUNKSIZE
  --passes PASSES
  --visualisation VISUALISATION
                        Topic visualisation using pyLDAvis (default: True)
```

### Working Example
We will harvest the metadata from 2019-11-01 to 2019-11-05 for the example using harvest_set = \'cs\'.

```bash
python main.py --from_when 2019-11-01 --until_when 2019-11-05 --harvestSet cs
```
 The pyLDAvis visualisation is exported as **./index.html**.
 
 ### More Info
Learn more about Open Archives Initiative [here](https://www.openarchives.org/). Learn about Sickle from [here](https://sickle.readthedocs.io/en/latest/).
