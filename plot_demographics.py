import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


prescreening_df = pd.read_excel('CaveCrystalQuest-Analysis/questionnaire/PreScreening_Questionnaire(1-14).xlsx')
prescreening_df = prescreening_df[1:] # exclude participant 3


sex_counts = prescreening_df['Sex at birth'].value_counts()
plt.bar(sex_counts.index, sex_counts.values)
plt.title("Gender Distribution")
plt.show()

age = prescreening_df["Age"]
print(f'M = {round(age.mean(),2)}, SD = {round(age.std(),2)}, n = {len(age)}')
sns.histplot(data=prescreening_df, x="Age",binwidth=1,kde=True)
plt.title("Age Distribution")
plt.show()
