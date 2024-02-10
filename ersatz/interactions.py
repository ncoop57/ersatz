# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_interactions.ipynb.

# %% auto 0
__all__ = ['BasicSeeder', 'EvolSeeder', 'GenerateQuestionOrInstruction', 'GenerateAnswer', 'Rephrase',
           'RephraseQAorInstructResponse', 'Conversation', 'BasicAgent', 'AlphaAgent']

# %% ../nbs/02_interactions.ipynb 3
import dspy

# %% ../nbs/02_interactions.ipynb 5
class BasicSeeder(dspy.Module):
    pass

# %% ../nbs/02_interactions.ipynb 6
class EvolSeeder(dspy.Module):
    pass

# %% ../nbs/02_interactions.ipynb 7
class GenerateQuestionOrInstruction(dspy.Signature):
    """Given a topic and a history of a conversation, generate a question or instruction for the next turn as a user."""

    topic = dspy.InputField(desc="The topic of the conversation.")
    history = dspy.InputField(desc="The history of the conversation. It can be empty.")
    question_or_instruction = dspy.OutputField(
        desc="The question or instruction for the next turn as a user. End with ---."
    )


class GenerateAnswer(dspy.Signature):
    """Given a topic and a history of a conversation, generate an answer for the next turn as an Assistant"""

    topic = dspy.InputField(desc="The topic of the conversation.")
    history = dspy.InputField(
        desc="The history of the conversation with the last turn being the user's question or instruction."
    )
    answer = dspy.OutputField(
        desc="The answer for the next turn as an Assistant. End with ---."
    )


class Rephrase(dspy.Signature):
    """Given a document and a way of rephrasing the document, generate a new document by rephrasing the original document."""

    original_doc = dspy.InputField(desc="The original document.")
    rephrase_like = dspy.InputField(desc="The way of rephrasing the document.")
    rephrased_doc = dspy.OutputField(
        desc="The rephrased document. It contains all the same information as the original document, just expressed in a different way."
    )


class RephraseQAorInstructResponse(dspy.Signature):
    """Given a question and answer or instruction and response and a way of rephrasing them, generate a new question and answer or instruction and response by rephrasing the original ones."""

    original_q_or_instruct = dspy.InputField(
        desc="The original question or instruction."
    )
    original_a_or_response = dspy.InputField(desc="The original answer or response.")
    rephrase_like = dspy.InputField(desc="The way of rephrasing the document.")
    # rephrased_q_or_instruct = dspy.OutputField(desc="The rephrased uesr question or instruction.")
    rephrased_a_or_response = dspy.OutputField(
        desc="The rephrased Assistant answer or response."
    )

# %% ../nbs/02_interactions.ipynb 8
class Conversation(dspy.Module):
    def __init__(self, tools=[]):
        super().__init__()
        self.tools = tools
        self.conversation_starter = dspy.Predict(GenerateQuestionOrInstruction)
        self.answer_generator = dspy.Predict(GenerateAnswer)
        self.follow_upper = dspy.Predict(GenerateQuestionOrInstruction)
        if len(self.tools) > 0:
            self.tool_usage = dspy.ChainOfThought(
                "topic, conversation_history, tools -> tool_usage", n=5
            )

    def forward(self, topic, num_turns=1):
        initial = self.conversation_starter(topic=topic, history="Empty")
        history = [initial.question_or_instruction]
        for i in range(num_turns):
            answer = self.answer_generator(topic=topic, history="\n\n".join(history))
            history.append(answer.answer)
            if i < num_turns - 1:
                follow_up = self.follow_upper(topic=topic, history="\n\n".join(history))
                history.append(follow_up.question_or_instruction)

        return history

# %% ../nbs/02_interactions.ipynb 12
class BasicAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.intent_generator = dspy.Predict("observation, topic -> intent")
        self.plan_generator = dspy.Predict(GenerateAnswer)
        self.action_generator = dspy.Predict(GenerateQuestionOrInstruction)

    def forward(self):
        pass

# %% ../nbs/02_interactions.ipynb 13
class AlphaAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.intent_generator = dspy.Predict("observation, topic -> intent")
        self.analysis_generator = dspy.Predict("observation, intent -> analysis")
        self.solution_generator = dspy.Predict(
            "observation, intent, analysis -> solution"
        )
        self.solution_ranker = dspy.Predict(
            "observation, intent, solutions -> ranked_solutions"
        )
        self.action_generator = dspy.Predict(
            "observation, analysis, ranked_solutions, action_history -> action"
        )

    def forward(self, observation, topic=None, action_history=None, num_solutions=None):
        pass
