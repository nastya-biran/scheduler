from pulp import *
import numpy as np
import pandas as pd
from  schedule_functions import *

M = 1e5

prob = LpProblem("schedule", LpMaximize)

attends = LpVariable.dicts("x", ((i, j, k, l, m)
                                  for i in range(len(all_groups))
                                  for j in range(len(all_subjects))
                                  for k in range(len(all_teachers))
                                  for l in range(len(all_days))
                                  for m in range(len(all_slots))),
                            cat="Binary")

online = LpVariable.dicts("online", ((i, l, m)
                    for i in range(len(all_groups))
                    for l in range(len(all_days))
                    for m in range(len(all_slots))),
               cat="Binary")

group_has_class = LpVariable.dicts("gr_h_cl", ((i, l, m)
                    for i in range(len(all_groups))
                    for l in range(len(all_days))
                    for m in range(len(all_slots))),
               cat="Binary")

teacher_has_class = LpVariable.dicts("teacher_has_class", ((j, k, l, m)
                    for j in range(len(all_subjects))
                    for k in range(len(all_teachers))
                    for l in range(len(all_days))
                    for m in range(len(all_slots))),
               cat="Binary")

is_teacher_for_this_subject_and_group = LpVariable.dicts("is_teacher_for_this_subject_and_group", ((i, j, k)
                    for i in range(len(all_groups))
                    for j in range(len(all_subjects))
                    for k in range(len(all_teachers))),
               cat="Binary")

teacher_has_classes_for_day = LpVariable.dicts("teacher_has_classes_for_day", ((k, l)
                    for k in range(len(all_teachers))
                    for l in range(len(all_days))),
               cat="Binary")

a = LpVariable.dicts("a", ((j, k, l, m, q)
                    for j in range(len(all_subjects))
                    for k in range(len(all_teachers))
                    for l in range(len(all_days))
                    for m in range(len(all_slots))
                    for q in range(len(all_auds))),
               cat="Binary")

teacher_classes_overall = LpVariable("teach_class_ov", 
                  cat="Integer")

w1 = LpVariable.dicts("w1", ((i, l, m)
                    for i in range(len(all_groups))
                    for l in range(len(all_days))
                    for m in range(len(all_slots))),
               cat="Binary")
w2 = LpVariable.dicts("w2", ((i, l, m)
                    for i in range(len(all_groups))
                    for l in range(len(all_days))
                    for m in range(len(all_slots))),
               cat="Binary")

windows = LpVariable.dicts("windows", ((i, l)
                    for i in range(len(all_groups))
                    for l in range(len(all_days))),
               cat="Integer")

classes_per_day = LpVariable.dicts("cl_day", ((i, l)
                    for i in range(len(all_groups))
                    for l in range(len(all_days))),
               cat="Integer")

has_classes = LpVariable.dicts("has_cl", ((i, l)
                    for i in range(len(all_groups))
                    for l in range(len(all_days))),
               cat="Binary")

online_classes_per_day = LpVariable.dicts("on_cl_day", ((i, l)
                    for i in range(len(all_groups))
                    for l in range(len(all_days))),
               cat="Integer")


has_online_classes = LpVariable.dicts("has_on_cl", ((i, l)
                    for i in range(len(all_groups))
                    for l in range(len(all_days))),
               cat="Binary")

group_has_elective = LpVariable.dicts("gr_h_el", ((i, l, m)
                        for i in range(len(all_groups))
                        for l in range(len(all_days))
                        for m in range(len(all_slots))),
                cat="Binary")

tgt1 = LpVariable("tgt1", 
                  cat="Integer")

tgt2 = LpVariable("tgt2", 
                  cat="Integer")

tgt3 = LpVariable("tgt3", 
                  cat="Integer")

tgt4 = LpVariable("tgt4", 
                  cat="Integer")

tgt5 = LpVariable("tgt5", 
                  cat="Integer")

tgt6 = LpVariable("tgt6", 
                  cat="Integer")

def initialise_group_has_class(prob):
    for i in range(len(all_groups)):
        for l in range(len(all_days)):
            for m in range(len(all_slots)):
                prob+= lpSum([attends[(i, j, k, l, m)]
                            for j in range(len(all_subjects))
                            for k in range(len(all_teachers))]) <= M * group_has_class[(i, l, m)]


def initialise_teacher_has_classes_for_day(prob):
    for k in range(len(all_teachers)):
        for l in range(len(all_days)):
            prob += M * teacher_has_classes_for_day[(k, l)] >= lpSum([teacher_has_class[(j, k, l, m)]
                                            for j in range(len(all_subjects))
                                            for m in range(len(all_slots))])
            prob += teacher_has_classes_for_day[(k, l)] <= lpSum([teacher_has_class[(j, k, l, m)]
                                            for j in range(len(all_subjects))
                                            for m in range(len(all_slots))])

def initialise_teacher_has_class(prob):
    for j in range(len(all_subjects)):
        for k in range(len(all_teachers)):
            for l in range(len(all_days)):
                for m in range(len(all_slots)):
                    prob += M * teacher_has_class[(j, k, l, m)] >= lpSum([attends[(i, j, k, l, m)]
                                                    for i in range(len(all_groups))])
                    prob += teacher_has_class[(j, k, l, m)] <= lpSum([attends[(i, j, k, l, m)]
                                                    for i in range(len(all_groups))])


def initialise_is_teacher_for_this_subject_and_group(prob):
    for i in range(len(all_groups)):
        for j in range(len(all_subjects)):
            for k in range(len(all_teachers)):
                prob += M * is_teacher_for_this_subject_and_group[(i, j, k)] >= lpSum([attends[(i, j, k, l, m)]
                                                    for l in range(len(all_days))
                                                    for m in range(len(all_slots))])


def initialise_online(prob):
    for i in range(len(all_groups)):
        for l in range(len(all_days)):
            for m in range(len(all_slots)):
                prob +=  lpSum([attends[(i, j, k, l, m)] * (get_format(all_teachers[k], all_subjects[j]) == "Онлайн")
                            for j in get_subjects_by_group(all_groups[i])
                            for k in get_teachers_by_subject(all_subjects[j])]) == online[(i, l, m)]
def initialise_online_classes_per_day(prob):
    initialise_online(prob)
    for i in range(len(all_groups)):
        for l in range(len(all_days)):
            prob += lpSum([online[(i, l, m)]
                                for m in range(len(all_slots))]) == online_classes_per_day[(i, l)]


def initialise_has_online_classes(prob):
    initialise_online_classes_per_day(prob)
    for i in range(len(all_groups)):
        for l in range(len(all_days)):
            prob += M * has_online_classes[(i, l)] >= online_classes_per_day[(i, l)]
            prob += has_online_classes[(i, l)] <= online_classes_per_day[(i, l)]


def initialise_first_and_last_class_for_day(prob):
    for i in range(len(all_groups)):
        for l in range(len(all_days)):
            prob += lpSum([w1[(i, l, m1)]
                        for m1 in range(len(all_slots))]) <= 1
            prob += lpSum([w2[(i, l, m1)]
                        for m1 in range(len(all_slots))]) <= 1
            for m in range(len(all_slots)):
                prob += w1[(i, l, m)] <= group_has_class[(i, l, m)]
                prob += lpSum([w1[(i, l, m1)]
                            for m1 in range(m + 1)]) >= group_has_class[(i, l, m)]      
                prob += w2[(i, l, m)] <= group_has_class[(i, l, m)]
                prob += lpSum([w2[(i, l, m1)]
                            for m1 in range(m, len(all_slots))]) >= group_has_class[(i, l, m)]


def initialise_classes_per_day(prob):
    for i in range(len(all_groups)):
        for l in range(len(all_days)):
            prob+= lpSum([group_has_class[(i, l, m)]
                            for m in range(len(all_slots))]) == classes_per_day[(i, l)]


def initialise_has_classes(prob):
    initialise_classes_per_day(prob)
    for i in range(len(all_groups)):
        for l in range(len(all_days)):
            prob += M * has_classes[(i, l)] >= classes_per_day[(i, l)]
            prob += has_classes[(i, l)] <= classes_per_day[(i, l)]


def initialise_windows(prob):
    initialise_first_and_last_class_for_day(prob)
    initialise_has_classes(prob)
    for i in range(len(all_groups)):
        for l in range(len(all_days)):
            prob += lpSum([w2[(i, l, m)] * m
                            for m in range(len(all_slots))])- lpSum([w1[(i, l, m)] * m
                                                                for m in range(len(all_slots))]) - classes_per_day[(i, l)] + has_classes[(i, l)] == windows[(i, l)]

def initialise_group_has_elective(prob):
    for i in range(len(all_groups)):
        for l in range(len(all_days)):
            for m in range(len(all_slots)):
                prob+= lpSum([attends[(i, j, k, l, m)]
                            for j in all_electives_ind
                            for k in range(len(all_teachers))]) <= M * group_has_elective[(i, l, m)]


