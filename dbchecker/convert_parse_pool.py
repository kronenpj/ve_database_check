#!/usr/bin/env python

"""A simple python script template.

"""
import inspect
import logging
import re
import sys
from typing import Any, Dict, List, Tuple

from .constants import EXAM_INDICES
from .globals import Question

global_log = logging.getLogger(__package__)
log = global_log.getChild(__name__.replace(f"{__package__}.", ""))
log.setLevel(global_log.getEffectiveLevel())


def collect_data_from_source(content: list) -> Tuple[List, List, Dict, Dict]:
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    mylog.setLevel(global_log.getEffectiveLevel())
    mylog.debug(f"Entering...")

    # Start parsing the lines of text.
    subelements = _parse_subelements(content)

    subsubelements = [temp for temp in _parse_subsubelements(content)]
    questions = {
        subsubelement: [temp for temp in _parse_question_ids(content, subsubelement)]
        for subsubelement in subsubelements
    }

    question_data = {}
    for subsubelement, value in questions.items():
        for question in value:
            question_data[question] = _parse_question(content, question)

    return subelements, subsubelements, questions, question_data


def consume_pool(inputfile: Any) -> List:
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    mylog.setLevel(global_log.getEffectiveLevel())
    mylog.debug(f"Entering...")

    file_content = []
    if inputfile is sys.stdin:
        print(f"Expecting data on standard input...")
        for line in sys.stdin:
            mylog.debug(f"Line read: {line.strip()}")
            file_content.append(line.strip())
    else:
        mylog.info(f"Input filename: {inputfile}")
        with open(inputfile, "r") as infile:
            for line in infile:
                file_content.append(line.strip())

    # Remove header cruft as best we can.
    file_content = _prune_content(file_content)

    return file_content


def _prune_content(filelines: list) -> list:
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    mylog.setLevel(global_log.getEffectiveLevel())
    mylog.debug(f"Entering...")

    found_exam_start_line = -1

    for line in range(len(filelines)):
        if filelines[line].startswith(
            ("SUBELEMENT T1", "SUBELEMENT G1", "SUBELEMENT E1")
        ):
            found_exam_start_line = line

    retlist = []
    for item in range(found_exam_start_line - 1, len(filelines)):
        mylog.debug(f"Appending read: {filelines[item]}")
        retlist.append(filelines[item])

    return retlist


def _parse_subelements(filelines: list) -> list:
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    mylog.setLevel(global_log.getEffectiveLevel())
    mylog.debug(f"Entering...")

    regexp = re.compile(r"^SUBELEMENT ([TGE][0-9]) - .*$")

    retval = []
    for line in filelines:
        if line.startswith(("SUBELEMENT T", "SUBELEMENT G", "SUBELEMENT E")):
            mylog.debug(f"Matched line: {line}")
            retval.append(regexp.match(line).group(1))

    mylog.debug(f"Subelements found: {retval}")
    return retval


def _parse_subsubelements(filelines: list) -> list:
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    mylog.setLevel(global_log.getEffectiveLevel())
    mylog.debug(f"Entering...")

    found_exam_start = False
    regexp = re.compile(rf"^([TGE][0-9][A-Z]) .*$")

    retval = []
    for line in filelines:
        mylog.debug(f"File line: {line}")
        if not found_exam_start:
            # Skip through the file header until we find the start of the exam proper.
            if line.startswith(("SUBELEMENT T", "SUBELEMENT G", "SUBELEMENT E")):
                found_exam_start = True
            continue
        try:
            retval.append(regexp.match(line).group(1))
        except AttributeError:
            pass  # This happens a lot :)

    mylog.debug(f"Subsubelements found: {retval}")
    return retval


def _parse_question_ids(filelines: list, subelement: str) -> list:
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    mylog.setLevel(global_log.getEffectiveLevel())
    mylog.debug(f"Entering...")

    found_exam_start = False
    regexp = re.compile(rf"^({subelement}[0-9]+) .*$")

    retval = []
    for line in filelines:
        if not found_exam_start:
            # Skip through the file header until we find the start of the exam proper.
            if line.startswith(("SUBELEMENT T", "SUBELEMENT G", "SUBELEMENT E")):
                found_exam_start = True
            continue
        try:
            retval.append(regexp.match(line).group(1))
        except AttributeError:
            pass  # This happens a lot :)

    return retval


def _parse_question(filelines: list, question: str) -> Question:
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    mylog.setLevel(global_log.getEffectiveLevel())
    mylog.debug(f"Entering...")

    found_question_start = False

    question_answer = re.compile(rf"^{question} \(([A-D])\).*$")
    question_options = re.compile(rf"^([A-D])\. (.*)$")
    answer = ""
    choices = {}
    text = ""
    for line in filelines:
        if not found_question_start:
            # Slip lines until we find the question we were told to find.
            if question_answer.match(line):
                mylog.debug(f"Line: {line}")
                answer = question_answer.match(line).group(1)
                mylog.debug(f"Start of question {question}.")
                mylog.debug(f"Grabbed answer: {answer}")
                found_question_start = True
        else:
            # Stop when we hit the double-tilde signifying the end of a question.
            if line == "~~":
                mylog.debug(f"End of question {question}.")
                break
            # Second and remaining lines of the question
            if not question_options.match(line):
                text = f"{text} {line}".strip()
                mylog.debug(f"Question text: {text}")
            else:
                mylog.debug("Parsing responses.")
                mylog.debug(f"{line}")
                if question_options.match(line) is not None:
                    choice, choice_text = question_options.match(line).group(1, 2)
                    if choice in ["A", "B", "C", "D"]:
                        choices[choice] = choice_text

    pool_id = EXAM_INDICES[question[0]]
    return Question(
        pool_id,
        question,
        text,
        answer,
        choices["A"],
        choices["B"],
        choices["C"],
        choices["D"],
    )
