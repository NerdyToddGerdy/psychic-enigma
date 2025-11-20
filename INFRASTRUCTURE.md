# Infrastructure Documentation

This document describes the infrastructure setup for the RPG Hex Grid Game, including configuration management, logging, containerization, and CI/CD pipelines.

## Table of Contents

1. [Environment Configuration](#environment-configuration)
2. [Logging Framework](#logging-framework)
3. [Docker Containerization](#docker-containerization)
4. [CI/CD Pipeline](#cicd-pipeline)
5. [Development Workflow](#development-workflow)
6. [Production Deployment](#production-deployment)

---

## Environment Configuration

The application uses environment variables for configuration management, allowing for different settings across development, staging, and production environments.

### Configuration Files

- **`.env`**: Environment-specific configuration (NOT committed to git)
- **`.env.example`**: Template for creating your `.env` file
- **`config.py`**: Configuration loader that reads from environment variables

### Setup

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your settings:**
   ```bash
   # Server Configuration
   FLASK_ENV=development
   FLASK_DEBUG=True
   HOST=127.0.0.1
   PORT=5000

   # Security
   SECRET_KEY=your-secret-key-here

   # CORS Configuration
   CORS_ORIGINS=*

   # Logging
   LOG_LEVEL=INFO
   LOG_FILE=logs/rpg_game.log
   ```

### Configuration Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_ENV` | Environment (development/production) | `development` | No |
| `FLASK_DEBUG` | Enable debug mode | `True` | No |
| `HOST` | Server host address | `127.0.0.1` | No |
| `PORT` | Server port | `5000` | No |
| `SECRET_KEY` | Flask secret key for sessions | Auto-generated | Yes (production) |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `*` | No |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | `INFO` | No |
| `LOG_FILE` | Log file path | `logs/rpg_game.log` | No |
| `LOG_MAX_BYTES` | Max log file size before rotation | `10485760` (10MB) | No |
| `LOG_BACKUP_COUNT` | Number of backup log files to keep | `5` | No |

---

## Logging Framework

The application uses Python's built-in `logging` module with both file and console output.

### Features

- **Rotating File Handler**: Logs rotate when they reach 10MB by default
- **Console Handler**: Real-time log output to console
- **Structured Logging**: Timestamps, log levels, and module names
- **Configurable Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL

### Log Locations

- **File Logs**: `logs/rpg_game.log` (configurable via `LOG_FILE`)
- **Console**: stdout/stderr

### Usage in Code

```python
from logging_config import get_logger

logger = get_logger(__name__)

# Log messages at different levels
logger.debug("Detailed debugging information")
logger.info("General informational message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical error message")
```

### Log Format

```
2025-11-19 10:30:45 - module_name - INFO - Message here
```

---

## Docker Containerization

The application is fully containerized using Docker for consistent deployment across environments.

### Files

- **`Dockerfile`**: Multi-stage build definition
- **`docker-compose.yml`**: Orchestration configuration
- **`.dockerignore`**: Files excluded from Docker build

### Quick Start with Docker

#### Option 1: Docker Compose (Recommended)

```bash
# Start the application
docker-compose up

# Start in detached mode
docker-compose up -d

# Stop the application
docker-compose down

# View logs
docker-compose logs -f

# Rebuild after code changes
docker-compose up --build
```

#### Option 2: Docker CLI

```bash
# Build the image
docker build -t rpg-hex-grid-game .

# Run the container
docker run -p 5000:5000 \
  -v $(pwd)/saves:/app/saves \
  -v $(pwd)/saved_characters:/app/saved_characters \
  -v $(pwd)/logs:/app/logs \
  --env-file .env \
  rpg-hex-grid-game

# Run in detached mode
docker run -d -p 5000:5000 \
  -v $(pwd)/saves:/app/saves \
  -v $(pwd)/saved_characters:/app/saved_characters \
  -v $(pwd)/logs:/app/logs \
  --env-file .env \
  --name rpg-game \
  rpg-hex-grid-game
```

### Docker Features

- **Health Checks**: Automatic container health monitoring
- **Volume Mounts**: Persistent game saves and logs
- **Multi-stage Build**: Optimized image size
- **Environment Variables**: Configuration via `.env` file

### Volumes

The following directories are mounted for persistence:

- `./saves` → `/app/saves` (game saves)
- `./saved_characters` → `/app/saved_characters` (character saves)
- `./logs` → `/app/logs` (application logs)

---

## CI/CD Pipeline

GitHub Actions is configured to automatically test, lint, and build the application on every push and pull request.

### Workflow File

`.github/workflows/ci.yml`

### Pipeline Jobs

#### 1. Test Job

- **Matrix Testing**: Python 3.10 and 3.11
- **Caching**: pip dependencies cached for faster builds
- **Test Execution**: Runs all unit tests in `tests/` directory

#### 2. Lint Job

- **Black**: Code formatting checks
- **Flake8**: Python linting (syntax errors, style violations)
- **Continue on Error**: Warnings don't fail the build

#### 3. Docker Job

- **Build**: Creates Docker image
- **Layer Caching**: Uses GitHub Actions cache for faster builds
- **Health Check**: Validates container starts correctly

#### 4. Security Job

- **Safety**: Scans dependencies for known vulnerabilities
- **Bandit**: Analyzes code for security issues

### Viewing Pipeline Results

1. Navigate to your repository on GitHub
2. Click the "Actions" tab
3. Select the workflow run to view details

### Local Testing Before Push

```bash
# Run tests
python -m unittest discover tests -v

# Check formatting
black --check .

# Run linting
flake8 .

# Build Docker image
docker build -t rpg-game-test .
```

---

## Development Workflow

### Initial Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd rpgGame

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment file
cp .env.example .env

# 5. Run the application
python run_server.py
```

### Development with Docker

```bash
# Start development server with live reload
docker-compose up

# Uncomment volume mount in docker-compose.yml for hot reload:
# volumes:
#   - .:/app
```

### Making Changes

1. Create a feature branch
2. Make your changes
3. Run tests locally
4. Commit and push
5. Create pull request
6. CI pipeline runs automatically
7. Merge after approval

---

## Production Deployment

### Prerequisites

- Docker and Docker Compose installed
- `.env` file configured for production
- SSL/TLS certificates (if using HTTPS)

### Deployment Steps

#### 1. Prepare Environment

```bash
# Create .env file
cp .env.example .env

# Edit with production values
nano .env
```

Set production values:
```bash
FLASK_ENV=production
FLASK_DEBUG=False
HOST=0.0.0.0
PORT=5000
SECRET_KEY=<generate-random-secret-key>
CORS_ORIGINS=https://yourdomain.com
LOG_LEVEL=WARNING
```

#### 2. Deploy with Docker Compose

```bash
# Pull latest code
git pull origin main

# Build and start
docker-compose up -d --build

# Verify deployment
docker-compose ps
docker-compose logs -f
```

#### 3. Set Up Reverse Proxy (Nginx)

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 4. Enable SSL with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal is configured automatically
```

### Monitoring

```bash
# View logs
docker-compose logs -f rpg-game

# Check container status
docker-compose ps

# View resource usage
docker stats rpg-game
```

### Backup

```bash
# Backup game saves
tar -czf backup-$(date +%Y%m%d).tar.gz saves/ saved_characters/

# Automate with cron
0 2 * * * cd /path/to/rpgGame && tar -czf backups/backup-$(date +\%Y\%m\%d).tar.gz saves/ saved_characters/
```

### Updating

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose up -d --build

# Clean up old images
docker image prune -f
```

---

## Security Best Practices

### Environment Variables

- Never commit `.env` to version control
- Use strong, random `SECRET_KEY` in production
- Restrict `CORS_ORIGINS` to specific domains

### Docker

- Run containers as non-root user (future improvement)
- Keep base images updated
- Scan for vulnerabilities regularly

### Networking

- Use HTTPS in production
- Configure firewall rules
- Limit CORS to trusted origins

### Logging

- Set `LOG_LEVEL=WARNING` or `ERROR` in production
- Rotate logs to prevent disk space issues
- Monitor logs for suspicious activity

---

## Troubleshooting

### Application Won't Start

```bash
# Check logs
docker-compose logs rpg-game

# Verify configuration
cat .env

# Check port availability
lsof -i :5000
```

### Permission Issues with Volumes

```bash
# Fix ownership
sudo chown -R $(whoami):$(whoami) saves/ saved_characters/ logs/
```

### Database/Save File Corruption

```bash
# Restore from backup
tar -xzf backup-YYYYMMDD.tar.gz
```

### CI Pipeline Failures

- Check GitHub Actions logs
- Run tests locally: `python -m unittest discover tests -v`
- Verify dependencies: `pip install -r requirements.txt`

---

## Future Improvements

- [ ] Add PostgreSQL database support
- [ ] Implement Redis caching
- [ ] Set up Prometheus metrics
- [ ] Add Grafana dashboards
- [ ] Implement automated backups to cloud storage
- [ ] Add E2E tests with Playwright
- [ ] Set up staging environment
- [ ] Implement blue-green deployments
- [ ] Add API rate limiting
- [ ] Implement WebSocket support for real-time updates

---

## Support

For issues or questions:

- GitHub Issues: https://github.com/NerdyToddGerdy/psychic-enigma/issues
- Documentation: See README.md and other docs in repository