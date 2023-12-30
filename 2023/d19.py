import utils

sample = utils.Utilities.get_lines_from_file_including_space("sample/d19sample.txt")
full = utils.Utilities.get_lines_from_file_including_space("d19.txt")

ACCEPT = "A"
REJECT = "R"
LOWER = "<"
GREATER = ">"
FINAL_STATES = [ACCEPT, REJECT]

START_RANGES = {
    'x': (1, 4000),
    'm': (1, 4000),
    'a': (1, 4000),
    's': (1, 4000)
}


class Rating:
    def __repr__(self):
        return ("Rating(expression={})"
                .format(self.expression))

    def __init__(self, variable, value, expression):
        self.variable = variable
        self.value = value
        self.expression = expression


class Rule:
    variable = None
    condition = False
    outcome = None

    def __repr__(self):
        return ("Rule(cond={}, outcome={})"
                .format(self.condition, self.outcome))

    def __init__(self, full_rule):
        self.full_rule = full_rule
        self.process_rule()

    def get_outcome(self):
        return self.outcome

    def process_rule(self):
        parts = self.full_rule.split(":")
        has_separator = len(parts) > 1
        if has_separator:
            self.outcome = parts[1]
            self.condition = parts[0]
            self.variable = self.condition[0]
        else:
            self.outcome = parts[0]

    def evaluate_rule(self, variable, value):
        if variable in self.condition:
            if GREATER in self.condition:
                return value > int(self.condition.split(GREATER)[1])
            else:
                return value < int(self.condition.split("<")[1])
        else:
            return False


def parse_input(lines):
    workflows = []
    ratings = []
    read_ratings = False
    for line in lines:
        if line == "":
            read_ratings = True
            continue

        if read_ratings:
            ratings.append(line)
        else:
            workflows.append(line)

    return workflows, ratings


def build_workflows(workflows):
    d_workflows = {}
    for workflow in workflows:
        workflow_rules_index = workflow.find("{")
        w = workflow[:workflow_rules_index]
        rules = workflow[workflow_rules_index + 1:-1].split(",")
        processed_rules = [Rule(r) for r in rules]
        d_workflows[w] = processed_rules
    return d_workflows


def process_result(accepted_ratings):
    values = []
    for g in accepted_ratings:
        for r in g.values():
            values.append(int(r.value))
    return sum(values)

def calculate_ranges_product(ranges):
    product = 1
    for start, end in ranges.values():
        product *= end - start + 1
    return product


def parse_rules(workflow):
    rule_parts = []
    for rule in workflow[:-1]:
        if LOWER in rule.condition:
            ps = rule.condition.split(LOWER)
            rule_parts.append((ps[0], LOWER, int(ps[1]), rule.outcome))
        else:
            ps = rule.condition.split(GREATER)
            rule_parts.append((ps[0], GREATER, int(ps[1]), rule.outcome))
    default = workflow[-1].outcome

    return rule_parts, default


def get_accepted_combinations(d_workflows, ranges, wf_name):
    if wf_name == REJECT:
        return 0
    if wf_name == ACCEPT:
        return calculate_ranges_product(ranges)

    rules, default = parse_rules(d_workflows[wf_name])

    total = 0
    for var, symb, num, target in rules:
        start, end = ranges[var]
        if symb == "<":
            rule_true_range = (start, num-1)
            rule_false_range = (num, end)
        else:
            rule_true_range = (num + 1, end)
            rule_false_range = (start, num)

        if rule_true_range[0] <= rule_true_range[1]:
            ranges_copy = dict(ranges)
            ranges_copy[var] = rule_true_range
            total += get_accepted_combinations(d_workflows, ranges_copy, target)

        if rule_false_range[0] <= rule_false_range[1]:
            ranges = dict(ranges)
            ranges[var] = rule_false_range

    total += get_accepted_combinations(d_workflows, ranges, default)
    return total


def solve(lines, part2=False):
    workflows, ratings = parse_input(lines)
    d_workflows = build_workflows(workflows)
    processed_ratings = []
    for rating in ratings:
        groups = [g.lstrip("{").rstrip("}") for g in rating.split(",")]
        rating_group = {rg.variable: rg for rg in [Rating(r.split("=")[0], int(r.split("=")[1]), r) for r in groups]}
        processed_ratings.append(rating_group)

    if not part2:
        accepted_ratings = []
        last_rating_checked = None
        for pr_group in processed_ratings:
            current_outcome = "in"
            while current_outcome not in FINAL_STATES:
                rules_to_check = d_workflows[current_outcome]
                for rule in rules_to_check:
                    if rule.variable in pr_group.keys():
                        rating = pr_group[rule.variable]
                        if rule.evaluate_rule(rating.variable, rating.value):
                            current_outcome = rule.get_outcome()
                            last_rating_checked = pr_group
                            break
                    elif not rule.variable:
                        current_outcome = rule.get_outcome()
                        break

            if current_outcome == "A":
                accepted_ratings.append(last_rating_checked)

        return process_result(accepted_ratings)
    else:
        return get_accepted_combinations(d_workflows, START_RANGES, "in")


if __name__ == '__main__':
    print(solve(sample))
    print(solve(full))
    print(solve(full, part2=True))
