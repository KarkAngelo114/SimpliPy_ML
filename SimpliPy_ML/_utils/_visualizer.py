from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def Visualize(actual_label_list, predicted_label_list, class_names, prediction_score_list, labels):
    # confusion matrix
    cm = confusion_matrix(actual_label_list, predicted_label_list)

    # Plot confusion matrix
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap="Blues",
                xticklabels=[name.replace("_", " ") for name in class_names],
                yticklabels=[name.replace("_", " ") for name in class_names])

    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.show()

    # ROC Curve + AUC Score
    fpr, tpr, _ = roc_curve(actual_label_list, prediction_score_list)
    auc = roc_auc_score(actual_label_list, prediction_score_list)

    plt.figure(figsize=(6, 4))
    plt.plot(fpr, tpr, label=f"AUC = {auc:.2f}")
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("AUC Curve")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Step 1: Define label names (adjust as needed).
    with open(labels, "r") as f:
        raw_class_names = [line.strip() for line in f.readlines()]

    label_names = [name.replace("_", " ") for name in raw_class_names]
    num_classes = len(label_names)


    # Step 2: Initialize counters
    correct_counts = [0] * num_classes
    incorrect_counts = [0] * num_classes

    # Step 3: Count correct vs incorrect predictions per class
    for true, pred in zip(actual_label_list, predicted_label_list):
        if true == pred:
            correct_counts[true] += 1
        else:
            incorrect_counts[true] += 1

    # Step 4: Create a dataframe for plotting
    df = pd.DataFrame({
        "Label": label_names,
        "Correct": correct_counts,
        "Incorrect": incorrect_counts
    })

    # Step 5: Plot bar chart
    df.set_index("Label").plot(
        kind="bar",
        stacked=True,
        color=["green", "red"]
    )

    plt.title("Correct vs Incorrect Predictions per Class")
    plt.ylabel("Number of Images")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
