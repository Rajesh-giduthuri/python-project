import json
from pathlib import Path

from database.db import get_session
from database.models import (
    Meeting,
    KeyPoint,
    Decision,
    ActionItem
)


# --------------------------------------------------
# SAVE MEETING
# --------------------------------------------------

def save_meeting(
    filename: str,
    transcript: str,
    meeting_data: dict
):
    """
    Save a complete meeting and its
    analysis data into SQLite.
    """

    session = get_session()

    try:

        # ------------------------------------------
        # CREATE MEETING
        # ------------------------------------------

        meeting = Meeting(
            filename=filename,
            transcript=transcript,
            summary=meeting_data.get(
                "summary",
                ""
            )
        )

        session.add(meeting)

        # Commit first so meeting.id is generated
        session.commit()

        # ------------------------------------------
        # KEY POINTS
        # ------------------------------------------

        for point in meeting_data.get(
            "key_points",
            []
        ):

            key_point = KeyPoint(
                meeting_id=meeting.id,
                content=point
            )

            session.add(key_point)


        # ------------------------------------------
        # DECISIONS
        # ------------------------------------------

        for decision in meeting_data.get(
            "decisions",
            []
        ):

            decision_record = Decision(
                meeting_id=meeting.id,
                content=decision
            )

            session.add(
                decision_record
            )


        # ------------------------------------------
        # ACTION ITEMS
        # ------------------------------------------

        for item in meeting_data.get(
            "action_items",
            []
        ):

            action_item = ActionItem(
                meeting_id=meeting.id,
                task=item.get(
                    "task",
                    ""
                ),
                owner=item.get(
                    "owner",
                    "Not specified"
                ),
                deadline=item.get(
                    "deadline",
                    "Not specified"
                )
            )

            session.add(action_item)


        # ------------------------------------------
        # SAVE EVERYTHING
        # ------------------------------------------

        session.commit()

        print(
            "\nMeeting saved successfully!"
        )

        print(
            f"Meeting ID: {meeting.id}"
        )

        return meeting.id


    except Exception:

        session.rollback()

        raise


    finally:

        session.close()


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    BASE_DIR = (
        Path(__file__)
        .resolve()
        .parent.parent
    )


    transcript_file = (
        BASE_DIR
        / "outputs"
        / "transcript.txt"
    )


    json_file = (
        BASE_DIR
        / "outputs"
        / "meeting_analysis.json"
    )


    # ----------------------------------------------
    # READ TRANSCRIPT
    # ----------------------------------------------

    with open(
        transcript_file,
        "r",
        encoding="utf-8"
    ) as file:

        transcript = file.read()


    # ----------------------------------------------
    # READ JSON
    # ----------------------------------------------

    with open(
        json_file,
        "r",
        encoding="utf-8"
    ) as file:

        meeting_data = json.load(file)


    # ----------------------------------------------
    # SAVE
    # ----------------------------------------------

    save_meeting(
        filename="short_meeting-3.webm",
        transcript=transcript,
        meeting_data=meeting_data
    )