import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
symptoms = pd.read_csv('"C:\MyPC\Datasets\Symptom\disease_symptom_dataset\Final_Augmented_dataset_Diseases_and_Symptoms.csv"')
symptoms_predictions = pd.read_csv('"C:\MyPC\Datasets\Symptom\disease_symptom_prediction\dataset.csv"')
symptoms_predictions_with_patients = pd.read_csv('"C:\MyPC\Datasets\Symptom\disease_symptom_patient_dataset\Disease_symptom_and_patient_profile_dataset.csv"')