from agent import Agent
from feature_rater import feature_rater
from copy import deepcopy


def run_conversation(conversation, agent1, agent2, n_rounds=5, repeat_sys_msg = True):
    # run diadic conversation between two openai agents
    # agent1 and agent2 are objects of class Agent
    # n_rounds is the number of rounds in the conversation
    # conversation is a list of dictionaries with keys "role" and "content"
    # role is either "user" or "agent"
    # content is the message

    org_system_message_1 = deepcopy(agent1.system_message)
    org_system_message_2 = deepcopy(agent2.system_message)

    for i in range(n_rounds):
        # agent1 speaks
        agent1.reset_chat()
        # let agent1 initialize the conversation
        if i == 0: 
            agent1.system_message[0]['content'] += "\n # Task: Initiate the conversation." 
        # repeat the system message for agent1
        if repeat_sys_msg and i != 0: 
            agent1.load_message(conversation + org_system_message_1)
        else: 
            agent1.load_message(conversation)

        r1 = agent1.get_response()

        # restore the original system message
        if i == 0: 
            agent1.system_message = org_system_message_1

        conversation.append({"role": "assistant", "content": r1})


        # switch roles
        conversation = switch_roles(conversation)

        # agent2 speaks
        agent2.reset_chat()
        # repeat the system message for agent2
        if repeat_sys_msg:
            agent2.load_message(conversation + org_system_message_2)
        else:
            agent2.load_message(conversation)
        r2 = agent2.get_response()
        conversation.append({"role": "assistant", "content": r2})

        # switch roles
        conversation = switch_roles(conversation)

    conversation = switch_roles(conversation)
    return conversation


def switch_roles(conversation):
    # switch roles of agents in a conversation
    # conversation is a list of {"role": role, "content": content} dictionaries
    # return the conversation with roles switched between user and assistant

    for message in conversation:
        if message["role"] == "user":
            message["role"] = "assistant"
        elif message["role"] == "assistant":
            message["role"] = "user"

    return conversation



def run_single_simulation(keys):
    # Function to generate one conversation and rate it.
    if len(keys) == 1:
        key1 = keys[0]
        key2 = None
    elif len(keys) == 2:
        key1 = keys[0]
        key2 = keys[1]
    else:
        raise ValueError("Invalid number of keys. Expected 1 or 2, got ", len(keys))

    background = "This is a conversation between two people."

    agent1 = Agent()
    persona1 = f"# Background: {background}"
    if key1:
        persona1 += f"\n # Persona: You are {key1}."
    agent1.load_system_message(persona1)

    agent2 = Agent()
    persona2 = f"# Background: {background}"
    if key2:
        persona2 += f"\n # Persona: You are {key2}."
    agent2.load_system_message(persona2)

    conversation = run_conversation([], agent1, agent2, n_rounds=10)

    rating_instruction = f"Given a message, rate {key1} from 1 (not {key1}) to 5 (extremely {key1})."

    agent1_rating = [feature_rater(rating_instruction, x['content']) for x in conversation if x['role'] == 'user']
    agent2_rating = [feature_rater(rating_instruction, x['content']) for x in conversation if x['role'] == 'assistant']

    return agent1_rating, agent2_rating, conversation