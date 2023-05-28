import numpy as np
import pandas as pd
from schedule_in import *


def get_subjects_by_teacher(teacher):
  teacher_data = teachers_data[teachers_data["Преподаватель"] == teacher].iloc[0]
  available_subjects = teacher_data["Дисциплина"]
  available_subjects_splitted = available_subjects.split(", ")
  types_of_classes = teacher_data["Тип занятий"]
  types_of_classes_splitted = types_of_classes.split(", ")
  available_subjects_full = []
  for subject in available_subjects_splitted:
    for class_type in types_of_classes_splitted:
      available_subjects_full.append(subject + ", " + class_type)
  subject_inds = [all_subjects.index(subject) for subject in available_subjects_full]
  return subject_inds

def get_groups_by_subject(subject):
  subject_data = groups_data[groups_data[subject] >= 1]
  available_groups = list(pd.unique(subject_data["Номер группы"]))
  group_inds = [all_groups.index(group) for group in available_groups]
  return group_inds

def get_answers(teacher):
  teacher_data = teachers_data[teachers_data["Преподаватель"] == teacher].iloc[0]
  answers = []
  for day in all_days:
    if pd.isna(teacher_data[day]):
      answers.append([None])
    else:
      slot_inds = [all_slots.index(slot) for slot in teacher_data[day].split(", ")]
      answers.append(slot_inds)
  return answers

def get_answers_unpref(teacher):
  answers = get_answers(teacher)
  unpref_answers = []
  for answer in answers:
    if None in answer:
      unpref_answers.append(range(len(all_slots)))
    else:
      unpref_answers.append(list(set(range(len(all_slots))) - set(answer)))
  return unpref_answers

def get_answers_for_auds(aud):
  aud_data = auds_data[auds_data["Аудитория"] == aud].iloc[0]
  answers = []
  for day in all_days:
    if pd.isna(aud_data[day]):
      answers.append(None)
    else:
      slot_inds = [all_slots.index(slot) for slot in aud_data[day].split(", ")]
      answers.append(slot_inds)
  return answers



def get_subjects_by_group(group):
  group_data = groups_data[groups_data["Номер группы"] == group]
  group_data = group_data.filter(all_subjects)
  group_data = group_data.dropna(axis=1, how="any")
  needed_subjects = list(group_data.where((group_data >= 1)).columns.values)
  subject_inds = [all_subjects.index(subject) for subject in needed_subjects]
  return subject_inds


def get_teachers_by_subject(subject):
  subject_and_type = subject.split(", ")
  subject_data = teachers_data[teachers_data["Дисциплина"].str.contains(subject_and_type[0], regex=False)]
  subject_data = subject_data[subject_data["Тип занятий"].str.contains(subject_and_type[1], regex=False)]
  available_teachers = list(pd.unique(subject_data["Преподаватель"]))
  teacher_inds = [all_teachers.index(teacher) for teacher in available_teachers]
  return teacher_inds

def get_classes_per_week_for_teacher(teacher):
  teacher_limits_data = teachers_data[teachers_data["Преподаватель"] == teacher].iloc[0]
  if pd.notna(teacher_limits_data["Нагрузка в неделю"]):
    classes_nums = teacher_limits_data["Нагрузка в неделю"].split("-")
  return int(classes_nums[0]), int(classes_nums[1])

def get_format(teacher, subject):
  teacher_data = teachers_data[teachers_data["Преподаватель"] == teacher].iloc[0]
  subject_and_type = subject.split(", ")
  if subject_and_type[0] in teacher_data["Дисциплина"] and subject_and_type[1] in teacher_data["Тип занятий"]:
    if "Лекции" in subject:
      return teacher_data["Формат лекций"]
    else:
      return teacher_data["Формат семинаров/практических занятий"]
  else:
    return "Преподаватель не ведет этот предмет"

def check_for_minor_and_military_day(group):
  group_data = groups_data[groups_data["Номер группы"] == group].iloc[0]
  has_minor = group_data["Майнор"]
  has_military_day = group_data["Военная кафедра"]
  return has_minor, has_military_day

def get_aud_capacity(aud):
  aud_data = auds_data[auds_data["Аудитория"] == aud].iloc[0]
  return aud_data["Вместимость"]

def get_group_size(group, subject):
  students = 0
  if subject in all_electives:
    group_data = electives_data[electives_data["Номер группы"] == group].iloc[0]
    students = group_data[subject]
  else:
    group_data = groups_data[groups_data["Номер группы"] == group].iloc[0]
    students = group_data["Количество студентов"]
  return students

def is_offline(teacher, subject):
  if get_format(teacher, subject) == "Очно":
    return 1
  else:
    return 0


def get_comp_auds():
  comp_auds_data = auds_data[auds_data["Тип"] == "Компьютерный класс"]
  comp_auds_names = comp_auds_data["Аудитория"].unique()
  inds = [all_auds.index(name) for name in  comp_auds_names]
  return inds


comp_auds = get_comp_auds()
not_comp_auds = list(set(range(len(all_auds))) - set(comp_auds))

def get_available_and_unavailable_auds(subject):
  available_auds = range(len(all_auds))
  unavailable_auds = []
  j = all_subjects.index(subject)
  if pd.notna(aud_reqs[j]) and "Компьютерный класс" in aud_reqs[j]:
    available_auds = comp_auds
    unavailable_auds = not_comp_auds
    #print(subject)
  elif "Семинары" in all_subjects[j]:
    available_auds = not_comp_auds
    unavailable_auds = comp_auds
  else:
    unavailable_auds = comp_auds
  return available_auds, unavailable_auds

def get_english_slots(group):
  group_data = groups_data[groups_data["Номер группы"] == group].iloc[0]
  english_slots = group_data["Слоты для английского"].split('; ')
  english_slots_separated = []
  for day_and_slots in english_slots:
    day = day_and_slots.split(': ')[0]
    ind_day = all_days.index(day)
    slots = day_and_slots.split(': ')[1].split(', ')
    ind_slots = [all_slots.index(slot) for slot in  slots]
    english_slots_separated.append([ind_day] + ind_slots)
  return english_slots_separated

def get_elective_seminar_by_elective_lecture(subject):
  subject_and_type = subject.split(", ")
  ind_lecture = all_subjects.index(subject)
  ind_seminar = all_subjects.index(subject_and_type[0] + ", Семинары")
  return [ind_lecture, ind_seminar]




pref_table = np.zeros((len(teachers_data), len(all_days), len(all_slots)))

for k, teacher in enumerate(all_teachers):
  available_subjects = get_subjects_by_teacher(teacher)
  available_slots = get_answers(teacher)
  for l, slots_for_day in enumerate(available_slots):
    if not(None in slots_for_day):
      for m in slots_for_day:
        pref_table[k, l, m] = 1

auds_free = np.ones((len(all_auds), len(all_days), len(all_slots)))

for q, aud in enumerate(all_auds):
  busy_slots = get_answers_for_auds(aud)
  for l, slots_for_day in enumerate(busy_slots):
    if slots_for_day is not None:
          for m in slots_for_day:
            auds_free[q, l, m] = 0

classes_overall = 0
electives_overall_for_students = 0
for i in range(len(all_groups)):
  needed_subjects = get_subjects_by_group(all_groups[i])
  group_data = groups_data[groups_data["Номер группы"] == all_groups[i]].iloc[0]
  for subject_ind in needed_subjects:
    if subject_ind in all_electives_ind:
      electives_overall_for_students += group_data[all_subjects[subject_ind]]
