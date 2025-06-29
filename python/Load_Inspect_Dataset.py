import pandas as pd

# Load CSVs
students = pd.read_csv('../data/student.csv')
grades = pd.read_csv('../data/grades.csv')
attendance = pd.read_csv('../data/attendance.csv')

# Quick check
print('students file:\n', students.head())
print('grades file:\n', grades.head())
print('attendance file:\n', attendance.head())

# Fill missing values
grades['grade'] = grades['grade'].fillna(grades['grade'].mean())
attendance['status'] = attendance['status'].fillna('Absent')

# Convert dates
students['enrollment_date'] = pd.to_datetime(students['enrollment_date'])
attendance['date'] = pd.to_datetime(attendance['date'])

# Drop duplicates
students.drop_duplicates(inplace=True)
grades.drop_duplicates(inplace=True)
attendance.drop_duplicates(inplace=True)

# Data Modeling
# Average grade per student
avg_grades = grades.groupby('student_id')['grade'].mean().reset_index()
avg_grades.rename(columns={'grade': 'avg_grade'}, inplace=True)

# Absence count per student
absences = attendance[attendance['status'] == 'Absent']
absence_counts = absences.groupby('student_id').size().reset_index(name='total_absences')

# Merge
student_model = students.merge(avg_grades, on='student_id', how='left')
student_model = student_model.merge(absence_counts, on='student_id', how='left')
student_model['total_absences'] = student_model['total_absences'].fillna(0)

# Risk flag
student_model['risk_flag'] = student_model.apply(
    lambda row: 'At Risk' if row['avg_grade'] < 65 and row['total_absences'] > 1 else 'OK',
    axis=1
)

# Export
student_model.to_csv('../data/student_summary.csv', index=False)
print('✅ Data exported to student_summary.csv')
