
# Plant Identification System

## Overview

The Plant Identification System is a smart web-based application that uses AI to identify plant species and provide information about medicinal properties, nutrition, and cultivation. Users can upload or capture plant images, and the system displays accurate identification results along with detailed plant information.

The project also includes a bilingual chatbot in English and Tamil to answer user queries related to plant care, medicinal uses, and environmental requirements.

---

## ⚙️Technologies Used

* Front-End: HTML, CSS, JavaScript, Bootstrap
* Back-End: Python, Django
* Database: SQLite
* AI & Image Processing: Pre-trained Model
* NLP & Chatbot: NLP

---

## 📌Features

* AI-based plant identification
* Real-time image processing
* Medicinal and cultivation information
* Bilingual chatbot support
* Responsive web interface
* Secure and scalable backend

---

## Workflow

1. User uploads or captures a plant image.
2. Image preprocessing is performed.
3. AI model predicts the plant species.
4. Database retrieves plant details.
5. Results are displayed to the user.
6. Chatbot provides additional assistance.

---

## Installation

1. Install Python and Django.
2. Clone the project repository.
3. Install required packages using:

   ```bash
   pip install -r requirements.txt
   ```
4. Run database migrations:

   ```bash
   python manage.py migrate
   ```
5. Start the Django server:

   ```bash
   python manage.py runserver
   ```
6. Open the browser and visit:

   ```bash
   http://127.0.0.1:8000/
   ```

---

## Conclusion

The system combines AI, image processing, database management, and NLP to provide accurate plant identification and useful plant-related information through an interactive and user-friendly platform.
