# Korean WordNet (KorLex) Graph Embedding for Improved Semantic Analysis

Welcome to our GitHub repository, dedicated to our research on enhancing semantic analysis in the Korean language through the integration of Korean WordNet (KorLex) Graph Embedding into deep neural network word embeddings.

## Abstract

The primary aim of our research is to utilize graph embedding vectors generated from the Korean lexical database, KorLex, and apply them to neural network word embedding models to encapsulate more semantic knowledge in the Korean language. Traditional word vector representations embed semantic knowledge within a corpus, but often miss the nuances captured by lexical databases such as WordNet. Our research focuses on mapping knowledge from KorLex into graph embedding vectors and then applying these vectors to improve the performance of deep neural network word embeddings. Our results demonstrate significant improvements in capturing additional semantic knowledge, indicating the efficacy of our approach for various natural language processing tasks.

## Key Contributions

1. **KorLex Graph Embedding Model**: We introduce a distance-based KorLex embedding model that transforms the structural similarities in KorLex into graph embeddings, using techniques inspired by Path2vec, whilst adapting for the unique constraints of the Korean language.

2. **Integration with Neural Word Embeddings**: We apply KorLex graph embedding vectors to deep neural network word embeddings, enhancing the semantic knowledge capture beyond traditional methods.
   
3. **Evaluation Dataset**: Development of a custom test set for similarity and analogy analysis, including POS tagging and sense number tagging with KorLex, to measure the effectiveness of our approach.

4. **Performance Improvement**: Our method demonstrates an accuracy improvement in analogy analysis, validating our hypothesis that integrating KorLex graph embeddings can significantly enhance semantic analysis capabilities.

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

1. **Installation**: Ensure that Python 3.x is installed on your system. Clone this repository and install the requirements using `pip install -r requirements.txt`.

2. **Data Preparation**: The `data/` directory contains the KorLex graph embeddings and evaluation datasets. Make sure to download and place them in the appropriate folders as indicated.

3. **Running the Models**: Navigate to the `src/` directory to find scripts for training the graph embedding model and integrating it with neural network word embeddings. Use the corresponding scripts to begin the training process.

4. **Evaluation**: After training, use the `notebooks/performance_evaluation.ipynb` Jupyter notebook to evaluate the models against our custom test set and compare the results with baseline models.

## Citation

If you use our work in your research, please consider citing:

```bibtex
@inproceedings{your_paper_id,
  title     = {Enhancing Semantic Analysis in Korean Language Using KorLex Graph Embeddings},
  author    = {Your Name and Collaborator's Name},
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
