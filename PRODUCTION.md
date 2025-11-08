# Production Deployment Guide

## Table of Contents
1. [Pre-Production Checklist](#pre-production-checklist)
2. [Deployment Architecture](#deployment-architecture)
3. [Security Hardening](#security-hardening)
4. [Performance Optimization](#performance-optimization)
5. [Monitoring and Logging](#monitoring-and-logging)
6. [Backup and Recovery](#backup-and-recovery)
7. [Scaling](#scaling)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Pre-Production Checklist

### Code Quality
- [ ] All tests passing (`pytest --cov`)
- [ ] Code style compliant (`black`, `flake8`, `mypy`)
- [ ] No security vulnerabilities found
- [ ] All dependencies pinned to specific versions
- [ ] No hardcoded secrets in codebase
- [ ] Error handling comprehensive
- [ ] Logging configured at all levels

### Infrastructure
- [ ] Server provisioned and configured
- [ ] SSL/TLS certificates installed
- [ ] Firewall rules configured
- [ ] Database initialized
- [ ] Backup system configured
- [ ] Monitoring tools installed
- [ ] Log aggregation configured

### Configuration
- [ ] Environment variables documented
- [ ] All configuration parameterized
- [ ] API keys rotated and verified
- [ ] Rate limits configured
- [ ] Timeouts set appropriately
- [ ] Retry policies configured

### Testing
- [ ] Unit tests: >80% coverage
- [ ] Integration tests passing
- [ ] Load testing completed
- [ ] Security testing completed
- [ ] Disaster recovery tested
- [ ] Failover tested

---

## Deployment Architecture

### Recommended Setup

```
┌─────────────────────────────────────┐
│         Load Balancer               │
│    (nginx, HAProxy, or cloud LB)    │
└────────────┬────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼───────┐   ┌────▼──────┐
│ autoMate  │   │ autoMate   │
│ Instance1 │   │ Instance2  │
└───┬───────┘   └────┬──────┘
    │                │
    │         ┌──────▼──────┐
    └────┬────┤  Shared DB  │
         │    │  (SQLite or │
         │    │   PostgreSQL)
    ┌────▼────────────────┐
    │  Cache Layer        │
    │  (Redis/Memcached)  │
    └─────────────────────┘
```

### Deployment Options

#### Option 1: Docker Container
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 7888

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:7888/health')"

# Run application
CMD ["python", "main.py"]
```

#### Option 2: Systemd Service
```ini
[Unit]
Description=autoMate Service
After=network.target

[Service]
Type=simple
User=automate
WorkingDirectory=/opt/automate
ExecStart=/usr/bin/python3.12 main.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

#### Option 3: Cloud Deployment
- **AWS**: EC2 + RDS + CloudWatch
- **GCP**: Cloud Run + Firestore + Cloud Logging
- **Azure**: App Service + Cosmos DB + Application Insights

---

## Security Hardening

### API Key Management
```python
from gradio_ui.utils.security import get_security_manager

security = get_security_manager()

# Store hashed API keys
api_key_hash = security.hash_api_key(api_key)

# Mask keys in logs
masked_key = security.mask_api_key(api_key)

# Validate format
if security.validate_api_key_format(api_key):
    store_key(api_key)
```

### Input Validation
```python
from gradio_ui.utils.validation import Validator, InputSanitizer

# Validate inputs
Validator.validate_string(input_text, min_length=1, max_length=1000)
Validator.validate_model_config(config)

# Sanitize inputs
safe_input = InputSanitizer.sanitize_string(input_text)
safe_path = InputSanitizer.sanitize_path(file_path)
```

### Rate Limiting
```python
from gradio_ui.utils.security import get_security_manager

security = get_security_manager()

# Check rate limit before processing
if not security.check_rate_limit(user_id, max_requests=100, window_seconds=60):
    raise RateLimitError("Too many requests")
```

### Access Control
```python
from gradio_ui.utils.security import AccessControl

access_control = AccessControl()

# Setup roles
access_control.create_role("admin", ["read", "write", "delete", "admin"])
access_control.create_role("user", ["read", "write"])
access_control.create_role("viewer", ["read"])

# Check permissions
if access_control.has_permission(user_role, "delete"):
    perform_deletion()
```

### Environment Security
```bash
# Use environment variables for secrets
export ANTHROPIC_API_KEY="sk-ant-..."
export DATABASE_URL="postgresql://..."

# Never commit .env files
echo ".env" >> .gitignore
echo "secrets/" >> .gitignore

# Restrict file permissions
chmod 600 ~/.automate/config
chmod 700 ~/.automate/
```

---

## Performance Optimization

### Caching Strategy
```python
from gradio_ui.utils.caching import cache_result, get_memory_cache, get_disk_cache

# Cache function results
@cache_result(ttl_seconds=300)
def expensive_operation(param):
    return perform_expensive_operation(param)

# Use caching in code
cache = get_memory_cache()
cache.set("key", value, ttl_seconds=600)
value = cache.get("key")

# Check cache stats
stats = cache.get_stats()
print(f"Cache hit rate: {stats['hit_rate']:.2%}")
```

### Database Optimization
```sql
-- Create indexes for frequently queried columns
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);

-- Vacuum database regularly
VACUUM ANALYZE;

-- Monitor query performance
EXPLAIN ANALYZE SELECT * FROM tasks WHERE status = 'completed';
```

### Async Operations
```python
import asyncio

# Parallel task execution
async def run_parallel_tasks():
    results = await asyncio.gather(
        vision_agent.analyze(screenshot1),
        vision_agent.analyze(screenshot2),
        vision_agent.analyze(screenshot3),
    )
    return results
```

### Resource Limits
```python
# Set memory limits
import resource

# Limit to 4GB
resource.setrlimit(resource.RLIMIT_AS, (4 * 1024 * 1024 * 1024, -1))

# Set timeout for operations
from gradio_ui.utils.error_handler import with_timeout

@with_timeout(timeout_seconds=30)
async def time_limited_operation():
    pass
```

---

## Monitoring and Logging

### Logging Setup
```python
from gradio_ui.utils.logger import setup_logging, create_task_logger

# Setup application logging
logger = setup_logging(
    name="automate",
    level="INFO",
    log_file=True,
    log_console=True,
)

# Create task-specific logger
task_logger = create_task_logger("task_123")
task_logger.info("Task started")
```

### Metrics Collection
```python
from gradio_ui.utils.monitoring import get_performance_monitor, get_task_monitor

perf_monitor = get_performance_monitor()
task_monitor = get_task_monitor()

# Track performance
perf_monitor.start_timer("operation")
# ... do work ...
elapsed = perf_monitor.end_timer("operation", unit="ms")

# Monitor task
task = task_monitor.start_task("task_1", "Process user input")
# ... do work ...
task_monitor.record_action()
task_monitor.end_task(status="completed")

# Get statistics
stats = task_monitor.get_summary_stats()
```

### Health Checks
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": check_database(),
            "cache": check_cache(),
            "api": check_api(),
        }
    }

@app.get("/metrics")
async def metrics():
    """Metrics endpoint"""
    return get_all_metrics()
```

### Alerting
```python
import logging

class AlertHandler(logging.Handler):
    """Send alerts for critical errors"""

    def emit(self, record):
        if record.levelno >= logging.CRITICAL:
            send_alert(record.getMessage())

# Add alert handler
alert_handler = AlertHandler()
logging.getLogger().addHandler(alert_handler)
```

---

## Backup and Recovery

### Database Backups
```bash
#!/bin/bash
# Backup SQLite database
BACKUP_DIR="/backups/automate"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Create backup
cp ~/.automate/tasks.db $BACKUP_DIR/tasks_$TIMESTAMP.db

# Compress backup
gzip $BACKUP_DIR/tasks_$TIMESTAMP.db

# Delete backups older than 30 days
find $BACKUP_DIR -name "*.db.gz" -mtime +30 -delete
```

### Recovery Procedure
```bash
#!/bin/bash
# Restore database from backup

BACKUP_FILE="$1"
RESTORE_PATH="~/.automate/tasks.db"

# Verify backup integrity
gunzip -t $BACKUP_FILE || exit 1

# Create temporary restore location
TEMP_PATH="/tmp/tasks_restore.db"

# Restore
gunzip -c $BACKUP_FILE > $TEMP_PATH

# Verify integrity
sqlite3 $TEMP_PATH "PRAGMA integrity_check;" || exit 1

# Restore to original location
mv $TEMP_PATH $RESTORE_PATH

echo "Database restored successfully"
```

### Configuration Backups
```bash
# Backup configuration
tar czf backups/config_$(date +%Y%m%d).tar.gz ~/.automate/

# Version control for configs
git add .env.production
git commit -m "Update production config"
```

---

## Scaling

### Horizontal Scaling
```yaml
# Kubernetes Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: automate
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: automate
        image: automate:latest
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        env:
        - name: AUTOMATE_WORKERS
          value: "4"
```

### Database Sharding
For large deployments, consider sharding by task ID or time period:

```python
def get_shard(task_id: str, num_shards: int = 4) -> int:
    """Determine which shard a task belongs to"""
    return hash(task_id) % num_shards
```

### Load Balancing
```nginx
upstream automate_backend {
    least_conn;
    server automate1:7888 weight=5;
    server automate2:7888 weight=3;
    server automate3:7888 weight=3;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://automate_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Best Practices

### Code Deployment
1. **Version Control**
   - Tag releases: `git tag -a v1.0.0 -m "Release 1.0.0"`
   - Use semantic versioning

2. **CI/CD Pipeline**
   ```yaml
   # GitHub Actions example
   name: Deploy
   on:
     push:
       branches: [main]
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v2
       - name: Run tests
         run: pytest --cov
       - name: Deploy
         run: ./deploy.sh
   ```

3. **Staging Environment**
   - Test in staging before production
   - Use same config as production
   - Test disaster recovery procedures

4. **Blue-Green Deployment**
   ```bash
   # Route traffic to blue
   nginx_config=blue

   # Deploy to green
   deploy_to_green()

   # Test green
   run_smoke_tests()

   # Switch traffic to green
   nginx_config=green

   # Keep blue as rollback
   ```

### Operational Excellence
1. **Documentation**
   - Keep runbooks updated
   - Document known issues
   - Maintain architecture diagrams

2. **Training**
   - Train ops team on procedures
   - Do regular drills
   - Review incident reports

3. **Capacity Planning**
   - Monitor growth trends
   - Plan for peak loads
   - Regular load testing

4. **Incident Response**
   - Have incident response plan
   - Define on-call rotation
   - Practice incident responses

---

## Troubleshooting

### Common Issues

#### API Timeouts
```python
# Increase timeout and add retries
from gradio_ui.utils.error_handler import RetryConfig

config = RetryConfig(
    max_retries=5,
    initial_delay=2.0,
    max_delay=60.0,
)
```

#### High Memory Usage
```bash
# Check memory usage
ps aux | grep automate | grep -v grep

# Profile memory
python -m memory_profiler main.py

# Limit memory
docker run -m 4g automate:latest
```

#### Database Locks
```python
# Configure timeout
import sqlite3
conn = sqlite3.connect("tasks.db", timeout=30)

# Vacuum database
conn.execute("VACUUM")
```

#### Slow Queries
```sql
-- Enable query logging
PRAGMA query_only = OFF;

-- Analyze query performance
EXPLAIN QUERY PLAN
SELECT * FROM tasks WHERE status = 'running';

-- Create appropriate indexes
CREATE INDEX idx_status ON tasks(status);
```

---

## Performance Targets

Set and monitor these targets:

| Metric | Target | Acceptable | Critical |
|--------|--------|-----------|----------|
| API Response Time | <100ms | <500ms | >5s |
| Task Completion Rate | >95% | >90% | <80% |
| Cache Hit Rate | >80% | >60% | <40% |
| Uptime | 99.9% | 99% | <95% |
| Error Rate | <0.1% | <1% | >5% |

---

## Conclusion

Following this guide ensures autoMate is deployed safely, securely, and reliably in production. Regular reviews and updates of these procedures are essential for maintaining system health.

For additional support, refer to:
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System design details
- [CONFIGURATION.md](./CONFIGURATION.md) - Configuration options
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) - Common issues and solutions
