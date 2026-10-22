import ast
import json
import re
from statistics import mean

from chat import add_assistant_message, add_user_message, chat
from models import MODEL_SONNET


def generate_dataset():
    prompt = """
Generate a evaluation dataset for a prompt evaluation.
The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks.
Generate an array of JSON objects, each representing task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
    {
        "task": "Description of task",
        "format": "json" or "python" or "regex",
        "solution_criteria": "Key criteria for evaluating teh solution",
    },
    ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""
    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```json")
    text = chat(messages, stop_sequences=["```"])
    return json.loads(text)


def run_prompt(test_case):
    """Merges the prompt and test case input, then returns the result."""
    prompt = f"""
Please solve the following task:

{test_case["task"]}

* Respond only with Python, JSON, or a plain Regex
* Do not add any comments or commentary or explanation
"""
    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```code")
    return chat(messages, stop_sequences=["```"])


def validate_json(text):
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0


def validate_python(text):
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0


def validate_regex(text):
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0


def grade_by_code(test_case, response):
    """Returns 10 if the response parses as the format declared in the test case, else 0."""
    fmt = test_case["format"]
    if fmt == "json":
        return validate_json(response)
    if fmt == "python":
        return validate_python(response)
    return validate_regex(response)


def grade_by_model(test_case, output):
    """Uses Claude to grade the output for a test case; returns a dict with strengths, weaknesses, reasoning, score."""
    eval_prompt = f"""
You are an expert AWS code reviewer. Your task is to evaluate the following AI-generated solution.

Original Task:
<task>
{test_case["task"]}
</task>

Solution to Evaluate:
<solution>
{output}
</solution>

Criteria you should use to evaluate the solution:
<criteria>
{test_case["solution_criteria"]}
</criteria>

Output Format:
Provide your evaluation as a structured JSON object with the following fields, in this specific order:
- "strengths": An array of 1-3 key strengths
- "weaknesses": An array of 1-3 key areas for improvement
- "reasoning": A concise explanation of your overall assessment
- "score": A number between 1-10

Respond with JSON. Keep your response concise and direct.
Example response shape:
{{
    "strengths": string[],
    "weaknesses": string[],
    "reasoning": string,
    "score": number
}}
"""
    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")
    eval_text = chat(messages, model=MODEL_SONNET, stop_sequences=["```"])
    return json.loads(eval_text)


def run_test_case(test_case):
    """Calls run_prompt and grades the result with a model-based grader."""
    output = run_prompt(test_case)
    model_grade = grade_by_model(test_case, output)
    model_score = model_grade["score"]
    code_score = grade_by_code(test_case, output)
    return {
        "output": output,
        "test_case": test_case,
        "score": (model_score + code_score) / 2,
        "reasoning": model_grade["reasoning"],
    }


def run_eval(dataset):
    """Runs run_test_case on each item of the dataset, prints the average score, and returns the list of results."""
    results = [run_test_case(test_case) for test_case in dataset]
    average_score = mean(result["score"] for result in results)
    print(f"Average score: {average_score}")
    return results
