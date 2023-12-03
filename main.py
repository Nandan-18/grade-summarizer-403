import scraper
import problems
import sys


username = sys.argv[1]
password = sys.argv[2]
course = sys.argv[3]

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
print("\n\nGRADING SUMMARY")
print("For Kattis User:", username)
print("Course:", course[:-4].upper(), "\n\n")

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

assign_final = assignment_overall / 11 * 0.8
open_final = total_solves["open-pool"] / 10 * 20

print("Assignment Overall (out of 80): {0:.02f}".format(assign_final))
print("Open Pool Grade (out of 20): {0:.02f}".format(open_final))

course_final = assign_final + open_final
print("Course Total (so far): {0:.02f}".format(course_final))
