# ⚡ Quick Start Guide

Get up and running with the Student Performance Analytics Dashboard in 5 minutes!

## 🎯 Prerequisites

- Python 3.8 or higher
- pip package manager
- A modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Installation (3 Steps)

### Step 1: Clone and Navigate
```bash
git clone https://github.com/yourusername/student-analytics-app.git
cd student-analytics-app
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the App
```bash
python app.py
```

That's it! Open your browser and go to: **http://localhost:5000**

## 🎨 Using the Dashboard

### Option A: Use Sample Data (Easiest)
1. Go to the "Upload Data" tab
2. Click "Load Sample Data"
3. Explore all features with pre-loaded data!

### Option B: Upload Your Own Data
1. Prepare a CSV or Excel file with student data
2. Go to "Upload Data" tab
3. Click "Choose File" and select your file
4. Click "Upload & Analyze"

### Required Data Format
Your file should have these columns:
```
student_id, name, math, science, english, history, attendance, study_hours
```

Example:
```csv
student_id,name,math,science,english,history,attendance,study_hours
STU001,John Doe,85,78,92,88,95,15
STU002,Jane Smith,72,68,75,70,88,12
```

## 📊 Explore Features

### 1. Dashboard Tab
- View summary statistics
- See grade distribution charts
- Analyze performance categories

### 2. Analytics Tab
- Explore attendance vs performance correlation
- Analyze study hours impact
- View top performers
- Check subject-wise distributions

### 3. ML Predictions Tab
- Click "Run Predictions"
- View predicted grades for all students
- Identify at-risk students
- Filter by risk level

### 4. Reports Tab
- Download Excel reports with detailed analytics
- Generate PDF reports with visualizations
- Share insights with stakeholders

## 🔧 Troubleshooting

### "Module not found" error?
```bash
pip install -r requirements.txt --upgrade
```

### Port 5000 already in use?
Edit `app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Changed to 8000
```

### Charts not displaying?
- Clear browser cache
- Try a different browser
- Check browser console for errors

## 💡 Tips

- **Sample Data**: Perfect for testing all features without your own data
- **Predictions**: Run them after loading data to see ML capabilities
- **Reports**: Great for presentations and sharing insights
- **Risk Levels**: High-risk students need immediate attention

## 📱 Next Steps

1. ✅ Explore the dashboard with sample data
2. ✅ Upload your own student data
3. ✅ Run ML predictions
4. ✅ Generate and download reports
5. ✅ Customize the app for your needs

## 🆘 Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Review [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Open an issue on GitHub for bugs or questions

## 🎉 You're All Set!

Enjoy using the Student Performance Analytics Dashboard!

---

**Pro Tip**: Start with the sample data to understand all features, then upload your real data for actual analysis.
