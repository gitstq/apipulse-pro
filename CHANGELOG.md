# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-05-20

### 🎉 Added

- Initial release
- Multi-endpoint API monitoring
- Response time measurement (ms precision)
- Health report generation
- Statistics (avg, min, max, P95 response times)
- Health status indicators (🟢 Healthy, 🟡 Warning, 🔴 Critical)
- Historical metrics storage
- JSON and CSV export
- Interactive setup mode
- Configuration file support
- Custom HTTP headers and request body support
- SSL certificate verification bypass
- Command-line interface with multiple modes
- Docker support example
- Kubernetes CronJob example
- Comprehensive documentation (EN, ZH-CN, ZH-TW)
- Zero dependencies design
- Unit tests

### ⚡ Features

- `--setup`: Interactive setup mode
- `--check`: Single check mode
- `--monitor`: Continuous monitoring mode
- `--export`: Export metrics to file
- `--health-report`: Generate health report
- `--url`: Quick single URL check
- `--clear`: Clear stored metrics

### 🛠️ Technical Details

- Language: Python 3.6+
- Dependencies: None (stdlib only)
- Lines of Code: ~500
- License: MIT
