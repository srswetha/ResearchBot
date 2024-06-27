import pandas as pd
import matplotlib.pyplot as plt
import spacy
from sentence_transformers import SentenceTransformer, util
import app

"""function to process the data file to get the answers 
from the ResearchBot of SE questions"""
def generate_answers_from_bot(inputFile, outputFile):
    # read data file and get question list
    data_df = pd.read_csv(inputFile)
    questions = data_df['question']
    answersFromBot = []
    index = 1
    # process the questions and get the answers
    for q in questions:
        generated_answer = app.answerQuestion('', q, "config.yaml")
        answersFromBot.append(generated_answer)
        print('Current question number: ', index, '\n')
        print(generated_answer)
        index += 1
    # store the answers into new feature column and save
    data_df['answerFromResearchBot'] = answersFromBot
    data_df.to_csv(outputFile, index=False)
    return data_df

"""
Sentence transformer (SBERT): a technique in NLP, where sentences are mapped to vectors of real numbers (numerial presentation).
Sentence embedding (BERT): SBERT has another training step on the level of sentences based on BERT.  
Those generated embedding can be compared, e.g. using cosine-similarity to find the sentences with
simialr meanings.

Applications: semantic textual similar, semantic search, parapharse minig, etc.

Package: 1. HuggingFace - sentence transformers; 2. Spacy - nlp
"""
def compare_two_answers_spacy(generated_output, expected_output):
    # Load the medium English model
    nlp = spacy.load("en_core_web_lg")

    # Process the texts
    doc1 = nlp(generated_output)
    doc2 = nlp(expected_output)

    # Compare the semantic similarity and return the values
    similarity = doc1.similarity(doc2)
    return similarity

def compare_two_answers_transformer(generated_output, expected_output):
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    # Compute embedding for both outputs
    embeddings1 = model.encode(generated_output, convert_to_tensor=True)
    embeddings2 = model.encode(expected_output, convert_to_tensor=True)
    # Compute cosine-similarities
    cosineScore = util.cos_sim(embeddings1, embeddings2)
    return cosineScore[0][0].item()

"""function to process file and compare all Q&As from StackExchange and ResearchBot"""
def compare_all_answers(inputFile, outputFile):
    # read data file and get answer lists
    data_df = pd.read_csv(inputFile)
    expected_answers = data_df['answer']
    generated_answers = data_df['answerFromResearchBot']
    sentence_similarity_spacy = []
    sentence_similarity_transformer= []
    # process the sentence similarity comparison 
    for index in range(len(expected_answers)):
        similarity1 = compare_two_answers_spacy(generated_answers[index], expected_answers[index])
        sentence_similarity_spacy.append(similarity1)

        similarity2 = compare_two_answers_transformer(generated_answers[index], expected_answers[index])
        sentence_similarity_transformer.append(similarity2)
    # store the score into new feature column and save
    data_df['similarityScoreSpacy'] = sentence_similarity_spacy
    data_df['similarityScoreSBERT'] = sentence_similarity_transformer
    data_df.to_csv(outputFile, index=False)

    return data_df

"""function to generate visualization of testing results"""
def visual(inputFile):

    # read data file and get answer lists
    data_df = pd.read_csv(inputFile)
    similarity_scores_spacy = data_df['similarityScoreSpacy']
    similarity_scores_SBERT = data_df['similarityScoreSBERT']

    # Create a histogram visualization and save the plot
    plt.figure(figsize=(10, 6))
    plt.hist(similarity_scores_spacy, bins=10, color='orange', edgecolor='maroon')
    plt.title('Distribution of Spacy (Semantic Similarity) Performance Scores')
    plt.xlabel('Similarity Score') 
    plt.ylabel('Frequency')
    plt.savefig('spacy.png')

    # Create a histogram visualization and save the plot
    plt.figure(figsize=(10, 6))
    plt.hist(similarity_scores_SBERT, bins=10, color='orange', edgecolor='maroon')
    plt.title('Distribution of SBERT (Semantic Similarity) Performance Scores')
    plt.xlabel('Similarity Score') 
    plt.ylabel('Frequency')
    plt.savefig('sbert.png')

    return 1 


"""Process the data testing here"""
# generate_answers_from_bot('./researchBot/testing.csv', 'results3.csv')
# compare_all_answers('./researchBot/module3_data_testing.csv', 'testing_performance.csv')
# visual('testing_performance.csv')