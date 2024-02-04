# Korean WordNet (KorLex) Graph Embedding for Improved Semantic Analysis

Welcome to our GitHub repository, dedicated to our research on enhancing semantic analysis in the Korean language through the integration of Korean WordNet (KorLex) Graph Embedding into deep neural network word embeddings.

## Abstract

The primary aim of our research is to utilize graph embedding vectors generated from the Korean lexical database, KorLex, and apply them to neural network word embedding models to encapsulate more semantic knowledge in the Korean language. Traditional word vector representations embed semantic knowledge within a corpus, but often miss the nuances captured by lexical databases such as WordNet. Our research focuses on mapping knowledge from KorLex into graph embedding vectors and then applying these vectors to improve the performance of deep neural network word embeddings. Our results demonstrate significant improvements in capturing additional semantic knowledge, indicating the efficacy of our approach for various natural language processing tasks.

## Key Contributions

1. **KorLex Graph Embedding Model**: We introduce a distance-based KorLex embedding model that transforms the structural similarities in KorLex into graph embeddings, using techniques inspired by Path2vec, whilst adapting for the unique constraints of the Korean language.

2. **Integration with Neural Word Embeddings**: We apply KorLex graph embedding vectors to deep neural network word embeddings, enhancing the semantic knowledge capture beyond traditional methods.
   
3. **Evaluation Dataset**: Development of a custom test set for similarity and analogy analysis, including POS tagging and sense number tagging with KorLex, to measure the effectiveness of our approach.

4. **Performance Improvement**: Our method demonstrates an accuracy improvement in analogy analysis, validating our hypothesis that integrating KorLex graph embeddings can significantly enhance semantic analysis capabilities.

## Methods Overview

Our approach involves two primary components: the **Graph Metric Embedding Model**, which projects lexical knowledge from KorLex into vector space, and the **Baseline Word Embedding Model**, utilizing FastText for generating 300-dimensional embeddings from news articles. The uniqueness of our method lies in merging these two models to enhance the resultant word vectors.

### Graph Metric Embedding Model

- **Model Definition**: Inspired by the Path2vec methodology, our model predicts user-defined similarities between node pairs in KorLex, aiming to capture both local and global relational semantics in vector space.
- **Training**: Utilizes negative sampling and an optimized objective that balances similarity prediction with regularization, geared towards mirroring the "gold" similarities in WordNet.
- **Related Methods**: Shares principles with Skip-gram and GloVe, but uniquely focuses on embedding lexical database graphs using custom distance metrics.

### Word Embedding Method

- **Baseline Model (FastText)**: Employs a sophisticated model capturing both word-level and sub-word-level information, making it adept at handling out-of-vocabulary words by incorporating character n-grams.
- **Vector Concatenation**: Enriches the base word embeddings by concatenating them with L2-normalized graph metric embeddings, yielding vectors that incorporate extensive semantic knowledge encoded in KorLex.

## Dataset Overview

This project utilizes several data sources and methodologies to enrich the semantic analysis capabilities of natural language processing models for Korean. Below, we provide details on the datasets used.

### 1. KorLex: Korean Wordnet

- **Description**: KorLex stands as the Korean analogue to Princeton WordNet, encompassing a broad spectrum of lexical relationships within the Korean language. It features over 130,000 synsets and 150,000 word senses across nouns, verbs, adverbs, and adjectives.
- **Construction**: Developed through a methodical translation of PWN 2.0, KorLex incorporates a hybrid approach of translation, expansion, and substitution, grounded in the Standard Korean Dictionary and refined by Korean language experts.
- **Distinctiveness**: Unlike its Princeton counterpart, KorLex accounts for the intricacies of the Korean language, housing multiple words within single synsets and allowing for words to appear across various synsets. Additionally, KorLex showcases unique path similarities, such as fully synonymous words exhibiting a similarity score of 1.0, diverging from PWN's metrics.

### 2. Training Dataset for Graph Embedding

#### 2.1 Selection Method

- **Scope**: Given the extensive nature of KorLex, we optimized our computational approach by selecting up to 200 close synonyms, hypernyms, and hyponyms for each node, resulting in a dataset comprising seventeen million word pairs, paired with Shortest Path, Leacock-Chodorow, and Wu-Palmer similarity metrics.

#### 2.2 Similarity Metrics

1. **Shortest Path Similarity (ShP)**: Inversely related to the shortest path distance in the taxonomy graph, facilitating a direct similarity measure for words within the same synset.
2. **Leacock-Chodorow Similarity (LCH)**: Derived from the shortest path between two synsets and the maximal depth in the taxonomy, offering a logarithmic scale of relational depth.
3. **Wu-Palmer Similarity (WuP)**: Focuses on the depth of synset nodes and their least common subsumer, adjusted to account for isolated nodes by assigning an average depth.

### 3. Training Dataset for Word Embedding

- **Source**: Utilizes all sections of Korea's Joongang articles spanning the last thirty years. This corpus lacked initial POS tagging and sense numbers, necessitating preprocessing to align with KorLex's structural intricacies.
- **Preprocessing**: Employed a rule-based WSD (Word Sense Disambiguation) discriminator with 99% accuracy for inferring POS tags and sense numbers, focusing on nouns, verbs, adverbs, and adjectives due to their semantic richness.
- **Composition**: The final dataset amasses three million lines, consolidating into 85 million sentences and over one billion words. This culminated in a vocabulary of 0.1 million words for the FastText model, intersecting 50 thousand common words with the graph embedding vocabulary.

## Evaluations and Results

In our study, we set out to evaluate the effectiveness of our graph embedding concatenated with word embedding model against various benchmarks. We utilized a test dataset translated and adapted from the Path2vec test dataset along with the Korean Analogy Test Set (KATS) to assess semantic and syntactic understanding facilitated by our embeddings.

### Test Dataset Overview

- **KorLex Golden Similarity**: A translation of 666 word pairs from the Path2vec dataset alongside an additional 2200 randomly selected word pairs, resulting in a comprehensive evaluation set of 2866 pairs covering three similarity metrics.
  
- **Korean Analogy (Sem 1-5)**: Semantic feature evaluation set translated from English, comprising 5000 items focused on evaluating semantic relations within the Korean language. Example: 아테네(Athens):그리스(Greece)=베이징(Beijing): 중국(China).

- **KATS (Korean Analogy Test Set)**: Based on the Bigger Analogy Test Set (BATS), focusing on semantic (S) and grammatical (G) analogies within the Korean context. Example: 남자(man):여자(woman)=형(brother):누나(sister).

### Results

#### Graph Embedding Evaluation

Our graph embedding model underwent extensive testing against the KorLex golden similarity, revealing a notably high correlation with the Shortest Path (ShP) similarity metric at 81.8%. This outcome highlights the model's ability to effectively capture semantic relations defined in KorLex.

**Table 1: Spearman Correlation between Golden Similarity and Predicted Similarity**

| Metric     | WordNet | Path2vec (Best) | KorLex | Graph Embedding |
|------------|---------|-----------------|--------|-----------------|
| LCH        | 100     | 93.5            | 100    | 51.2            |
| ShP        | 100     | 95.2            | 100    | 81.8            |
| WUP        | 100     | 93.1            | 100    | 62.7            |

Our findings indicate that while the ShP metric aligns more closely with the inherent structure of KorLex, the LCH and WUP metrics exhibit a broader disparity due to the unique hierarchical structure and multiplicity of root synsets within the KorLex graph.

#### Word Embedding Analysis

We experimented with summation and concatenation techniques to amalgamate graph and word embeddings, uncovering that concatenation notably enhances model performance on analogy tasks.

**Table 2: Analogy Analysis Accuracy (%)**

| Model       | Sem1-5 | KATS |
|-------------|--------|------|
| Base        | 11.4   | 11.6 |
| Summation   | 8.9    | 9.9  |
| Concatenate | 19.0   | 22.2 |

The concatenated model demonstrated a remarkable improvement, underscoring the efficacy of leveraging graph embeddings to bolster semantic understanding in word embeddings.

## Conclusion

Our research illustrates the substantial benefits of incorporating KorLex graph embeddings into word embeddings for the Korean language. The enhanced semantic analysis facilitated by our combined model holds significant promise for various NLP applications, including but not limited to, more accurate machine translation, sentiment analysis, and information retrieval systems tailored for the Korean language.

We invite collaborators and enthusiasts in the field of NLP to explore our methodologies, datasets, and findings further. Contributions to improve and extend our research are warmly welcomed.

For detailed inquiries or contributions, please refer to our documentation and code available in this repository, or contact the authors directly through the provided channels.

Thank you for your interest in advancing the understanding of the Korean language in the realm of computational linguistics.

## Repository Structure

```
- data/
    - korlex_embeddings/
    - evaluation_dataset/
- src/
    - graph_embedding/
    - neural_network_models/
- notebooks/
    - performance_evaluation.ipynb
- requirements.txt
- README.md
```

## Getting Started

To get started with our project, follow the steps below:

1. **Installation**: Ensure that Python 3.8 is installed on your system. Clone this repository and install the requirements using `pip install -r requirements.txt`.

2. **Data Preparation**: The `data/` directory contains the KorLex graph embeddings and evaluation datasets. Make sure to download and place them in the appropriate folders as indicated.

3. **Running the Models**: Navigate to the `src/` directory to find scripts for training the graph embedding model and integrating it with neural network word embeddings. Use the corresponding scripts to begin the training process.

4. **Evaluation**: After training, use the `notebooks/performance_evaluation.ipynb` Jupyter notebook to evaluate the models against our custom test set and compare the results with baseline models.

## Citation

If you use our work in your research, please consider citing:

```bibtex
@inproceedings{paper_id,
  title     = {Distance based Korean wordnet(KorLex) embedding model},
  author    = {SeongReol Park° Jung-Hun Lee° JoongMin Shin Sanghyun Cho},
  year      = {2023},
  booktitle = {Proceedings of the NLP Conference}
}
```
## Contribution

We welcome contributions and suggestions to improve our models and datasets. Feel free to open an issue or send a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

For any further questions or collaboration inquiries, please reach out to the authors listed in the paper.

Thank you for visiting our project!
