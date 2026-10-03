import json
from pathlib import Path


# --------------------------------------------------
# EXTRACT STRUCTURED DATA
# --------------------------------------------------

def extract_meeting_data(analysis: str) -> dict:
    """
    Convert the meeting analysis text into
    structured Python data.
    """

    if not analysis.strip():
        raise ValueError(
            "Analysis text is empty."
        )

    data = {
        "summary": "",
        "key_points": [],
        "decisions": [],
        "action_items": []
    }

    current_section = None

    lines = analysis.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # ------------------------------------------
        # SECTION DETECTION
        # ------------------------------------------

        if line.upper().startswith("SUMMARY:"):
            current_section = "summary"

            value = line.split(
                ":", 1
            )[1].strip()

            if value:
                data["summary"] = value

            continue


        if line.upper().startswith("KEY POINTS:"):
            current_section = "key_points"
            continue


        if line.upper().startswith("DECISIONS:"):
            current_section = "decisions"
            continue


        if line.upper().startswith("ACTION ITEMS:"):
            current_section = "action_items"
            continue


        # ------------------------------------------
        # SUMMARY
        # ------------------------------------------

        if current_section == "summary":

            data["summary"] += (
                " " + line
            )

            continue


        # ------------------------------------------
        # KEY POINTS
        # ------------------------------------------

        if current_section == "key_points":

            if line.startswith("-"):

                point = line[1:].strip()

                if point:
                    data["key_points"].append(
                        point
                    )

            continue


        # ------------------------------------------
        # DECISIONS
        # ------------------------------------------

        if current_section == "decisions":

            if line.startswith("-"):

                decision = line[1:].strip()

                if decision:
                    data["decisions"].append(
                        decision
                    )

            continue


        # ------------------------------------------
        # ACTION ITEMS
        # ------------------------------------------

        if current_section == "action_items":

            if line.startswith("- Task:"):

                task = line.replace(
                    "- Task:",
                    "",
                    1
                ).strip()

                data["action_items"].append(
                    {
                        "task": task,
                        "owner": "Not specified",
                        "deadline": "Not specified"
                    }
                )

                continue


            if line.startswith("Owner:"):

                if data["action_items"]:

                    owner = line.replace(
                        "Owner:",
                        "",
                        1
                    ).strip()

                    data["action_items"][-1][
                        "owner"
                    ] = owner

                continue


            if line.startswith("Deadline:"):

                if data["action_items"]:

                    deadline = line.replace(
                        "Deadline:",
                        "",
                        1
                    ).strip()

                    data["action_items"][-1][
                        "deadline"
                    ] = deadline

                continue


    # ------------------------------------------
    # CLEAN SUMMARY
    # ------------------------------------------

    data["summary"] = data[
        "summary"
    ].strip()


    return data


# --------------------------------------------------
# SAVE JSON
# --------------------------------------------------

def save_meeting_json(
    data: dict,
    output_path: str | Path
):
    """
    Save structured meeting data
    as a JSON file.
    """

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\nStructured JSON saved to:"
        f"\n{output_path}"
    )


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    BASE_DIR = Path(
        __file__
    ).resolve().parent.parent


    analysis_file = (
        BASE_DIR
        / "outputs"
        / "meeting_analysis.txt"
    )


    json_file = (
        BASE_DIR
        / "outputs"
        / "meeting_analysis.json"
    )


    # ----------------------------------------------
    # READ ANALYSIS
    # ----------------------------------------------

    with open(
        analysis_file,
        "r",
        encoding="utf-8"
    ) as file:

        analysis = file.read()


    # ----------------------------------------------
    # EXTRACT
    # ----------------------------------------------

    meeting_data = extract_meeting_data(
        analysis
    )


    # ----------------------------------------------
    # DISPLAY
    # ----------------------------------------------

    print("\n")
    print("=" * 60)
    print("STRUCTURED MEETING DATA")
    print("=" * 60)

    print(
        json.dumps(
            meeting_data,
            indent=4,
            ensure_ascii=False
        )
    )

    print("=" * 60)


    # ----------------------------------------------
    # SAVE
    # ----------------------------------------------

    save_meeting_json(
        meeting_data,
        json_file
    )