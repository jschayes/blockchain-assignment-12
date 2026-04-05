import os
import shutil
import subprocess
import re
import sys
from pathlib import Path


def strip_ansi_codes(s):
    """
        forge outputs text with ANSI codes for color
        We need to strip them out to get the latex regexes to work
    """
    return re.sub(r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?', '', s)


def validate(code_path, retry=0):
    project_name = "AMM"
    student_file = 'AMM.sol'
    test_path = Path(__file__).parent.absolute() / project_name  # This is where the test contract files live
    test_file = test_path / "src" / student_file  # This is the actual file to be tested

    # Find the student's file submission
    if (code_path / student_file).is_file():
        from_file = code_path / student_file  # From the repository root
    else:
        from_file = code_path / project_name / "src" / student_file  # or from /src (whole contract uploaded)

    if not from_file.is_file():
        print(f"Error: unable to locate your '{student_file}' file in your "
              f"repo root directory or\n{os.fspath(from_file)}")
        sys.exit(1)

    # Copy the students file into the test contract
    try:
        shutil.copyfile(os.fspath(from_file), os.fspath(test_file))
    except Exception as e:
        print(f"Failed to copy file {student_file}\n{e}")

    num_passed = num_failed = 0
    max_retries = 3
    forge_failed = False
    try:
        proc = subprocess.check_output(['/home/codio/.foundry/bin/forge', 'test'], cwd=test_path)
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:  # If some forge tests fail, forge returns with code 1
            forge_failed = True  # We need to note this because when forge fails, its output is different
            proc = e.output
        else:
            return 0
    except Exception as e:
        if retry < max_retries:
            return validate(code_path, retry=retry + 1)
        else:
            print("Could not run 'forge test'")
            sys.exit(1)

    output = strip_ansi_codes(proc.decode('utf-8').splitlines()[-1])
    if forge_failed:
        rmatch = re.search('(\d+) tests succeeded', output)
        if rmatch:
            num_passed = int(rmatch.group(1))
            print(f"num_passed = {num_passed}")
        rmatch = re.search('(\w+) failing tests', output)
        if rmatch:
            num_failed = int(rmatch.group(1))
            print(f"num_failed = {num_failed}")
    else:
        rmatch = re.search('(\d+) passed', output)
        if rmatch:
            num_passed = int(rmatch.group(1))
            print(f"num_passed = {num_passed}")
        rmatch = re.search('(\d+) failed', output)
        if rmatch:
            num_failed = int(rmatch.group(1))
            print(f"num_failed = {num_failed}")

    score = 0
    if num_passed + num_failed > 0:
        score = (100.0 * num_passed) / (num_passed + num_failed)

    print(f"\nFor more indepth feedback, open a terminal and type 'cd {project_name}'\n"
          "then run the tests by typing 'forge test' or 'forge test -vvv'\n")
    return score


if __name__ == '__main__':
    score = validate(Path("./").absolute())
    print(f"Score = {score}")
