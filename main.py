from pulp import *
import numpy as np
import pandas as pd

from  schedule_out import *
from prob_groups import *
from prob_teachers import *
from prob_auds import *
from prob_targets import *



build_constraits_for_groups()
build_constraits_for_teachers()
build_constraits_for_auds()
build_targets()



prob += tgt1 >= 0.95 * classes_overall


prob += -0.35 * tgt2 / (len(all_groups) * 6) - 0.1 * tgt3 / (len(all_groups) * 6) - 0.2 * tgt4 / (len(all_groups) * 6) - 0.15* tgt5 / len(all_groups) - 0.2 * tgt6 / electives_overall_for_students


prob.solve(PULP_CBC_CMD(msg=1, timeLimit = 60 * 60, threads=12))

print(prob.status)


if (prob.objective is not None):
    print("Значение целевой функции:", prob.objective.value())

prob_res = prob.variablesDict()
write_res_for_teachers(prob_res)
write_res_for_groups(prob_res)

