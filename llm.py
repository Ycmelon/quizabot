import os
import nlpcloud

NLPCLOUD_API_KEY = os.environ["NLPCLOUD_API_KEY"]

client = nlpcloud.Client("chatdolphin", NLPCLOUD_API_KEY, gpu=True)


def get_answer(query: str) -> str:
    res = client.chatbot(
        query,
        context="You are a helpful chatbot providing brief and factual answers.",
        history=[
            {
                "input": "Which historical person is responsible for giving the teddy bear its name?",
                "response": """The teddy bear got its name from President Theodore Roosevelt. The story goes that during a hunting trip in Mississippi in 1902, Roosevelt refused to shoot a bear that had been tied up for him to shoot, deeming it unsportsmanlike. This act of compassion was widely publicized, and a political cartoon depicting the incident inspired a Brooklyn shopkeeper named Morris Michtom to create a stuffed bear and name it "Teddy's Bear" after the president. The toy became incredibly popular, and the name stuck, giving birth to the teddy bear we know today.""",
            },
            {
                "input": "What does ÷ represent?",
                "response": """The symbol "÷" represents division in mathematics. It is commonly used to denote the operation of dividing one number by another. For example, in the expression "10 ÷ 2," it indicates that you should divide 10 by 2, resulting in a quotient of 5.""",
            },
            {
                "input": "In what country did stamp collecting start",
                "response": """Stamp collecting, as we understand it today, began in the United Kingdom in the mid-19th century. The first postage stamp, the Penny Black, was issued in the UK in 1840, and it quickly gained popularity among collectors. Stamp collecting then spread to other countries, becoming a worldwide hobby.""",
            },
            {
                "input": "Which family of animals do wolves belong to?",
                "response": """Wolves belong to the family Canidae, which includes other canines such as domestic dogs, foxes, and jackals.""",
            },
        ],
    )

    return res["response"][:1000]
