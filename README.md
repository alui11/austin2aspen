# austin2aspen
Goal: Scrape assessment results from UTexas and record grades in Aspen.

Version 1: scrape results from UTexas and output to csv.

## Flow
1. Log in to UTexas.
2. Download main landing page and extract links for each course.
3. Download course pages and extract assignment ID.
4. Download the assignment results page and extract link for each student.
5. Download student results page and extract total number of correct problems.
6. Print to csv.

## Function defs
```python
def authenticate():
    """Initializes web requester with authentication for UTexas login."""

def download_page(link):
    """Downloads html pointed to by the link."""

def extract_course_links(html):
    """Parse html and return dictionary of {period_no: course link}."""

def extract_assignment_links(html):
    """Calls extract_assignmentIDs and converts IDs to assignment result links. Returns dict of {assignment_name: link}."""

def extract_student_links(html):
    """Parse html and return dictionary of {student_name: link}."""

def compute_student_score(html):
    """Given student restuls page, return the total number of assignment problems that have a nonzero score."""

def get_student_scores(student_name2link):
    """Returns dict of {student_name: score}."""
```

## Links
login portal:
https://enterprise.login.utexas.edu/idp/profile/SAML2/Redirect/SSO?execution=e2s1

landing page:
https://quest.cns.utexas.edu/instructor/courses

period 1 link:
https://quest.cns.utexas.edu/instructor/courses/show?course=755474

period 1 work intro results page:
https://quest.cns.utexas.edu/instructor/elements/results?elementx=assignment_1520312

student results page:
https://quest.cns.utexas.edu/instructor/instances/show?instance=courseuserassignment_43078046

