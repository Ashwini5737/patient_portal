import torch
from PIL import Image
import os
import pandas as pd
from torchvision import transforms

# Device setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the dataset for labels
DATA_ENTRY_PATH = "D:\\Downloads\\Databases\\Microsoft Fabric\\microsoft_fabric_hackathon\\Data_Entry_2017.csv"
data_entry = pd.read_csv(DATA_ENTRY_PATH)
all_labels = sorted(set(label for sublist in data_entry['Finding Labels'].str.split('|') for label in sublist))

# Load model
def load_xray_model(model_path="D:\\Downloads\\Databases\\Microsoft Fabric\\microsoft_fabric_hackathon\\best_model.pth"):
    model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet50', pretrained=False)
    model.fc = torch.nn.Sequential(
        torch.nn.Linear(model.fc.in_features, len(all_labels)),
        torch.nn.Sigmoid()
    )
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def analyze_xray(image_path, model):
    """ Analyzes an X-ray image and returns the classification result. """
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        probs, classes = torch.max(outputs, dim=1)
        predicted_class = all_labels[classes.item()]
        predicted_prob = torch.sigmoid(probs).item()

    return f"Predicted Condition: {predicted_class} with probability {predicted_prob:.2%}"

# Load model globally to avoid redundant loading
xray_model = load_xray_model()
