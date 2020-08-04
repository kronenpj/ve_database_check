#!/usr/bin/env python3
"""
Compare pool text files to supplied database.
"""
import argparse
import inspect
import logging
import sys
from builtins import IndexError

from Levenshtein.StringMatcher import StringMatcher

import dbchecker.convert_parse_pool as cpp
from dbchecker.data import Data

log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)


def arg_parser():
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    # mylog.setLevel(logging.DEBUG)
    mylog.debug(f"Entering...")

    mylog.debug(f"Number of arguments: {len(sys.argv)}")

    argp = argparse.ArgumentParser(
        description="Compares provided files to the provided database."
    )
    argp.add_argument("-d", "--database", type=str, default=None, required=True)
    argp.add_argument(
        "-l", "--lev", type=int, default=1, help="Levenshtein distance, default=1"
    )
    argp.add_argument("infile", nargs="*", type=str, default=None)
    args: argparse.Namespace = argp.parse_args()
    return args


def compare_questions():
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    # mylog.setLevel(logging.DEBUG)
    mylog.debug(f"Entering...")

    args = arg_parser()

    for source in args.infile:
        print(f"Checking {source} against database.")
        content = cpp.consume_pool(source)

        lev_distance = args.lev

        (subels, subsubels, qs, q_data) = cpp.collect_data_from_source(content)
        data = Data(args.database)

        # Compare with the original database.
        for question in q_data.keys():
            try:
                mylog.debug(f"question: {q_data[question]}")
                database = data.question_data(question)

                lev_check(
                    question,
                    q_data[question].q_text,
                    database["text"],
                    "text",
                    lev_distance,
                )
                check(
                    question,
                    q_data[question].q_answer,
                    database["ans"],
                    "correct answer",
                )
                lev_check(
                    question,
                    q_data[question].q_a,
                    database["a"],
                    "response A",
                    lev_distance,
                )
                lev_check(
                    question,
                    q_data[question].q_b,
                    database["b"],
                    "response B",
                    lev_distance,
                )
                lev_check(
                    question,
                    q_data[question].q_c,
                    database["c"],
                    "response C",
                    lev_distance,
                )
                lev_check(
                    question,
                    q_data[question].q_d,
                    database["d"],
                    "response D",
                    lev_distance,
                )
            except IndexError:
                mylog.error(f"Question '{question}' does not exist in the database.\n")


def check(question, pool_data, database, reference):
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    # mylog.setLevel(logging.DEBUG)
    mylog.debug(f"Entering...")

    if pool_data != database:
        mylog.error(
            f"Difference: Question {question}, {reference} does not match the database "
        )
        mylog.error(f"           Pool: {pool_data}")
        mylog.error(f"       Database: {database}\n")


def lev_check(question, pool_data, database, reference, lev_distance):
    mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
    # mylog.setLevel(logging.DEBUG)
    mylog.debug(f"Entering...")

    lev = StringMatcher()

    lev.set_seqs(pool_data, database)
    if lev.distance() > lev_distance:
        mylog.error(
            f"Difference: Question {question}, {reference} does not match the database "
            f"(distance: {lev.distance()})."
        )
        mylog.error(f"           Pool: {pool_data}")
        mylog.error(f"       Database: {database}\n")


if __name__ == "__main__":  # pragma: no mutate
    # execute only if run as a script
    compare_questions()
