#!/usr/bin/env python

"""A simple python script template.

"""

from __future__ import print_function, with_statement, unicode_literals, division

import inspect
import logging
import re
from typing import List, Dict, Any

import sys

from .globals import Question, EXAM_INDICES

log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)


def collect_data_from_source(content: list) -> (List, List, Dict, Dict):
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    # mylog.setLevel(logging.DEBUG)
    mylog.debug(f"Entering...")

    # Start parsing the lines of text.
    subelements = _parse_subelements(content)

    subsubelements = list()
    for temp in _parse_subsubelements(content):
        subsubelements.append(temp)

    questions = dict()
    for subsubelement in subsubelements:
        questions[subsubelement] = list()
        for temp in _parse_question_ids(content, subsubelement):
            questions[subsubelement].append(temp)

    question_data = dict()
    for subsubelement in questions.keys():
        for question in questions[subsubelement]:
            question_data[question] = _parse_question(content, question)

    return subelements, subsubelements, questions, question_data


def consume_pool(inputfile: Any) -> List:
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    # mylog.setLevel(logging.DEBUG)
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
    # mylog.setLevel(logging.DEBUG)
    mylog.debug(f"Entering...")

    found_exam_start_line = -1

    for line in range(0, len(filelines)):
        if filelines[line].startswith(
            ("SUBELEMENT T1", "SUBELEMENT G1", "SUBELEMENT E1")
        ):
            found_exam_start_line = line

    retlist = list()
    for item in range(found_exam_start_line - 1, len(filelines)):
        mylog.debug(f"Appending read: {filelines[item]}")
        retlist.append(filelines[item])

    return retlist


def _parse_subelements(filelines: list) -> list:
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    # mylog.setLevel(logging.DEBUG)
    mylog.debug(f"Entering...")

    retval = list()
    regexp = re.compile(r"^SUBELEMENT ([TGE][0-9]) - .*$")

    for line in filelines:
        if line.startswith(("SUBELEMENT T", "SUBELEMENT G", "SUBELEMENT E")):
            mylog.debug(f"Matched line: {line}")
            retval.append(regexp.match(line).group(1))

    mylog.debug(f"Subelements found: {retval}")
    return retval


def _parse_subsubelements(filelines: list) -> list:
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    # mylog.setLevel(logging.DEBUG)
    mylog.debug(f"Entering...")

    found_exam_start = False
    retval = list()
    regexp = re.compile(rf"^([TGE][0-9][A-Z]) .*$")

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
    mylog.debug(f"Entering...")

    found_exam_start = False
    retval = list()
    regexp = re.compile(rf"^({subelement}[0-9]+) .*$")

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
    mylog.debug(f"Entering...")

    found_question_start = False

    question_answer = re.compile(rf"^{question} \(([A-D])\).*$")
    question_options = re.compile(rf"^([A-D])\. (.*)$")
    answer = ""
    choices = dict()
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
    retval = Question(
        pool_id,
        question,
        text,
        answer,
        choices["A"],
        choices["B"],
        choices["C"],
        choices["D"],
    )
    return retval
