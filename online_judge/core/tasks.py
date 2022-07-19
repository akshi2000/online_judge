from online_judge.celery import app
from .models import *
import time
import os

COMPILED_LANGUAGES = [
    "C",
    "CPP",
    "Java",
]

LANGUAGE_EXTENSIONS = {
    "C": "c",
    "CPP": "cpp",
    "Python": "py",
    "Java": "java",
}


@app.task(name="compile_and_run", bind=True, max_retries=3)
def compile_and_run(self, submission_id):
    def done():
        os.system(f"rm -fr /home/guest/{submission_id}")

    submission = Submission.objects.get(id=submission_id)
    ques = submission.ques
    testcases = ques.testcases.all()
    lang = submission.lang
    extension = LANGUAGE_EXTENSIONS.get(lang, "txt")
    profile, created = Profile.objects.get_or_create(user=submission.user)

    os.system(f"mkdir /home/guest/{submission_id}")
    DIR = f"/home/guest/{submission_id}"

    # executes this command using ubuntu user
    with open(f"{DIR}/{submission_id}.{extension}", "w") as f:
        f.write(submission.code)

    # compile code in case of c, c++ and Java
    if lang in COMPILED_LANGUAGES:
        compile = 0

        if lang == "C":
            compile = os.system(
                f"gcc {DIR}/{submission_id}.{extension} -o {DIR}/{submission_id}"
            )

        elif lang == "CPP":
            compile = os.system(
                f"g++ {DIR}/{submission_id}.{extension} -o {DIR}/{submission_id}"
            )

        elif lang == "Java":
            pass

        if compile != 0:
            submission.verdict = "Compilation Error"
            submission.save()
            done()
            return

        else:
            submission.verdict = "Compiled"
            submission.save()

    # command for executing code (language specific)
    cmd = ""
    if lang in ["C", "CPP"]:
        cmd = f"{DIR}/{submission_id}"
    elif lang == "Python":
        cmd = f"python3 {DIR}/{submission_id}.{extension}"
    elif lang == "Java":
        pass

    # Testing begins...
    for i, testcase in enumerate(testcases):
        submission.verdict = f"Running on Testcase {i + 1}"
        submission.save()

        with open(f"{DIR}/{submission_id}.tc", "w") as f:
            f.write(testcase.testcase)

        err_code = os.system(
            f'su - guest -c "schroot -c compile-run --directory {DIR} -- timeout {ques.timelimit} {cmd} < {DIR}/{submission_id}.tc" > {DIR}/{submission_id}.out'
        )

        if err_code == 31744:
            submission.verdict = f"Time Limit Exceeded on Testcase {i + 1}"
            submission.save()
            done()
            profile.tle_submissions += 1
            profile.save()
            return

        elif err_code != 0:
            submission.verdict = f"Runtime Error on Testcase {i + 1}"
            submission.save()
            done()
            profile.runtime_error_submissions += 1
            profile.save()
            return

        with open(f"{DIR}/{submission_id}.ans", "w") as f:
            f.write(testcase.answer)

        match = os.system(
            f"diff -ZB {DIR}/{submission_id}.out {DIR}/{submission_id}.ans"
        )

        if match != 0:
            submission.verdict = f"Wrong Answer on Testcase {i + 1}"
            submission.save()
            done()
            profile.incorrect_submissions += 1
            profile.save()
            return

    profile = Profile.objects.get(user=submission.user)

    submission.verdict = f"Correct Answer!!"
    profile.correct_submissions += 1
    profile.save()
    submission.save()
    done()
    return


@app.task(name="test", bind=True, max_retries=3)
def test(self):
    time.sleep(5)
