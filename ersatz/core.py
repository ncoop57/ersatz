# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_interactions.ipynb.

# %% auto 0
__all__ = ['Conversation']

# %% ../nbs/02_interactions.ipynb 3
import dspy

# %% ../nbs/02_interactions.ipynb 4
class Conversation(dspy.Module):
    def __init__(self):
        super().__init__()
        self.conversation_starter = dspy.Predict('topic -> initial_question_or_instruction')
        self.answer_generator = dspy.Predict('topic, conversation_history -> answer')
        self.follow_upper = dspy.Predict('topic, conversation_history -> follow_up_question_or_instruction')

    def forward(self, topic, num_turns=1):
        initial = self.conversation_starter(topic)
        history = [initial]
        for i in range(num_turns):
            history.append(self.answer_generator(topic, history))
            if i < num_turns - 1:
                follow_up = self.follow_upper(topic, history)
                history.append(follow_up)

        return history[:-1]
