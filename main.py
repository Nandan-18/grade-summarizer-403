import scraper
import problems
import sys

# Read command line arguments
if len(sys.argv) not in {4, 6}:
    print(
        "Usage: python3 main.py <kattis-username> <password> <course-file> [<total-seminar-score> <project-score>]"
    )
    print("See README.md for details")
    quit()

username = sys.argv[1]
password = sys.argv[2]

course = sys.argv[3]
if course not in {"cmput303.txt", "cmput403.txt"}:
    print("Invalid course file name:", course)
    print("Should be one of cmput303.txt or cmput403.txt")

if len(sys.argv) >= 5:
    if course == "cmput403.txt":
        if len(sys.argv) != 6:
            print("Error: SEMINAR and PROJECT must be set when COURSE=403.")
            exit(1)

        try:
            seminar_total = float(sys.argv[4])
        except:
            seminar_total = -1.0
        try:
            project_total = float(sys.argv[5])
        except:
            project_total = -1.0

        if seminar_total < 0.0 or seminar_total > 10.0:
            print("Bad seminar total:", sys.argv[4])
            print("Should be a floating point value between 0.0 and 10.0")
            quit()
        if project_total < 0.0 or project_total > 15.0:
            print("Bad project total:", sys.argv[5])
            print("Should be a floating point value between 0.0 and 15.0")
            quit()
    else:
        seminar_total = -1.0
        project_total = -1.0
else:
    project_total = 0.0
    seminar_total = 0.0
# Get the assignment specification data (problems, deadlines, etc)
assignments = problems.getAssignments(course)

course_start = assignments["course-start"][1]
course_cutoff = assignments["course-cutoff"][1]

# Get the list of problems solved as well as their earliest solve
# during the course
userdata = scraper.getAllSolvedProblems(username, password, course_start)


# the student's score (out of 100) for a particular accepted submission
# does not reflect whether there was a header or not!
def submission_score(deadline, subtime):
    if subtime < course_start or subtime > course_cutoff:
        return 0
    elif subtime > deadline:
        return 50
    else:
        return 100


def message(score):
    if score == 0:
        return "UNSOLVED"
    if score == 50:
        return "ACCEPTED (LATE)"
    if score == 100:
        return "ACCEPTED"

    return "ERROR!"


# now get the total scores in each pool category
assignment_overall = 0.0
total_solves = {}

# finally, print the report to the user!
print()
print()
print("GRADING SUMMARY")
print("For Kattis user:", username)
print("Course:", course[:-4].upper())
print()
print(
    "Disclaimer: this tool is still in testing, please report any issues to the course instructor"
)
print()
for a in assignments:
    if a in {"course-start", "course-cutoff"}:
        continue

    print(a)

    problist, deadline = assignments[a]

    total_solves[a] = 0
    grade_total = 0

    for prob in problist:
        if prob in userdata:
            score = submission_score(deadline, userdata[prob])
        else:
            score = 0

        if a[:4] == "week" or score > 0:
            print(prob, "-", message(score))

        if score > 0:
            total_solves[a] += 1
        grade_total += score

    assignment_grade = grade_total / len(problist)

    if a[:4] == "week":
        print("Assignment grade (out of 100%): {0:.02f}".format(assignment_grade))
        assignment_overall += assignment_grade
    elif a[:4] == "open":
        if total_solves[a] == 0:
            print("NO SOLVES YET")

    print()

if course == "cmput303.txt":
    assign_final = assignment_overall / 11 * 0.8
    open_final = total_solves["open-pool"] / 10 * 20

    print("Assignment Overall (out of 80): {0:.02f}".format(assign_final))
    print("Open Pool Grade (out of 20): {0:.02f}".format(open_final))

    course_final = assign_final + open_final
    print("Course Total (so far): {0:.02f}".format(course_final))

elif course == "cmput403.txt":
    assign_final = assignment_overall / 11 * 0.6

    easy = total_solves["open-pool-easy"]
    medium = total_solves["open-pool-medium"]
    hard = total_solves["open-pool-hard"]
    open_score = min(min(min(easy, 2) + 2 * medium, 12) + 3 * hard, 15)

    project_final = project_total
    seminar_final = seminar_total

    print("Assignment Overall Grade (out of 60): {0:.02f}".format(assign_final))
    print("Open Pool Grade (out of 15): {0:.02f}".format(open_score))
    print("Seminar Grade (out of 10): {0:.02f}".format(seminar_final))
    print("Project Grade (out of 15): {0:.02f}".format(project_final))

    course_final = assign_final + open_score + project_final + seminar_final
    print("Course Total (so far): {0:.02f}%".format(course_final))
