# 🚀 Deployment Guide

Complete guide for deploying the Student Performance Analytics Dashboard to various platforms.

## 📋 Pre-Deployment Checklist

- [ ] All dependencies in `requirements.txt`
- [ ] Environment variables configured
- [ ] Database setup (if using persistent storage)
- [ ] Security settings reviewed
- [ ] Testing completed
- [ ] Documentation updated

## 🌐 Deployment Options

### 1. Local Development

**Quick Start:**
```bash
python app.py
```
Access at: http://localhost:5000

**Production-like Local:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 2. Heroku Deployment

#### Step 1: Prepare Files

Create `Procfile`:
```
web: gunicorn app:app
```

Create `runtime.txt`:
```
python-3.11.0
```

Update `requirements.txt` to include:
```
gunicorn==21.2.0
```

#### Step 2: Deploy
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# Open app
heroku open
```

### 3. AWS EC2 Deployment

#### Step 1: Launch EC2 Instance
- Choose Ubuntu Server 22.04 LTS
- Select t2.micro (free tier)
- Configure security group (port 80, 443, 22)

#### Step 2: Connect and Setup
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx -y

# Clone repository
git clone https://github.com/yourusername/student-analytics-app.git
cd student-analytics-app

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### Step 3: Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/student-analytics
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /home/ubuntu/student-analytics-app/static;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/student-analytics /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 4: Setup Systemd Service
```bash
sudo nano /etc/systemd/system/student-analytics.service
```

Add:
```ini
[Unit]
Description=Student Analytics Dashboard
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/student-analytics-app
Environment="PATH=/home/ubuntu/student-analytics-app/venv/bin"
ExecStart=/home/ubuntu/student-analytics-app/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl start student-analytics
sudo systemctl enable student-analytics
sudo systemctl status student-analytics
```

### 4. Docker Deployment

#### Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads reports temp_charts models

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

#### Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
      - ./reports:/app/reports
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

#### Deploy:
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### 5. DigitalOcean App Platform

1. Push code to GitHub
2. Go to DigitalOcean App Platform
3. Click "Create App"
4. Select your GitHub repository
5. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn -w 4 -b 0.0.0.0:8080 app:app`
6. Deploy!

### 6. Google Cloud Platform (Cloud Run)

#### Create `Dockerfile` (same as above)

#### Deploy:
```bash
# Install gcloud CLI
gcloud init

# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/student-analytics
gcloud run deploy --image gcr.io/PROJECT-ID/student-analytics --platform managed
```

## 🔒 Production Configurations

### Environment Variables

Create `.env` file:
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
```

Load in `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
```

### Security Enhancements

1. **Add Authentication**
```python
from flask_login import LoginManager, login_required

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html')
```

2. **HTTPS/SSL**
- Use Let's Encrypt for free SSL
- Configure Nginx for HTTPS redirect

3. **CORS Configuration**
```python
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "https://yourdomain.com"}})
```

4. **Rate Limiting**
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/upload')
@limiter.limit("5 per minute")
def upload():
    pass
```

### Database Integration

For persistent storage, add PostgreSQL:

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), unique=True)
    # ... other fields
```

## 📊 Monitoring & Logging

### Application Logging
```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### Error Tracking (Sentry)
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()]
)
```

## 🔄 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/
    
    - name: Deploy to production
      run: |
        # Add deployment commands here
```

## 🧪 Testing Before Deployment

```bash
# Run with production settings
export FLASK_ENV=production
python app.py

# Test all endpoints
curl http://localhost:5000/
curl http://localhost:5000/api/data/summary
```

## 📈 Scaling Considerations

1. **Load Balancing**: Use multiple workers with Gunicorn
2. **Caching**: Implement Redis for frequently accessed data
3. **CDN**: Use CloudFlare for static assets
4. **Database**: Move to PostgreSQL for larger datasets
5. **Queue**: Use Celery for long-running ML predictions

## 🛠️ Maintenance

### Regular Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Restart service
sudo systemctl restart student-analytics
```

### Backup Strategy
```bash
# Backup database
pg_dump dbname > backup.sql

# Backup uploads folder
tar -czf uploads_backup.tar.gz uploads/
```

## 🆘 Troubleshooting

### Common Issues

**Port already in use:**
```bash
sudo lsof -i :5000
kill -9 PID
```

**Permission errors:**
```bash
sudo chown -R www-data:www-data /var/www/student-analytics
```

**Out of memory:**
- Reduce number of workers
- Optimize pandas operations
- Add swap space

## 📞 Support

For deployment issues:
1. Check application logs
2. Review Nginx/Apache logs
3. Verify firewall settings
4. Test database connection
5. Check environment variables

## ✅ Post-Deployment Checklist

- [ ] Application accessible via domain
- [ ] HTTPS working correctly
- [ ] File uploads functioning
- [ ] Reports generating successfully
- [ ] Charts displaying properly
- [ ] ML predictions working
- [ ] Monitoring setup
- [ ] Backups configured
- [ ] Error tracking active
- [ ] Documentation updated

---

**Remember:** Always test thoroughly in a staging environment before deploying to production!
