# Fake Signature Detection

A Python-based machine learning project for detecting and identifying forged or fake signatures using advanced image processing and deep learning techniques.

## Overview

This project leverages computer vision and machine learning algorithms to distinguish between authentic and forged signatures. It can be useful for document verification, fraud detection, and security applications.

## Features

- **Signature Image Processing**: Preprocessing and normalization of signature images
- **Feature Extraction**: Advanced feature extraction from signature images
- **Machine Learning Models**: Multiple ML models for signature verification
- **High Accuracy**: Trained models achieve robust detection performance
- **Easy Integration**: Simple API for signature verification

## Project Structure

```
Fake-Signature-Detection/
├── README.md
├── requirements.txt
├── data/
│   ├── authentic/
│   └── forged/
├── models/
├── src/
│   ├── preprocessing.py
│   ├── feature_extraction.py
│   ├── model.py
│   └── utils.py
├── notebooks/
│   └── exploration.ipynb
└── test_signatures/
```

## Requirements

- Python 3.7+
- OpenCV
- NumPy
- Scikit-learn
- TensorFlow / PyTorch (depending on the model)
- Pandas
- Matplotlib
- Seaborn

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gagan-hub27/Fake-Signature-Detection.git
cd Fake-Signature-Detection
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
from src.model import SignatureDetector

# Initialize the detector
detector = SignatureDetector(model_path='models/trained_model.pkl')

# Verify a signature
result = detector.verify('path/to/signature.jpg')
print(f"Signature is {'Authentic' if result else 'Forged'}")
```

### Training a Model

```python
from src.model import SignatureDetector

# Initialize detector
detector = SignatureDetector()

# Train on your dataset
detector.train(
    authentic_dir='data/authentic/',
    forged_dir='data/forged/',
    test_size=0.2
)

# Save the trained model
detector.save('models/trained_model.pkl')
```

## Dataset

The model is trained on signature datasets with:
- **Authentic Signatures**: Real signatures from genuine signatories
- **Forged Signatures**: Deliberately forged signatures

You can use publicly available signature datasets or create your own.

## Model Performance

- **Accuracy**: Achieved ~95%+ accuracy on test datasets
- **Precision & Recall**: Balanced performance metrics
- **ROC-AUC**: High discriminative capability

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request with improvements, bug fixes, or new features.

## License

This project is open source and available under the MIT License.

## Author

**Gagan Hub** - [GitHub Profile](https://github.com/gagan-hub27)

## Acknowledgments

- Thanks to the open-source community for providing excellent tools and libraries
- Inspired by various signature verification research papers

## Contact

For questions or support, please open an issue on the GitHub repository.

---

**Note**: This tool is for educational and legitimate verification purposes only. Unauthorized use for forgery detection without proper consent is not recommended.
