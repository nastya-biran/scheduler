import numpy as np
import pandas as pd

teachers_data = pd.read_csv("Teachers_small.csv")
groups_data = pd.read_csv("Groups_small.csv")
auds_data = pd.read_csv("Classrooms_small.csv")
electives_data = pd.read_csv("Electives_small.csv")


all_slots = ['9:30-10:50', '11:10-12:30', '13:00-14:20', '14:40-16:00', '16:20-17:40', '18:10-19:30']
all_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
all_subjects = list(groups_data.columns.values)[2:-3]
all_teachers = list(pd.unique(teachers_data["Преподаватель"]))
all_auds = list(pd.unique(auds_data["Аудитория"]))
all_electives = list(pd.unique(electives_data.columns[1:]))
all_base = list(set(all_subjects) - set(all_electives))
all_electives_ind = sorted([int(all_subjects.index(subject)) for subject in all_electives])
all_base_ind = sorted([int(all_subjects.index(subject)) for subject in all_base])
all_groups = list(pd.unique(groups_data[groups_data["Номер группы"] != "Отдельные требования для предмета"]["Номер группы"]))

print(all_subjects)
print(all_teachers)
print(all_groups)
print(all_auds)
print(all_electives)
print(all_base)

aud_reqs_data = groups_data[groups_data["Номер группы"] == "Отдельные требования для предмета"].iloc[0]
aud_reqs = []
for j in range(len(all_subjects)):
  req = aud_reqs_data[all_subjects[j]]
  aud_reqs.append(req)


groups_data = groups_data[groups_data["Номер группы"] != "Отдельные требования для предмета"]
groups_data.iloc[:, 2 : -3] = groups_data.iloc[:, 2 : -3].astype('int32')
electives_data.iloc[:, 0] = electives_data.iloc[:, 0].astype('str')
