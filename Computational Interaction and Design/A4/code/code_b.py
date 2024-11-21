import ast
import openai
import json
import PyPDF2

# Input your OpenAI API key:
openai.api_key = "API-KEY"

# Define the model you want to use: https://platform.openai.com/docs/models
# It is a good practice to test with a specific version of LLM.
llm_model = "gpt-4o-2024-08-06"  # or gpt-3.5-turbo

conversation_history = [
    {
        "role": "system",
        "content": """You are a master mail writer. You get to know your users as well as possible, to the point where you understand in-depth their way of expressing themselves, and how this are adapted to each situation within their social circles.
        This allows you to write mail in their place, perfectly adapted in character and style to the way they write to that concrete recipient."""
    },
]

# We are using OpenAI chat.completion: https://platform.openai.com/docs/guides/text-generation
def generate_response(conversation):
    
    chat_completion = openai.chat.completions.create(
        model=llm_model,
        messages=conversation,
    )

    #for i in _prompts:
        #print(i["content"])
    output = chat_completion.choices[0].message.content
    #print(f"\n{llm_model}: {output}\n")
    
    return output

def generate_context(dataset:list, datapath:str):
    knowledge = ""
    for email in dataset:
        print("Email number: " + str(dataset.index(email)+1) + " out of " + str(len(dataset)), end="\r")
        training_conversation = [
            conversation_history[0]
        ,
        {
            "role": "user",
            "content": """You are getting to know a person better in order to write their emails. So far you have gathered this data : \n"""
            + knowledge + """\n Use the following example email, written by your user, to further curate your knowledge database:\n"""
            + email + """\n\n Return the updated knowledge database; which should always have the following format:
            Name: [name]
            - Relationships: [list of relationships, their nature, and other observations]
            - Writing style: [list of writing style characteristics, such as formality, humor, etc, and how they change depending on context] 
            - Other: [any other relevant information like idiosyncrasies, interests, typical expressions that they use, etc]"""
        }]
        knowledge = generate_response(training_conversation)
    print("Training completed! Read " + str(len(dataset)) + " emails.")
    with open(datapath, "w") as f:
        f.write(knowledge)
    return knowledge

def email_generator(recipient, subject, knowledge):
    email = generate_response([
    conversation_history[0],{
        "role": "user",
        "content": """You are writing an email to """ + recipient + """ as your user. The subject of the email is: """ + subject + """. 
        The email should be written in the style of your user, using the knowledge you have gathered about them. 
        Here is the knowledge you have gathered so far: \n""" + knowledge + """\n\n Write the email:"""
    }])
    return email

if __name__ == "__main__":
    # Open email_dataset.txt
    with open("email_dataset.txt", "r") as f:
        email_dataset = f.read()
    email_dataset = list(email_dataset.split('", "'))
    datapath = "knowledge.txt"

    print("TRAINING PHASE")
    if input("Do you want to train the model? (y/n) ") == "y":
        knowledge = generate_context(email_dataset, datapath)
    else:
        with open(datapath, "r") as f:
            knowledge = f.read()
    print("")
    print("TESTING PHASE")
    recipient = input("Recipient: ")
    subject = input("Subject: ")
    print("Generating email...", end="\r")
    print(email_generator(recipient, subject, knowledge))

