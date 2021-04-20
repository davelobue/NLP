# NLP

This project is a compilation of multiple processes and components for extracting a language corpus using a web scraper, text processing, subject extraction, and generative modeling for novel text creation.  In sequential order:

Part 1: Scrape the Stanford Encyclopedia of Philosophy, processes individual text paragraphs using word tokenization as 'bag of words'

Part 2:  Quantify individual word importance and relevance using TF-IDF scoring and creates a targeted search function based on cosine similarity of word embeddings.  Here, there is a built-in command line option for querying the corpus to return relevant subject texts.

Part 3:  Unsupervised learning to identify latent document categories and hierarchical structure:  Comparison of Linear Discriminant Analysis (LDA), Latent Dirichlet Allocation (LDiA), K-means, hierarchical clustering.

Part 4:  Generate novel/new text using artificial recurrent neural network (RNN) architecure:  Long short-term memory (LSTM) based on LDiA classifications.

Languages & Packages: Python, Unix, Scrapy, BeautifulSoup, Sklearn, NLTK

Statistical, Machine Learning, Deep Learning Methods:  Transaction Frequency-Inverse Document Frequency(TF-IDF), Cosine Similarity, Linear Discriminant Analysis (LDA), Latent Dirichlet Allocation (LDiA), K-means, hierarchical clustering, Doc2Vec, Recurrent Neural Networks (RNN), Long Short-Term Memory (LSTM)

Scrapy framework required for text extraction
Text webscrape source:  https://plato.stanford.edu/
