def calculate_risk(report_count: int):

    if report_count == 0:
        return 0

    if report_count <= 2:
        return 25

    if report_count <= 5:
        return 50

    if report_count <= 10:
        return 75

    return 95