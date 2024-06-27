from openai import OpenAI
import yaml


def generateQuery(configFile, userInput):
    with open(configFile) as f:
        config_yaml = yaml.load(f, Loader=yaml.FullLoader)
    client = OpenAI(api_key=config_yaml['token'])
    # configFile.close()
    messages_queryGen = [
        {"role": "system" , "content": "From now on I will pass in a prompt like \"How do I perform document similarity using NLP\" and I would like you to curate an output that looks similar to this \"nlp+natural+language+processing+document+similarity\". This is what a search query would look like for the given prompt. It uses '+'  which separates all the key words"},
        {"role": "user" , "content": userInput}
    ]
    ans = client.chat.completions.create(
        model="gpt-4",
        messages=messages_queryGen)
    return ans.choices[0].message.content

















