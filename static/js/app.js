// Global variables
let chartsInitialized = false;
let allPredictions = [];
let charts = {};

// Tab switching
function openTab(evt, tabName) {
    const tabContents = document.getElementsByClassName('tab-content');
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove('active');
    }
    
    const tabButtons = document.getElementsByClassName('tab-button');
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }
    
    document.getElementById(tabName).classList.add('active');
    evt.currentTarget.classList.add('active');
    
    // Load data when switching to specific tabs
    if (tabName === 'dashboard' && !chartsInitialized) {
        loadDashboard();
    } else if (tabName === 'analytics') {
        loadAnalytics();
    }
}

// Load dashboard data
function loadDashboard() {
    fetch('/api/data/summary')
        .then(response => response.json())
        .then(data => {
            updateSummaryStats(data);
            loadVisualizations();
            chartsInitialized = true;
        })
        .catch(error => console.error('Error loading dashboard:', error));
}

// Update summary statistics
function updateSummaryStats(data) {
    document.getElementById('totalStudents').textContent = data.total_students || 0;
    
    if (data.statistics && data.statistics.average_grade) {
        document.getElementById('avgGrade').textContent = 
            data.statistics.average_grade.mean.toFixed(2);
    }
    
    if (data.performance_categories) {
        const passing = data.total_students - (data.performance_categories.failing || 0);
        const passRate = ((passing / data.total_students) * 100).toFixed(1);
        document.getElementById('passRate').textContent = passRate + '%';
        document.getElementById('atRisk').textContent = data.performance_categories.failing || 0;
    }
}

// Load visualizations
function loadVisualizations() {
    fetch('/api/data/visualizations')
        .then(response => response.json())
        .then(data => {
            createGradeDistChart(data);
            createPerfCategoryChart(data);
            createSubjectAvgChart(data);
        })
        .catch(error => console.error('Error loading visualizations:', error));
}

// Create grade distribution chart
function createGradeDistChart(data) {
    const ctx = document.getElementById('gradeDistChart');
    if (charts.gradeDist) charts.gradeDist.destroy();
    
    if (data.grade_histogram) {
        const labels = data.grade_histogram.bins.slice(0, -1).map((bin, i) => 
            `${bin.toFixed(0)}-${data.grade_histogram.bins[i+1].toFixed(0)}`
        );
        
        charts.gradeDist = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Number of Students',
                    data: data.grade_histogram.counts,
                    backgroundColor: 'rgba(102, 126, 234, 0.7)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 5 }
                    }
                }
            }
        });
    }
}

// Create performance category chart
function createPerfCategoryChart(data) {
    const ctx = document.getElementById('perfCategoryChart');
    if (charts.perfCategory) charts.perfCategory.destroy();
    
    fetch('/api/data/summary')
        .then(response => response.json())
        .then(summaryData => {
            if (summaryData.performance_categories) {
                const perf = summaryData.performance_categories;
                
                charts.perfCategory = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Excellent', 'Good', 'Average', 'Below Average', 'Failing'],
                        datasets: [{
                            data: [
                                perf.excellent || 0,
                                perf.good || 0,
                                perf.average || 0,
                                perf.below_average || 0,
                                perf.failing || 0
                            ],
                            backgroundColor: [
                                '#4CAF50',
                                '#8BC34A',
                                '#FFC107',
                                '#FF9800',
                                '#F44336'
                            ]
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: true,
                        plugins: {
                            legend: {
                                position: 'bottom'
                            }
                        }
                    }
                });
            }
        });
}

// Create subject average chart
function createSubjectAvgChart(data) {
    const ctx = document.getElementById('subjectAvgChart');
    if (charts.subjectAvg) charts.subjectAvg.destroy();
    
    if (data.subject_averages) {
        const subjects = Object.keys(data.subject_averages);
        const averages = Object.values(data.subject_averages);
        
        charts.subjectAvg = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: subjects.map(s => s.charAt(0).toUpperCase() + s.slice(1)),
                datasets: [{
                    label: 'Average Score',
                    data: averages,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }
}

// Load analytics tab
function loadAnalytics() {
    fetch('/api/data/visualizations')
        .then(response => response.json())
        .then(data => {
            createAttendanceChart(data);
            createStudyHoursChart(data);
            updateTopPerformers(data);
            updateSubjectDistributions(data);
        })
        .catch(error => console.error('Error loading analytics:', error));
}

// Create attendance vs grade chart
function createAttendanceChart(data) {
    const ctx = document.getElementById('attendanceChart');
    if (charts.attendance) charts.attendance.destroy();
    
    if (data.attendance_vs_grade) {
        charts.attendance = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Students',
                    data: data.attendance_vs_grade.attendance.map((att, i) => ({
                        x: att,
                        y: data.attendance_vs_grade.grades[i]
                    })),
                    backgroundColor: 'rgba(102, 126, 234, 0.5)',
                    borderColor: 'rgba(102, 126, 234, 1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    x: {
                        title: { display: true, text: 'Attendance (%)' },
                        min: 0,
                        max: 100
                    },
                    y: {
                        title: { display: true, text: 'Average Grade' },
                        min: 0,
                        max: 100
                    }
                },
                plugins: {
                    subtitle: {
                        display: true,
                        text: `Correlation: ${data.attendance_vs_grade.correlation.toFixed(3)}`
                    }
                }
            }
        });
    }
}

// Create study hours chart
function createStudyHoursChart(data) {
    const ctx = document.getElementById('studyHoursChart');
    if (charts.studyHours) charts.studyHours.destroy();
    
    if (data.study_hours_impact) {
        charts.studyHours = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Students',
                    data: data.study_hours_impact.study_hours.map((hours, i) => ({
                        x: hours,
                        y: data.study_hours_impact.grades[i]
                    })),
                    backgroundColor: 'rgba(76, 175, 80, 0.5)',
                    borderColor: 'rgba(76, 175, 80, 1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    x: {
                        title: { display: true, text: 'Study Hours per Week' }
                    },
                    y: {
                        title: { display: true, text: 'Average Grade' },
                        min: 0,
                        max: 100
                    }
                },
                plugins: {
                    subtitle: {
                        display: true,
                        text: `Correlation: ${data.study_hours_impact.correlation.toFixed(3)}`
                    }
                }
            }
        });
    }
}

// Update top performers table
function updateTopPerformers(data) {
    const tbody = document.querySelector('#topPerformersTable tbody');
    tbody.innerHTML = '';
    
    if (data.top_performers) {
        data.top_performers.forEach((student, index) => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${student.student_id}</td>
                <td>${student.name}</td>
                <td>${student.average_grade.toFixed(2)}</td>
            `;
        });
    }
}

// Update subject distributions
function updateSubjectDistributions(data) {
    const container = document.getElementById('subjectDistributions');
    container.innerHTML = '';
    
    if (data.subject_distributions) {
        Object.entries(data.subject_distributions).forEach(([subject, dist]) => {
            const card = document.createElement('div');
            card.className = 'subject-dist-card';
            card.innerHTML = `
                <h4>${subject.charAt(0).toUpperCase() + subject.slice(1)}</h4>
                <p>Above 80%: <strong>${dist.above_80}</strong></p>
                <p>60-80%: <strong>${dist.between_60_80}</strong></p>
                <p>Below 60%: <strong>${dist.below_60}</strong></p>
            `;
            container.appendChild(card);
        });
    }
}

// Run predictions
function runPredictions() {
    const button = event.target;
    button.disabled = true;
    button.textContent = 'Running predictions...';
    
    fetch('/api/predictions', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            allPredictions = data.predictions;
            displayPredictions(allPredictions);
            
            // Update model accuracy
            const accuracyDiv = document.getElementById('modelAccuracy');
            accuracyDiv.innerHTML = `
                <strong>Model Performance:</strong><br>
                R² Score: ${data.model_accuracy.regression_r2.toFixed(3)} | 
                RMSE: ${data.model_accuracy.regression_rmse.toFixed(2)} | 
                Classification Accuracy: ${(data.model_accuracy.classification_accuracy * 100).toFixed(1)}%
            `;
            
            button.disabled = false;
            button.textContent = 'Run Predictions';
        })
        .catch(error => {
            console.error('Error running predictions:', error);
            button.disabled = false;
            button.textContent = 'Run Predictions';
        });
}

// Display predictions
function displayPredictions(predictions) {
    const tbody = document.querySelector('#predictionsTable tbody');
    tbody.innerHTML = '';
    
    predictions.forEach(pred => {
        const row = tbody.insertRow();
        const riskClass = `risk-${pred.risk_level.toLowerCase()}`;
        
        row.innerHTML = `
            <td>${pred.student_id}</td>
            <td>${pred.name}</td>
            <td>${pred.current_grade.toFixed(2)}</td>
            <td>${pred.predicted_grade.toFixed(2)}</td>
            <td>${(pred.pass_probability * 100).toFixed(1)}%</td>
            <td><span class="${riskClass}">${pred.risk_level}</span></td>
            <td>${pred.improvement_needed.toFixed(2)}</td>
        `;
    });
}

// Filter predictions
function filterPredictions() {
    const filter = document.getElementById('riskFilter').value;
    
    if (filter === 'all') {
        displayPredictions(allPredictions);
    } else {
        const filtered = allPredictions.filter(p => p.risk_level === filter);
        displayPredictions(filtered);
    }
}

// Export to Excel
function exportExcel() {
    const button = event.target;
    button.disabled = true;
    button.textContent = 'Generating...';
    
    fetch('/api/export/excel', { method: 'POST' })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'student_analytics_report.xlsx';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();
            
            button.disabled = false;
            button.textContent = 'Download Excel Report';
        })
        .catch(error => {
            console.error('Error exporting Excel:', error);
            button.disabled = false;
            button.textContent = 'Download Excel Report';
        });
}

// Export to PDF
function exportPDF() {
    const button = event.target;
    button.disabled = true;
    button.textContent = 'Generating...';
    
    fetch('/api/export/pdf', { method: 'POST' })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'student_analytics_report.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();
            
            button.disabled = false;
            button.textContent = 'Download PDF Report';
        })
        .catch(error => {
            console.error('Error exporting PDF:', error);
            button.disabled = false;
            button.textContent = 'Download PDF Report';
        });
}

// Upload file
function uploadFile() {
    const fileInput = document.getElementById('dataFile');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    const statusDiv = document.getElementById('uploadStatus');
    statusDiv.innerHTML = 'Uploading...';
    statusDiv.className = '';
    
    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            statusDiv.innerHTML = `Error: ${data.error}`;
            statusDiv.className = 'error';
        } else {
            statusDiv.innerHTML = `Success! Loaded ${data.rows} rows with ${data.columns.length} columns.`;
            statusDiv.className = 'success';
            
            // Reset charts and reload data
            chartsInitialized = false;
            setTimeout(() => {
                loadDashboard();
            }, 1000);
        }
    })
    .catch(error => {
        statusDiv.innerHTML = `Error: ${error.message}`;
        statusDiv.className = 'error';
    });
}

// Load sample data
function loadSampleData() {
    fetch('/api/data/reset', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            chartsInitialized = false;
            loadDashboard();
        })
        .catch(error => console.error('Error loading sample data:', error));
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadDashboard();
});
