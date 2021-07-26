"""
Provide an interface to retrieve information from the database.
"""
import inspect
import logging

from sqlalchemy import create_engine, text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)
# sqllog = logging.getLogger('sqlalchemy.engine')
# sqllog.setLevel(logging.DEBUG)


class Data:
    """Class to encapsulate interactions with the exam database."""

    # Create a reference to the desired database for SQLAlchemy
    engine = None

    def __init__(self, engine_file: str):
        self.engine = create_engine(f"sqlite:///{engine_file}")

        self.dbbase = automap_base()

        # reflect the tables
        self.dbbase.prepare(self.engine, reflect=True)

        # Start a database session
        self.dbsession = Session(self.engine)

        # mapped classes are now created with names by default matching that of the table name.
        self.hamquestion = self.dbbase.classes.hamquestion
        self.lockedout = self.dbbase.classes.lockedout
        self.pool = self.dbbase.classes.pool
        self.specs = self.dbbase.classes.specs
        # These exist in the ARRL version of the database but this program doesn't check them.
        # self.graphics = self.dbbase.classes.graphics
        # self.metadata = self.dbbase.classes.metadata  # pragma: no mutate

    def pools(self) -> dict:
        """Return all pool identifiers and names."""
        mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
        # mylog.setLevel(logging.DEBUG)
        mylog.debug(f"Entering...")

        thing = self.dbsession.query(self.pool).order_by(text("p_id")).all()
        return {item.p_id: item.p_name for item in thing}

    def pool_title(self, pool: int) -> str:
        """Return a pool title."""
        mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
        # mylog.setLevel(logging.DEBUG)
        mylog.debug(f"Entering...")

        thing = self.dbsession.query(self.pool).filter(self.pool.p_id == pool).all()
        pools = ""
        for item in thing:
            pools = item.p_formalname
        return pools

    def pool_questions(self, pool: int) -> int:
        """Return the number of expected questions for the provided pool."""
        mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
        # mylog.setLevel(logging.DEBUG)
        mylog.debug(f"Entering...")

        thing = self.dbsession.query(self.pool).filter(self.pool.p_id == pool)
        return thing[0].p_numq

    def specs_all_leadstrings(self) -> dict:
        """Return all 'lead strings' in all pools."""
        mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
        # mylog.setLevel(logging.DEBUG)
        mylog.debug(f"Entering...")

        thing = (
            self.dbsession.query(self.specs).order_by(text("s_p_id")).all()
        )  # pragma: no mutate
        return {item.s_leadstrings: item.s_count for item in thing}  # pragma: no mutate

    def specs_pool_leadstrings(self, pool: int) -> dict:
        """Return 'lead strings' for the requested pool."""
        mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
        # mylog.setLevel(logging.DEBUG)
        mylog.debug(f"Entering...")

        thing = (
            self.dbsession.query(self.specs)
            .filter_by(s_p_id=pool)
            .order_by(text("s_leadstrings"))
            .all()
        )
        return {item.s_leadstrings: item.s_count for item in thing}

    def all_lockedout_questions(self) -> list:
        """Return all questions listed as locked out."""
        mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
        # mylog.setLevel(logging.DEBUG)
        mylog.debug(f"Entering...")

        mylog.debug(f"Gathering all locked-out questions")
        thing = self.dbsession.query(self.lockedout).all()
        return [item.lo_q_id for item in thing]

    def lockedout_questions(self, pool: int) -> list:
        """Return questions listed as locked out for a supplied pool."""
        mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
        # mylog.setLevel(logging.DEBUG)
        mylog.debug(f"Entering...")

        mylog.debug(f"Looking for locked-out questions in pool {pool}")
        thing = (
            self.dbsession.query(self.lockedout)
            .filter(self.lockedout.lo_p_id == pool)
            .all()
        )
        return [item.lo_q_id for item in thing]

    def questions_leadstring(self, leadstring: str) -> list:
        """Return questions in the requested 'lead string' group."""
        mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
        # mylog.setLevel(logging.DEBUG)
        mylog.debug(f"Entering...")

        mylog.debug(f"Looking for {leadstring}%")
        thing = (
            self.dbsession.query(self.hamquestion)
            .filter(self.hamquestion.q_id.like(f"{leadstring}%"))
            .order_by(text("q_id"))
            .all()
        )
        return [item.q_id for item in thing]

    def question_data(self, question_id: str) -> dict:
        """Return requested question in a dictionary."""
        mylog = log.getChild(f"{inspect.currentframe().f_code.co_name}")
        # mylog.setLevel(logging.DEBUG)
        mylog.debug(f"Entering...")

        mylog.debug(f"Gathering data for {question_id}%")
        thing = (
            self.dbsession.query(self.hamquestion)
            .filter(self.hamquestion.q_id == question_id)  # pragma: no mutate
            .all()
        )
        mylog.debug(f"thing: <q_text={thing[0].q_text}, q_ans={thing[0].q_ans}>")

        # Construct the response
        return {
            "text": thing[0].q_text.strip(),
            "ans": thing[0].q_ans.strip(),
            "a": thing[0].q_a.strip(),
            "b": thing[0].q_b.strip(),
            "c": thing[0].q_c.strip(),
            "d": thing[0].q_d.strip(),
        }
