"""
    This script contains the dspy classes for generating LLM suggestions given user's information and context.
"""

import dspy


class ResponseSignature(dspy.Signature):
    """Generate a tailored answer to the user's question using the context and user's information"""

    user_query = dspy.InputField(
        desc="Information about the user followed by a question"
    )
    context = dspy.InputField(
        desc="An extract from a news article that may be used to answer the user's query"
    )
    response = dspy.OutputField(
        desc="Justified answer to the user's question within 100 tokens"
    )


class GenerateSuggestions(dspy.Module):
    """
    DSPY module for generating LLM responses for user's query provided the context by using Chain of Thought reasoning.
    """

    def __init__(self):
        super().__init__()
        self.cot = dspy.ChainOfThought(ResponseSignature)

    def forward(self, about_me: str, context: str) -> str:
        """
        Forward function takes user's info and the context.
        Generates LLM response using Chain of Thought reasoning.

        Args:
            about_me (str): User's Information and Query.
            context (str): Relevant factoid for answering the Query.

        Returns:
            output (Dict): Returns reasoning and response for the given query.
        """
        output = self.cot(user_query=about_me, context=context)
        return output
