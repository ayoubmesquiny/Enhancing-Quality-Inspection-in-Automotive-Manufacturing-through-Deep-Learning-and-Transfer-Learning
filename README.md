# Enhancing Quality Inspection in Automotive Manufacturing through Deep Learning and Transfer Learning

## Overview

Ensuring quality control and accurate defect detection are critical in the automotive manufacturing industry. This project introduces a deep learning-based approach leveraging transfer learning to automate defect detection process for Terminal Crimp Cross-Section.

---

## Key Features

1. Utilizes pre-trained Convolutional Neural Networks (CNNs) such as DenseNet121, VGG19, and others.

2. Implements transfer learning to address limited labeled datasets.

3. Achieves high accuracy (>98%) in defect detection and classification.

4. Deploys models in a real-time production environment with a user-friendly GUI for the Quality team.

---

## Repository Contents

  **src**: Scripts for preprocessing, training, and evaluating the CNN models.

  **app**: A user-friendly interface for real-time deployment in production environments.

  **Documentation**: Detailed descriptions of the methods, metrics, and experimental setup.

  **Sample Data**: Example datasets for terminal crimp cross-sections (restricted due to proprietary limitations).

---

## Requirements

### Hardware

  **Machine 1:** Ubuntu 22, 16 CPUs, 16 GB RAM, 100 GB Disk, Azure-based.

  **Machine 2:** Debian 11, 8 CPUs, 15 GB RAM, 140 GB Disk, On-premise server.

### Software

  **Python Libraries:** TensorFlow, Keras, scikit-learn, seaborn, and other dependencies listed in ```requirements.txt```.

---

## Installation

### Clone the repository:
```bash
git clone https://github.com/your-username/quality-inspection-automotive.git
cd quality-inspection-automotive
```

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Launch the Streamlit application:
```bash
streamlit run your_script.py
```

---

## Future Work

Incorporating object detection models (R-CNN, YOLO) for precise defect localization.

Expanding datasets to cover additional manufacturing applications.

Enhancing model interpretability for better insights into defect classification.
