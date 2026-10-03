from database.db import get_session
from database.models import (
    Meeting,
    KeyPoint,
    Decision,
    ActionItem
)


# --------------------------------------------------
# GET ALL MEETINGS
# --------------------------------------------------

def get_all_meetings():

    session = get_session()

    try:

        meetings = (
            session.query(Meeting)
            .order_by(Meeting.id.desc())
            .all()
        )

        return meetings

    finally:

        session.close()


# --------------------------------------------------
# GET MEETING BY ID
# --------------------------------------------------

def get_meeting(
    meeting_id: int
):

    session = get_session()

    try:

        meeting = (
            session.query(Meeting)
            .filter(
                Meeting.id == meeting_id
            )
            .first()
        )

        return meeting

    finally:

        session.close()


# --------------------------------------------------
# GET KEY POINTS
# --------------------------------------------------

def get_key_points(
    meeting_id: int
):

    session = get_session()

    try:

        return (
            session.query(KeyPoint)
            .filter(
                KeyPoint.meeting_id == meeting_id
            )
            .all()
        )

    finally:

        session.close()


# --------------------------------------------------
# GET DECISIONS
# --------------------------------------------------

def get_decisions(
    meeting_id: int
):

    session = get_session()

    try:

        return (
            session.query(Decision)
            .filter(
                Decision.meeting_id == meeting_id
            )
            .all()
        )

    finally:

        session.close()


# --------------------------------------------------
# GET ACTION ITEMS
# --------------------------------------------------

def get_action_items(
    meeting_id: int
):

    session = get_session()

    try:

        return (
            session.query(ActionItem)
            .filter(
                ActionItem.meeting_id == meeting_id
            )
            .all()
        )

    finally:

        session.close()


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    meetings = get_all_meetings()

    print(
        "\nTotal meetings:",
        len(meetings)
    )


    for meeting in meetings:

        print("\n" + "=" * 60)

        print(
            f"Meeting ID: {meeting.id}"
        )

        print(
            f"Filename: {meeting.filename}"
        )

        print(
            f"Summary: {meeting.summary}"
        )


        key_points = get_key_points(
            meeting.id
        )

        print("\nKey Points:")

        for point in key_points:

            print(
                f"- {point.content}"
            )


        decisions = get_decisions(
            meeting.id
        )

        print("\nDecisions:")

        for decision in decisions:

            print(
                f"- {decision.content}"
            )


        action_items = get_action_items(
            meeting.id
        )

        print("\nAction Items:")

        for item in action_items:

            print(
                f"- Task: {item.task}"
            )

            print(
                f"  Owner: {item.owner}"
            )

            print(
                f"  Deadline: {item.deadline}"
            )