import ast
import openai
import json
import PyPDF2

# Input your OpenAI API key:
openai.api_key = "API KEY"

# Define the model you want to use: https://platform.openai.com/docs/models
# It is a good practice to test with a specific version of LLM.
llm_model = "gpt-4o-2024-08-06"  # or gpt-3.5-turbo

# We are using OpenAI chat.completion: https://platform.openai.com/docs/guides/text-generation
def generate_response(_prompts):
    
    chat_completion = openai.chat.completions.create(
        model=llm_model,
        messages=_prompts,
    )

    for i in _prompts:
        print(i["content"])
    output = chat_completion.choices[0].message.content
    print(f"\n{llm_model}: {output}\n")
    
    return output

# Memory
memory_stream = {
    "reading_behavior": [],
    "user_interest": [],
    "suggestions": [],
    "intervention": [],
    "action": []
}

reading_stream = {
    "reading_behavior": [],
    "read_sentences": [],
    "reflections": [],
    "suggestions_followed": [],
    "achieved_from_suggestion": []
}

def update_memory_stream(_keys=list, _values=list):
    for key, value in zip(_keys, _values):
        if key in memory_stream:
            memory_stream[key].append(value)

# Retrieve
def retrieve_memory(_length):
    # Get N number of latest memory  
    retrieved_memory = {key: value[-_length:] for key, value in memory_stream.items()}
    return retrieved_memory

# Infer the user's interest from the observed user behaviors and what they were interested in before.
def infer_user_interest(_reading_behavior, _user_interest):
    prompts = [
        {
            "role": "system",
            "content": "You are a reading assistant designed to guess a user's interests based on their reading behaviors and their previous interest.\n"
        },
        {
            "role": "user",
            "content": "### User's reading behavior ###\n"
                       f"{_reading_behavior}\n"
                       "### User's previous interest ###\n"
                       f"{_user_interest}\n"
                       "What do you think the user is interested in now?\n"
                       "Show only the result in the following format:\n"
                       "\"The user is interested in ...\""
        }
    ]
    output = generate_response(prompts)
    return output

# Generate what kinds of research topics would be interesting to the user based on their interests and what the agent has suggesetd before.
def generate_suggestion(_user_interest, _previous_suggestions):
    prompts = [
        {
            "role": "system",
            "content": "You are a proactive reading assistant designed to suggest a research topic to a user based on their interesets and what you suggested before.\n"
        },
        {
            "role": "user",
            "content": "### User's interest ###\n"
                       f"{_user_interest}\n"
                       "### Previous suggestions to the user ###\n"
                       f"{_previous_suggestions}\n"
                       "What other new or advanced research topic would you suggest?\n"
                       "Show only the result in the following format:\n"
                       "\"I should suggest ...\""
        }
    ]
    output = generate_response(prompts)
    return output

# Judge whether this is a good timing to intervene the user and make suggestions based on the user's reading behaviors.
def decide_intervention(_reading_behavior):
    prompts = [
        {
            "role": "system",
            "content": "You are a proactive reading assistant designed to suggest a research topic to a user.\n"
                       "Your task is to observe user's reading behaviors and determine whether it is okay to interven or not.\n"
        },
        {
            "role": "user",
            "content": "### User's reading behavior ###\n"
                       f"{_reading_behavior}\n"
                       "Is it a good moment to intervene?\n"
                       "If you may intervene, reply \"Intervene\".\n"
                       "If you should NOT intervene, reply \"Wait\"."
        }
    ]
    output = generate_response(prompts)
    return output

# Based on the infered user interest and potential suggestions, the agent make suggestions to the user. 
def action(_intervene, _llm_user_interest, _llm_suggestion):
    if "Intervene" in _intervene:
        prompts = [
            {
                "role": "system",
                "content": "You are a proactive chatbot designed to suggest a research topic to a user.\n"
            },
            {
                "role": "user",
                "content": "Here is your observation:\n"
                           f"{_llm_user_interest}\n"
                           f"{_llm_suggestion}\n"
                           "Based on your observation what would you say to the user?\n"
            }
        ]
        output = generate_response(prompts)
    else:
        output = "(no action)"
    return output



# STUDENT CODE: read PDF by sentence.
def read_pdf_by_sentence(pdf_path):
    # Returns a list of sentences from the PDF
    with open(pdf_path, "rb") as file:
        pdf = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    sentences = text.split(". ")
    sentences = [sentence for sentence in sentences if sentence.strip() != ""]
    sentences.append("!$& END OF DOCUMENT !$&")
    return sentences

# STUDENT CODE: Set the knowledge goal
def set_knowledge_goal(path, title):
    # From the PDF title, the agent generates a goal to learn about the topic. This will be compared against to decide whether the agent has enough knowledge.
    prompt = f'A generative agent is set to start reading the file "{path}". Knowing this and the title "{title}", set a comprehensive list of goals (between 3 and 5) for their learning; which are attainable only by reading the document. Make them easy goals. Return only these goals.'
    prompts = [
        {
            "role": "system",
            "content": "You are an expert educator; with in-depth knowledge of how people and generative agents learn. Thus, you know perfectly well how to set goals for the different stages of learning at any level."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]   
    goal = generate_response(prompts)
    return goal

# STUDENT CODE: Enough knowledge?
def check_enough_knowledge(goals):
    prompts = [
        {
            "role": "system",
            "content": "You are an expert evaluator; with the ability to assess the knowledge of a generative agent based on the goals set for their learning."
        },
        {
            "role": "user",
            "content": f'So far, the agent you are evaluating has read the following sentences: {reading_stream["read_sentences"]} \n and reflected on the knowledge like this: {reading_stream["reflections"]}\n'
            f'Also, the agent has achieved the following from past suggestions: {reading_stream["achieved_from_suggestion"]}\n'
            f'The agent has the following learning goals:\n {goals} \n.'
            f'Given all of this, has the agent, through reading, reflections, and suggested actions, achieved their learning goals? Be sufficiently strict: ALL the goals must be achieved to return YES.'
            f'Return only a YES/NO response.'
        }
    ]
    answer = generate_response(prompts)
    answer = answer.lower().strip()
    if "yes" in answer:
        enough_knowledge = True
    else:
        enough_knowledge = False
    return enough_knowledge

# STUDENT CODE: Potential Agent action - Read the next sentence
def read_next_sentence(sentence_count, current_sentence):
    if current_sentence == "!$& END OF DOCUMENT !$&" or sentence_count >= len(sentences):
        action = "The reading agent has reached the end of the document."
    else:
        reading_stream["read_sentences"].append(current_sentence)
        action =  f"The reading agent reads the '{sentence_count}' sentence: {current_sentence}."
    return action

# STUDENT CODE: Potential Agent action - Reflect
def read_reflect(goals):
    prompts = [
        {
            "role": "system",
            "content": "You are an autonomous generative agent designed to learn from a document you are reading."
        },
        {
            "role": "user",
            "content": f"So far, you've read the following sentences: {reading_stream['read_sentences']}\n"
                       f"You've previously reflected on the knowledge: {reading_stream['reflections']}\n"
                       f"Also, you've previously achieved the following from past suggestions by a reading assistant: {reading_stream['achieved_from_suggestion']}\n"
                       f"The agent's goals are: {goals}\n"
                       "Briefly reflect on all this information. Interiorize it, debate it, think about your goals, etc. Return only this reflection."
        }
    ]
    reflections = generate_response(prompts)
    action = f"The reading agent reflects on the information: {reflections}"
    reading_stream["reflections"].append(reflections)

    # Check goals
    goal_check = check_enough_knowledge(goals)

    return action, goal_check

# STUDENT CODE: Potential Agent action - Follow suggestion
def follow_suggestion(suggestion):
    prompts = [
        {
            "role": "system",
            "content": "You are an autonomous generative agent designed to learn from a document you are reading. To aid in your task, there is also a reading assistant that will, from time to time, suggest actions; though it is up to you to decide whether to follow them or not."
        },
        {
            "role": "user",
            "content": f"So far, you've read the following sentences: {reading_stream['read_sentences']}\n"
                       f"You've previously reflected on the knowledge: {reading_stream['reflections']}\n"
                       f"Also, you've previously achieved the following from past suggestions: {reading_stream['achieved_from_suggestion']}\n"
                       f"The reading assistant has suggested: {suggestion}\n"
                       f"And you have decided to follow it. What actions do you do to follow the suggestion? What do you achieve and/or learn from it? Answer with the following format: The reading agent follows the suggestion given, ..."
        }
    ]
    action = generate_response(prompts)
    reading_stream["suggestions_followed"].append(suggestion)
    reading_stream["achieved_from_suggestion"].append(action)
    return action

# STUDENT CODE: Defining user behaviour
def user_behavior(previous_prompts, goals, sentence_count, sentences, suggestion):
    goal_check = False
    if len(previous_prompts) == 0:
        prompts = [
        {
            "role": "system",
            "content": """You are an autonomous generative agent designed to learn from a document you are reading.
            To aid in your task, there is also a reading assistant that will, from time to time, suggest actions; though it is up to you to decide whether to follow them or not.
            Your main goal is to learn about the topic and fulfill the goals set for you.
            Each time you are interacted with, you have four options: \n
            1. Read the next sentence: return READ \n
            2. Reflect on the information: return REFLECT (note that Reflection should be triggered when enough new information guarrants it, and not every other read sentence. This is an active and in-depth reflection action.)\n
            3. Follow the suggestion: return FOLLOW (careful: if you only follow suggestions, you will never finish reading the original source!) \n
            4. Do something else: return your behaviour \n"""
        },
        {
            "role": "user",
            "content": f""" You just started your new assignment. Your goals for the current doucment are: \n {goals}.
            Remember: Each time you are interacted with, you have four options: \n
            1. Read the next sentence: return READ \n
            2. Reflect on the information: return REFLECT \n
            3. Follow the suggestion: return FOLLOW \n
            4. Do something else: return your behaviour \n
            What would you like to do now?
            """
        }
        ]
    else:
        previous_prompts[-1]["content"] += f"""\n The reading assistent has suggested: {suggestion} \n.
        Remeber your learning goals: {goals} \n
        What would you like to do now? (READ, REFLECT, FOLLOW, or your own behavior)"""
        prompts = previous_prompts

    decision = generate_response(prompts)
    reading_stream["reading_behavior"].append(decision)

    prompts.append(
        {
            "role": "assistant",
            "content": decision
        })

    if "READ" == decision:
        current_sentence = sentences[sentence_count]
        sentence_count += 1
        behavior = read_next_sentence(sentence_count, current_sentence)

    elif "REFLECT" == decision:
        behavior, goal_check = read_reflect(goals)

    elif "FOLLOW" == decision:
        behavior = follow_suggestion(suggestion)

    else:
        behavior = decision

    prompts.append(
        {
            "role": "user",
            "content": behavior
        }
    )
    return prompts, behavior, sentence_count, goal_check

# Main loop
if __name__ == "__main__":
    enough_kowledge = False
    
    # Pre-process PDF
    pdf_path = "Assingment 1a - CompInetraction and Design - Combinatiorial Optimization.pdf"
    #pdf_path = "Cyborg Manifesto - Donna Haraway.pdf"
    sentences = read_pdf_by_sentence(pdf_path)
    # Clean-up sentences: no blank sentences, no special sentences
    if pdf_path == "Cyborg Manifesto - Donna Haraway.pdf":
        for sentence in sentences:
            sentence_clean = sentence.lower().strip()
            if sentence_clean == "" or "university of minnesota" in sentence_clean or "proquest" == sentence_clean or 'proquest ebook central,         http://ebookcentral' == sentence_clean  or 'com/lib/warw/detail' == sentence_clean or 'action?docID=4392065' == sentence or "created from warw" in sentence_clean or "2016" in sentence_clean or 'all rights reserved' in sentence_clean:
                sentences.remove(sentence)

    print(f"Readied-up {len(sentences)} sentences from the PDF: {pdf_path}.")
    print("")
    
    # Set the knowledge goal
    print("------- Knowledge Goals ------")
    goals = set_knowledge_goal(pdf_path, sentences[0])
    print("--- End of Knowledge Goals ---")
    print("")

    # Start the main loop
    sentence_count = 0
    sentence = sentences[sentence_count]
    new_action = None
    reader_memeory = []
    while not enough_kowledge:
        
        # input("----------------------\nPress enter to input the next reader-assistant step.\n----------------------")
        print("--------------------------------------------------")

        ## READING BEHAVIOR
        reader_memeory, behavior, sentence_count, enough_kowledge = user_behavior(reader_memeory, goals, sentence_count, sentences, new_action)

        ## ASSISTANT BEHAVIOR
        # 1. Perceive
        reading_behavior = behavior

        # 2. Memory stream
        update_memory_stream(["reading_behavior"], [reading_behavior])

        # 3. Retrieve
        retrieved_memory = retrieve_memory(3)

        # 4. Retrieved memories
        reading_behavior = retrieved_memory["reading_behavior"]
        previous_user_interest = retrieved_memory["user_interest"]
        previous_suggestion = retrieved_memory["suggestions"]
        previous_intervension = retrieved_memory["intervention"]
        previous_action = retrieved_memory["action"]

        # 5. Reflect
        new_user_interest = infer_user_interest(reading_behavior, previous_user_interest)
        new_suggestion = generate_suggestion(new_user_interest, previous_suggestion)
        new_intervention = decide_intervention(reading_behavior)

        # 6. Action
        new_action = action(new_intervention, new_user_interest, new_suggestion) 

        # Update the memory stream for the next round
        update_memory_stream(
            ["user_interest", "suggestions", "intervention", "action"],
            [new_user_interest, new_suggestion, new_intervention, new_action]
        )
        
        # Store the updated memory for you to review
        with open("memory_stream.json", "w") as json_file:
            json.dump(memory_stream, json_file)
        with open("reading_stream.json", "w") as json_file:
            json.dump(reading_stream, json_file)
        

