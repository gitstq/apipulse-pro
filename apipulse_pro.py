#!/usr/bin/env python3
"""
🛡️ APIPulse-Pro: 轻量级API智能监控与告警引擎
Lightweight API Intelligent Monitoring & Alerting Engine

Author: gitstq
Version: 1.0.0
License: MIT
"""

import argparse
import json
import sys
import time
import statistics
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import urllib.request
import urllib.error
import ssl


@dataclass
class APIEndpoint:
    """API endpoint configuration"""
    name: str
    url: str
    method: str = "GET"
    headers: Dict[str, str] = None
    body: Optional[str] = None
    expected_status: int = 200
    timeout: int = 30

    def __post_init__(self):
        if self.headers is None:
            self.headers = {}
        if "User-Agent" not in self.headers:
            self.headers["User-Agent"] = "APIPulse-Pro/1.0"


@dataclass
class MetricResult:
    """Single metric result"""
    timestamp: str
    endpoint: str
    status_code: int
    response_time: float
    success: bool
    error_message: Optional[str] = None


@dataclass
class HealthReport:
    """Health report for an endpoint"""
    endpoint: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    success_rate: float
    avg_response_time: float
    min_response_time: float
    max_response_time: float
    p95_response_time: float
    uptime_percentage: float
    health_status: str


class APIPulsePro:
    """APIPulse-Pro: 轻量级API智能监控与告警引擎"""

    VERSION = "1.0.0"
    BANNER = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║   🛡️  APIPulse-Pro v{version}                               ║
    ║   轻量级API智能监控与告警引擎                             ║
    ║   Lightweight API Intelligent Monitoring & Alerting      ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """

    def __init__(self, config_file: Optional[str] = None):
        self.endpoints: List[APIEndpoint] = []
        self.metrics: List[MetricResult] = []
        self.config_file = config_file
        self.alert_thresholds = {
            "response_time": 1000,
            "error_rate": 5,
            "success_rate": 95
        }
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    def load_endpoints(self, file_path: str) -> bool:
        """Load endpoints from JSON/YAML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "endpoints" in data:
                    for ep_data in data["endpoints"]:
                        ep = APIEndpoint(**ep_data)
                        self.endpoints.append(ep)
                if "alert_thresholds" in data:
                    self.alert_thresholds.update(data["alert_thresholds"])
                return True
        except Exception as e:
            print(f"❌ Failed to load endpoints: {e}")
            return False

    def add_endpoint(self, endpoint: APIEndpoint):
        """Add a single endpoint"""
        self.endpoints.append(endpoint)

    def check_endpoint(self, endpoint: APIEndpoint) -> MetricResult:
        """Check a single endpoint"""
        timestamp = datetime.now().isoformat()
        start_time = time.time()

        try:
            req = urllib.request.Request(
                endpoint.url,
                method=endpoint.method,
                headers=endpoint.headers,
                data=endpoint.body.encode('utf-8') if endpoint.body else None
            )

            with urllib.request.urlopen(
                req,
                timeout=endpoint.timeout,
                context=self.ssl_context
            ) as response:
                response_time = (time.time() - start_time) * 1000
                status_code = response.status

                return MetricResult(
                    timestamp=timestamp,
                    endpoint=endpoint.name,
                    status_code=status_code,
                    response_time=response_time,
                    success=(status_code == endpoint.expected_status),
                    error_message=None
                )

        except urllib.error.HTTPError as e:
            response_time = (time.time() - start_time) * 1000
            return MetricResult(
                timestamp=timestamp,
                endpoint=endpoint.name,
                status_code=e.code,
                response_time=response_time,
                success=(e.code == endpoint.expected_status),
                error_message=f"HTTP {e.code}: {e.reason}"
            )

        except urllib.error.URLError as e:
            response_time = (time.time() - start_time) * 1000
            return MetricResult(
                timestamp=timestamp,
                endpoint=endpoint.name,
                status_code=0,
                response_time=response_time,
                success=False,
                error_message=f"Connection Error: {str(e.reason)}"
            )

        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return MetricResult(
                timestamp=timestamp,
                endpoint=endpoint.name,
                status_code=0,
                response_time=response_time,
                success=False,
                error_message=f"Error: {str(e)}"
            )

    def check_all_endpoints(self) -> List[MetricResult]:
        """Check all configured endpoints"""
        results = []
        for endpoint in self.endpoints:
            result = self.check_endpoint(endpoint)
            results.append(result)
            self.metrics.append(result)
        return results

    def generate_health_report(self, endpoint_name: str) -> Optional[HealthReport]:
        """Generate health report for an endpoint"""
        endpoint_metrics = [m for m in self.metrics if m.endpoint == endpoint_name]

        if not endpoint_metrics:
            return None

        response_times = [m.response_time for m in endpoint_metrics]
        total_requests = len(endpoint_metrics)
        successful_requests = sum(1 for m in endpoint_metrics if m.success)
        failed_requests = total_requests - successful_requests

        if total_requests == 0:
            return None

        success_rate = (successful_requests / total_requests) * 100
        uptime = (successful_requests / total_requests) * 100

        sorted_times = sorted(response_times)
        p95_index = int(len(sorted_times) * 0.95)

        health_status = "🟢 Healthy"
        if success_rate < self.alert_thresholds["success_rate"]:
            health_status = "🔴 Critical"
        elif success_rate < 99:
            health_status = "🟡 Warning"

        if response_times:
            avg_time = statistics.mean(response_times)
            if avg_time > self.alert_thresholds["response_time"]:
                health_status = "🔴 Critical"

        return HealthReport(
            endpoint=endpoint_name,
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            success_rate=round(success_rate, 2),
            avg_response_time=round(statistics.mean(response_times), 2) if response_times else 0,
            min_response_time=round(min(response_times), 2) if response_times else 0,
            max_response_time=round(max(response_times), 2) if response_times else 0,
            p95_response_time=round(sorted_times[p95_index], 2) if sorted_times else 0,
            uptime_percentage=round(uptime, 2),
            health_status=health_status
        )

    def print_health_report(self, report: HealthReport):
        """Print health report in formatted style"""
        print(f"\n{'='*60}")
        print(f"📊 Health Report: {report.endpoint}")
        print(f"{'='*60}")
        print(f"Status: {report.health_status}")
        print(f"Total Requests: {report.total_requests}")
        print(f"Successful: {report.successful_requests} | Failed: {report.failed_requests}")
        print(f"Success Rate: {report.success_rate}%")
        print(f"Response Time (ms):")
        print(f"  - Average: {report.avg_response_time}")
        print(f"  - Min: {report.min_response_time}")
        print(f"  - Max: {report.max_response_time}")
        print(f"  - P95: {report.p95_response_time}")
        print(f"Uptime: {report.uptime_percentage}%")
        print(f"{'='*60}\n")

    def print_metrics(self, metrics: List[MetricResult]):
        """Print current metrics"""
        print(f"\n{'='*80}")
        print(f"🕐 Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        print(f"{'Endpoint':<30} {'Status':<10} {'Time(ms)':<12} {'Result':<20}")
        print(f"{'-'*80}")

        for metric in metrics:
            status_icon = "✅" if metric.success else "❌"
            status_text = f"{status_icon} {metric.status_code}" if metric.status_code > 0 else "❌ Error"
            error_text = f"({metric.error_message[:20]}...)" if metric.error_message and len(metric.error_message) > 20 else f"({metric.error_message})" if metric.error_message else ""

            print(f"{metric.endpoint:<30} {status_text:<10} {metric.response_time:<12.2f} {error_text:<20}")

        print(f"{'='*80}\n")

    def export_metrics(self, output_file: str, format_type: str = "json"):
        """Export metrics to file"""
        try:
            if format_type == "json":
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump([asdict(m) for m in self.metrics], f, indent=2, ensure_ascii=False)
            elif format_type == "csv":
                import csv
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    if self.metrics:
                        fieldnames = list(asdict(self.metrics[0]).keys())
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        for m in self.metrics:
                            writer.writerow(asdict(m))

            print(f"✅ Metrics exported to {output_file}")
            return True
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False

    def clear_metrics(self):
        """Clear all stored metrics"""
        self.metrics.clear()
        print("✅ Metrics cleared")


def interactive_setup() -> APIPulsePro:
    """Interactive setup for APIPulse-Pro"""
    print(APIPulsePro.BANNER.format(version=APIPulsePro.VERSION))

    monitor = APIPulsePro()

    print("\n📝 Interactive Setup - Add API Endpoints")
    print("-" * 50)

    while True:
        print("\nAdd a new endpoint:")
        name = input("  Name (e.g., MyAPI): ").strip()
        if not name:
            print("⚠️  Name is required")
            continue

        url = input("  URL (e.g., https://api.example.com/health): ").strip()
        if not url:
            print("⚠️  URL is required")
            continue

        method = input("  Method [GET/POST/PUT/DELETE] (default: GET): ").strip().upper() or "GET"

        headers_input = input("  Headers (JSON format, e.g., {\"Authorization\": \"Bearer xxx\"}): ").strip()
        headers = {}
        if headers_input:
            try:
                headers = json.loads(headers_input)
            except:
                print("⚠️  Invalid JSON, using empty headers")
                headers = {}

        body_input = input("  Request Body (optional): ").strip()
        body = body_input if body_input else None

        expected_status = input("  Expected Status Code (default: 200): ").strip()
        expected_status = int(expected_status) if expected_status else 200

        timeout = input("  Timeout in seconds (default: 30): ").strip()
        timeout = int(timeout) if timeout else 30

        endpoint = APIEndpoint(
            name=name,
            url=url,
            method=method,
            headers=headers,
            body=body,
            expected_status=expected_status,
            timeout=timeout
        )

        monitor.add_endpoint(endpoint)

        more = input("\n➕ Add another endpoint? (y/N): ").strip().lower()
        if more != 'y':
            break

    return monitor


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="🛡️ APIPulse-Pro: 轻量级API智能监控与告警引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive setup
  %(prog)s --setup

  # Check endpoints from config file
  %(prog)s --config endpoints.json --check

  # Continuous monitoring
  %(prog)s --config endpoints.json --monitor --interval 60

  # Export metrics
  %(prog)s --export metrics.json --format json

  # View health report
  %(prog)s --health-report endpoint_name
        """
    )

    parser.add_argument('--version', '-v', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('--setup', action='store_true', help='Interactive setup mode')
    parser.add_argument('--config', '-c', type=str, help='Config file path (JSON/YAML)')
    parser.add_argument('--check', action='store_true', help='Check all endpoints once')
    parser.add_argument('--monitor', action='store_true', help='Continuous monitoring mode')
    parser.add_argument('--interval', type=int, default=60, help='Check interval in seconds (default: 60)')
    parser.add_argument('--count', type=int, default=1, help='Number of checks in monitor mode (default: infinite)')
    parser.add_argument('--export', type=str, help='Export metrics to file')
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Export format')
    parser.add_argument('--health-report', type=str, help='Generate health report for endpoint')
    parser.add_argument('--clear', action='store_true', help='Clear all stored metrics')
    parser.add_argument('--url', type=str, help='Quick check a single URL')
    parser.add_argument('--name', type=str, default='QuickCheck', help='Name for quick check')

    args = parser.parse_args()

    # Print banner
    print(APIPulsePro.BANNER.format(version=APIPulsePro.VERSION))

    # Interactive setup mode
    if args.setup:
        monitor = interactive_setup()
        print("\n✅ Setup complete! You can now use:")
        print(f"   python apipulse_pro.py --config <config_file> --check")
        return

    # Quick check mode
    if args.url:
        monitor = APIPulsePro()
        endpoint = APIEndpoint(name=args.name, url=args.url)
        monitor.add_endpoint(endpoint)
        results = monitor.check_all_endpoints()
        monitor.print_metrics(results)
        return

    # Load from config
    monitor = APIPulsePro()
    if args.config:
        if not monitor.load_endpoints(args.config):
            sys.exit(1)

    # Clear metrics
    if args.clear:
        monitor.clear_metrics()
        return

    # Health report
    if args.health_report:
        report = monitor.generate_health_report(args.health_report)
        if report:
            monitor.print_health_report(report)
        else:
            print(f"❌ No metrics found for endpoint: {args.health_report}")
        return

    # Check mode
    if args.check:
        if not monitor.endpoints:
            print("❌ No endpoints configured. Use --setup or --config to add endpoints.")
            sys.exit(1)

        results = monitor.check_all_endpoints()
        monitor.print_metrics(results)

        # Export if requested
        if args.export:
            monitor.export_metrics(args.export, args.format)

        return

    # Monitor mode
    if args.monitor:
        if not monitor.endpoints:
            print("❌ No endpoints configured. Use --setup or --config to add endpoints.")
            sys.exit(1)

        print(f"🟢 Starting continuous monitoring (interval: {args.interval}s)")
        print("Press Ctrl+C to stop\n")

        check_count = 0
        try:
            while True:
                check_count += 1
                print(f"🔄 Check #{check_count} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                results = monitor.check_all_endpoints()
                monitor.print_metrics(results)

                # Export if requested
                if args.export:
                    monitor.export_metrics(args.export, args.format)

                # Check count limit
                if args.count > 0 and check_count >= args.count:
                    print("\n✅ Monitoring completed")
                    break

                time.sleep(args.interval)

        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped by user")

        # Generate final health reports
        print("\n" + "="*80)
        print("📊 Final Health Reports")
        print("="*80)

        for endpoint in monitor.endpoints:
            report = monitor.generate_health_report(endpoint.name)
            if report:
                monitor.print_health_report(report)

        return

    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()
