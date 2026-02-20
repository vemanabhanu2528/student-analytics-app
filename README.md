# 📊 Student Performance Analytics Dashboard

A comprehensive web-based analytics platform for analyzing student performance data using Flask, Pandas, and Machine Learning. This application provides real-time insights, predictive analytics, and automated report generation.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 📈 Interactive Dashboard
- Real-time summary statistics (total students, average grades, pass rates)
- Visual grade distribution charts
- Performance category breakdowns
- Subject-wise analysis

### 🔍 Advanced Analytics
- Correlation analysis (attendance vs performance, study hours vs grades)
- Top performer rankings
- Subject-wise distribution analysis
- At-risk student identification

### 🤖 Machine Learning Predictions
- Grade prediction using Random Forest Regression
- Pass/Fail classification using Gradient Boosting
- Risk level assessment (High/Medium/Low)
- Feature importance analysis
- Model performance metrics (R², RMSE, Accuracy)

### 📄 Report Generation
- **Excel Reports**: Multi-sheet workbooks with formatted tables and summary statistics
- **PDF Reports**: Professional reports with charts, executive summaries, and detailed analytics
- One-click export functionality

### 📤 Data Management
- CSV/Excel file upload support
- Sample data generation for testing
- Data validation and preprocessing
- Support for custom datasets

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/student-analytics-app.git
cd student-analytics-app
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Access the dashboard**
Open your browser and navigate to: `http://localhost:5000`

## 📊 Data Format

The application expects CSV or Excel files with the following columns:

| Column | Description | Required |
|--------|-------------|----------|
| `student_id` | Unique student identifier | Yes |
| `name` | Student name | Yes |
| `math` | Math grade (0-100) | Yes |
| `science` | Science grade (0-100) | Yes |
| `english` | English grade (0-100) | Yes |
| `history` | History grade (0-100) | Yes |
| `attendance` | Attendance percentage | Optional |
| `study_hours` | Weekly study hours | Optional |
| `assignments_submitted` | Number of assignments submitted | Optional |
| `total_assignments` | Total number of assignments | Optional |

### Sample Data Format

```csv
student_id,name,math,science,english,history,attendance,study_hours
STU0001,Student 1,85,78,92,88,95,15
STU0002,Student 2,72,68,75,70,88,12
STU0003,Student 3,95,92,89,94,98,20
```

## 🎯 Usage

### 1. Upload Your Data
- Navigate to the "Upload Data" tab
- Click "Choose File" and select your CSV or Excel file
- Click "Upload & Analyze"
- Or use the "Load Sample Data" button to explore with demo data

### 2. View Dashboard
- See overall statistics at a glance
- Explore grade distribution charts
- Analyze performance categories

### 3. Explore Analytics
- View correlation between attendance and performance
- Analyze study hours impact
- Check top performers
- Review subject-wise distributions

### 4. Run ML Predictions
- Click "Run Predictions" to train the model
- View predicted grades for all students
- Identify at-risk students
- Filter by risk level (High/Medium/Low)

### 5. Generate Reports
- Export comprehensive Excel reports with multiple sheets
- Download professional PDF reports with visualizations
- Share insights with stakeholders

## 🏗️ Project Structure

```
student-analytics-app/
├── app.py                 # Main Flask application
├── analytics.py           # Statistical analysis module
├── ml_predictor.py        # Machine learning predictions
├── report_generator.py    # Excel/PDF report generation
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/
│   └── index.html        # Main dashboard template
├── static/
│   ├── css/
│   │   └── style.css     # Dashboard styles
│   └── js/
│       └── app.js        # Frontend JavaScript
├── uploads/              # User uploaded files
├── reports/              # Generated reports
└── temp_charts/          # Temporary chart images
```

## 🧠 Machine Learning Models

### Regression Model (Grade Prediction)
- **Algorithm**: Random Forest Regressor
- **Features**: Math, Science, English, History, Attendance, Study Hours
- **Target**: Average Grade
- **Metrics**: R² Score, RMSE

### Classification Model (Pass/Fail Prediction)
- **Algorithm**: Gradient Boosting Classifier
- **Features**: Same as regression
- **Target**: Pass (≥60) or Fail (<60)
- **Metrics**: Accuracy Score

## 📈 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard page |
| `/api/upload` | POST | Upload student data file |
| `/api/data/summary` | GET | Get summary statistics |
| `/api/data/visualizations` | GET | Get visualization data |
| `/api/predictions` | POST | Run ML predictions |
| `/api/student/<id>` | GET | Get student details |
| `/api/export/excel` | POST | Export Excel report |
| `/api/export/pdf` | POST | Export PDF report |
| `/api/data/reset` | POST | Reset to sample data |

## 🎨 Technologies Used

### Backend
- **Flask**: Web framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning models
- **SciPy**: Statistical functions
- **Openpyxl**: Excel file generation
- **ReportLab**: PDF report generation
- **Matplotlib**: Chart generation

### Frontend
- **HTML5/CSS3**: Structure and styling
- **JavaScript (ES6)**: Interactive functionality
- **Chart.js**: Data visualization
- **jQuery**: AJAX requests

## 🔧 Configuration

You can customize the application by modifying:

- `app.py`: Port, host, upload folder settings
- `ml_predictor.py`: ML model parameters, feature selection
- `analytics.py`: Statistical thresholds, categories
- `report_generator.py`: Report formatting, chart styles

## 📝 Features in Detail

### Dashboard Analytics
- **Summary Cards**: Quick overview of key metrics
- **Grade Distribution**: Histogram showing grade spread
- **Performance Categories**: Pie chart of student performance levels
- **Subject Averages**: Bar chart comparing subject performance

### Advanced Analytics
- **Correlation Analysis**: Scatter plots with correlation coefficients
- **Top Performers**: Ranked list of highest-achieving students
- **Subject Distribution**: Breakdown of performance across subjects
- **Study Patterns**: Analysis of study hours vs performance

### Predictive Models
- **Grade Forecasting**: Predict final grades based on current performance
- **Risk Assessment**: Identify students at risk of failing
- **Improvement Metrics**: Calculate points needed for passing
- **Probability Scores**: Pass/fail probability percentages

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Your Name - [vemanabhanu2528](https://github.com/vemanabhanu2528)

## 🙏 Acknowledgments

- Flask documentation and community
- Scikit-learn for ML algorithms
- Chart.js for beautiful visualizations
- The open-source community

## 📧 Contact

For questions or support, please open an issue on GitHub or contact: vemanabhanu2528@gmail.com

---

**Note**: This is a demo application for educational purposes. Always ensure you have proper authorization before analyzing student data and comply with data privacy regulations like FERPA.
