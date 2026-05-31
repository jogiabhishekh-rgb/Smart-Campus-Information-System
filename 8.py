import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    df = pd.read_csv("student_performance.csv")

    print(df.head())

    print("\nStatistical Summary")
    print(df.describe())

    scores = df[["Math", "Science", "English"]].to_numpy()

    print("\nMean:", np.mean(scores, axis=0))
    print("Median:", np.median(scores, axis=0))
    print("Std Dev:", np.std(scores, axis=0))

    subjects = ["Math", "Science", "English"]
    mean_scores = np.mean(scores, axis=0)

    plt.bar(subjects, mean_scores)
    plt.title("Average Scores")
    plt.show()

    df.plot(x="Name", y=["Math", "Science", "English"], kind="bar")
    plt.title("Student Performance")
    plt.show()

except FileNotFoundError:
    print("CSV file not found.")