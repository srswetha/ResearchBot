from openai import OpenAI
import yaml

def formulate_context(papers):
    context = ""
    for paper in papers:
        title, abstract, url = paper[0], paper[1], paper[2]
        context = context + f"{title}. {abstract} {url}\n"
    return context

def get_answer(question, context, configFile):
    with open(configFile) as f:
        config_yaml = yaml.load(f, Loader=yaml.FullLoader)
    client = OpenAI(api_key=config_yaml['token'])
    # configFile.close()

    # Concatenate question with context
    prompt = f"Question: {question}\nContext: {context}\nAnswer:"

    messages_queryGen = [
        {"role": "system","content": "From now on I will pass in a Software Engineering question and some relevant research papers as context for the answer. I would like you to answer the question with references made to the contexts (make sure that the focus of the answer is to answer the question, not the context itself). Be sure to also include the URL after the reference to the paper in the text. Use this format to cite in-text (<a href=\"url\" target=\"_blank\">title</a>). If the question is not in the context of Software Engineering or Computer Science your reply should be: The functionality of Research Bot only extends to Computer Science and hence I am unable to answer your question."},
        {"role": "user", "content": prompt}
    ]
    # Ask the question
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages_queryGen
    )

    # Extract the answer
    answer = response.choices[0].message.content

    return answer


