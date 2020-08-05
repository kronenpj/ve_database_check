"""
Global information to be used by the module.
"""

EXAM_INDICES = {
    "T": 1,
    "G": 2,
    "E": 3,
}


class Question:
    q_p_id: int
    q_id: str
    q_text: str
    q_answer: str
    q_a: str
    q_b: str
    q_c: str
    q_d: str

    def __init__(
        self,
        q_p_id=None,
        q_id=None,
        q_text=None,
        q_answer=None,
        q_a=None,
        q_b=None,
        q_c=None,
        q_d=None,
    ):
        self.q_p_id = q_p_id
        self.q_id = q_id
        self.q_text = q_text
        self.q_answer = q_answer
        self.q_a = q_a
        self.q_b = q_b
        self.q_c = q_c
        self.q_d = q_d

    def __str__(self):
        temp = f"    Pool ID: {self.q_p_id}\n"
        temp = f"{temp}Question ID: {self.q_id}\n"
        temp = f"{temp}  Text: {self.q_text}\n"
        temp = f"{temp}Answer: {self.q_answer}\n"
        temp = f"{temp}     A: {self.q_a}\n"
        temp = f"{temp}     B: {self.q_b}\n"
        temp = f"{temp}     C: {self.q_c}\n"
        temp = f"{temp}     D: {self.q_d}"
        return temp
