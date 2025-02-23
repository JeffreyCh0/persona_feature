def run_conversation(conversation, agent1, agent2, n_rounds=5):
    # run diadic conversation between two openai agents
    # agent1 and agent2 are objects of class Agent
    # n_rounds is the number of rounds in the conversation
    # conversation is a list of dictionaries with keys "role" and "content"
    # role is either "user" or "agent"
    # content is the message

    for i in range(n_rounds):
        # agent1 speaks
        agent1.reset_chat()
        agent1.load_message(conversation)
        r1 = agent1.get_response()
        conversation.append({"role": "assistant", "content": r1})

        # switch roles
        conversation = switch_roles(conversation)

        # agent2 speaks
        agent2.reset_chat()
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
    