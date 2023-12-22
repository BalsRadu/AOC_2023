"""
The Elves of Gear Island are thankful for your help and send you on your way. They even have a hang glider that someone stole from Desert Island; since you're already going that direction, it would help them a lot if you would use it to get down there and return it to them.

As you reach the bottom of the relentless avalanche of machine parts, you discover that they're already forming a formidable heap. Don't worry, though - a group of Elves is already here organizing the parts, and they have a system.

To start, each part is rated in each of four categories:

x: Extremely cool looking
m: Musical (it makes a noise when you hit it)
a: Aerodynamic
s: Shiny
Then, each part is sent through a series of workflows that will ultimately accept or reject the part. Each workflow has a name and contains a list of rules; each rule specifies a condition and where to send the part if the condition is true. The first rule that matches the part being considered is applied immediately, and the part moves on to the destination described by the rule. (The last rule in each workflow has no condition and always applies if reached.)

Consider the workflow ex{x>10:one,m<20:two,a>30:R,A}. This workflow is named ex and contains four rules. If workflow ex were considering a specific part, it would perform the following steps in order:

Rule "x>10:one": If the part's x is more than 10, send the part to the workflow named one.
Rule "m<20:two": Otherwise, if the part's m is less than 20, send the part to the workflow named two.
Rule "a>30:R": Otherwise, if the part's a is more than 30, the part is immediately rejected (R).
Rule "A": Otherwise, because no other rules matched the part, the part is immediately accepted (A).
If a part is sent to another workflow, it immediately switches to the start of that workflow instead and never returns. If a part is accepted (sent to A) or rejected (sent to R), the part immediately stops any further processing.

The system works, but it's not keeping up with the torrent of weird metal shapes. The Elves ask if you can help sort a few parts and give you the list of workflows and some part ratings (your puzzle input). For example:

px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
The workflows are listed first, followed by a blank line, then the ratings of the parts the Elves would like you to sort. All parts begin in the workflow named in. In this example, the five listed parts go through the following workflows:

{x=787,m=2655,a=1222,s=2876}: in -> qqz -> qs -> lnx -> A
{x=1679,m=44,a=2067,s=496}: in -> px -> rfg -> gd -> R
{x=2036,m=264,a=79,s=2244}: in -> qqz -> hdj -> pv -> A
{x=2461,m=1339,a=466,s=291}: in -> px -> qkq -> crn -> R
{x=2127,m=1623,a=2188,s=1013}: in -> px -> rfg -> A
Ultimately, three parts are accepted. Adding up the x, m, a, and s rating for each of the accepted parts gives 7540 for the part with x=787, 4623 for the part with x=2036, and 6951 for the part with x=2127. Adding all of the ratings for all of the accepted parts gives the sum total of 19114.

Sort through all of the parts you've been given; what do you get if you add together all of the rating numbers for all of the parts that ultimately get accepted?

Your puzzle answer was 446517.

--- Part Two ---
Even with your help, the sorting process still isn't fast enough.

One of the Elves comes up with a new plan: rather than sort parts individually through all of these workflows, maybe you can figure out in advance which combinations of ratings will be accepted or rejected.

Each of the four ratings (x, m, a, s) can have an integer value ranging from a minimum of 1 to a maximum of 4000. Of all possible distinct combinations of ratings, your job is to figure out which ones will be accepted.

In the above example, there are 167409079868000 distinct combinations of ratings that will be accepted.

Consider only your list of workflows; the list of part ratings that the Elves wanted you to sort is no longer relevant. How many distinct combinations of ratings will be accepted by the Elves' workflows?

Your puzzle answer was 130090458884662.
"""

import re

def parse_workflows(content):
    """
    Parses the workflows from the provided content and returns a dictionary where each key is a workflow name
    and each value is a list of tuples representing the rules in the workflow.
    """
    workflows = {}
    parts = []
    parsing_workflows = True

    for line in content.splitlines():
        if line.strip() == "":
            parsing_workflows = False
            continue

        if parsing_workflows:
            # Extract workflow name and rules
            workflow_name, rules_str = line.split("{", 1)
            rules = []
            for rule_str in rules_str[:-1].split(","):
                # Parse condition and destination
                if ":" in rule_str:
                    condition, destination = rule_str.split(":", 1)
                    rules.append((condition, destination))
                else:
                    # Final rule without a condition
                    rules.append((None, rule_str))
            workflows[workflow_name] = rules
        else:
            # Parse part ratings
            ratings = dict(re.findall(r'(\w)=(\d+)', line))
            parts.append({k: int(v) for k, v in ratings.items()})

    return workflows, parts

def evaluate_condition(condition, part_ratings):
    """
    Evaluates the condition against the part's ratings.
    """
    if condition is None:
        return True  # No condition means always true
    match = re.match(r'(\w)([<>])(\d+)', condition)
    if match:
        attribute, operator, value = match.groups()
        value = int(value)
        if attribute in part_ratings:
            if operator == '>':
                return part_ratings[attribute] > value
            elif operator == '<':
                return part_ratings[attribute] < value
    return False

def process_part_through_workflows(part, workflows):
    """
    Processes a part through the workflows starting from the 'in' workflow.
    """
    current_workflow = 'in'
    while True:
        for condition, destination in workflows[current_workflow]:
            if evaluate_condition(condition, part):
                if destination == 'A':
                    return True, sum(part.values())  # Part accepted
                elif destination == 'R':
                    return False, 0  # Part rejected
                else:
                    current_workflow = destination  # Move to the next workflow
                    break  # Break the for loop and continue while loop with the new workflow

def generate_intervals(workflow_name, workflows, path_conditions=[], negated_conditions=[]):
    """
    Recursively generates intervals for each path in the workflow that leads to acceptance ('A').
    This function also considers the negation of conditions for the paths not taken.
    """
    intervals = []

    # Get the list of all next steps in the workflow
    next_steps = workflows[workflow_name]

    for i, (condition, destination) in enumerate(next_steps):
        new_path_conditions = path_conditions.copy()
        new_negated_conditions = negated_conditions.copy()

        # Add the current condition to the path
        if condition:
            new_path_conditions.append(condition)

            # Add the negation of other conditions not taken in this path
        for j, (other_condition, _) in enumerate(next_steps):
            if j < i and other_condition:
                # Negate the other condition
                attribute, operator, value = re.match(r'(\w)([<>])(\d+)', other_condition).groups()
                negated_operator = '<' if operator == '>' else '>'
                negated_value = str(int(value) + 1) if operator == '>' else str(int(value) - 1)
                negated_condition = f"{attribute}{negated_operator}{negated_value}"
                new_negated_conditions.append(negated_condition)

        if destination == 'A':
            # Convert path conditions to interval, considering negated conditions as well
            interval = {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000]}
            valid = True
            for cond in new_path_conditions + new_negated_conditions:
                attribute, operator, value = re.match(r'(\w)([<>])(\d+)', cond).groups()
                value = int(value)
                if operator == '>':
                    interval[attribute][0] = max(interval[attribute][0], value + 1)
                elif operator == '<':
                    interval[attribute][1] = min(interval[attribute][1], value - 1)
                if interval[attribute][0] > interval[attribute][1]:
                    valid = False
                    break
            if valid:
                intervals.append(interval)
        elif destination != 'R':
            # Continue exploring the workflow with the updated conditions
            intervals.extend(generate_intervals(destination, workflows, new_path_conditions, new_negated_conditions))

    return intervals


def count_combinations_in_intervals(intervals):
    """
    Counts the number of combinations for each interval.
    """
    total_combinations = 0

    for interval in intervals:
        combinations = 1
        for attr in ['x', 'm', 'a', 's']:
            lower, upper = interval[attr]
            combinations *= max(0, upper - lower + 1)
        total_combinations += combinations

    return total_combinations


with open("input.txt") as f:
    content = f.read()
    # Parse the content of the file
    workflows, parts = parse_workflows(content)

    # Re-process each part through the workflows
    total_ratings = 0
    for part in parts:
        accepted, ratings_sum = process_part_through_workflows(part, workflows)
        if accepted:
            total_ratings += ratings_sum


    # Generate intervals for the 'in' workflow which is the starting point
    intervals = generate_intervals('in', workflows)

    # Count the combinations in these intervals
    total_combinations_intervals = count_combinations_in_intervals(intervals)

    print("First puzzle solution:", total_ratings)
    print("Second puzzle solution:", total_combinations_intervals)
