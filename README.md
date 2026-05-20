# 🛡️ APIPulse-Pro

> 轻量级API智能监控与告警引擎 | Lightweight API Intelligent Monitoring & Alerting Engine

[English](./README_en.md) | [繁體中文](./README_zh_TW.md) | 简体中文

---

## 🎉 项目介绍

**APIPulse-Pro** 是一款专为开发者设计的轻量级API监控与告警工具。它能够帮助您实时监控API端点的可用性、响应时间和健康状态，并在异常情况发生时及时告警。

### 🔥 核心亮点

- ⚡ **零依赖设计** - 仅使用Python标准库，无需安装额外包
- 🎯 **轻量级** - 单文件实现，体积小巧（约500行代码）
- 📊 **实时监控** - 支持连续监控模式，实时展示指标
- 🔔 **智能告警** - 支持自定义阈值，异常自动告警
- 📈 **健康报告** - 生成详细的端点健康分析报告
- 💾 **数据导出** - 支持JSON/CSV格式导出，方便分析

### 💡 解决的问题

- ✅ 手动检查API可用性繁琐耗时
- ✅ 缺少统一的API健康监控工具
- ✅ 难以追踪API响应时间变化趋势
- ✅ 无法及时发现API故障
- ✅ 缺少历史数据分析能力

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🌐 **多端点监控** | 支持同时监控多个API端点 |
| ⏱️ **响应时间测量** | 精确测量每个请求的响应时间 |
| 📊 **统计报告** | 生成平均、最小、最大、P95响应时间 |
| 🔴 **健康状态** | 智能判断端点健康状态（健康/警告/危险） |
| 📝 **历史记录** | 保存所有监控数据，支持回溯分析 |
| 💾 **数据导出** | 导出为JSON或CSV格式 |
| 🎨 **友好界面** | 彩色终端输出，一目了然 |
| ⚙️ **灵活配置** | 支持JSON配置文件 |

---

## 🚀 快速开始

### 📋 环境要求

- Python 3.6+
- 无需安装任何依赖包！

### 📥 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/apipulse-pro.git

# 进入目录
cd apipulse-pro

# 直接运行
python apipulse_pro.py --version
```

### 🎯 快速使用

#### 交互式设置（推荐新手）

```bash
python apipulse_pro.py --setup
```

#### 快速检查单个URL

```bash
python apipulse_pro.py --url https://api.github.com --name "GitHub API"
```

#### 使用配置文件监控

```bash
python apipulse_pro.py --config endpoints.json --check
python apipulse_pro.py --config endpoints.json --monitor --interval 60
```

#### 导出监控数据

```bash
python apipulse_pro.py --config endpoints.json --check --export metrics.json --format json
```

---

## 📖 配置文件格式

```json
{
  "endpoints": [
    {
      "name": "API名称",
      "url": "https://api.example.com/endpoint",
      "method": "GET",
      "headers": {},
      "body": null,
      "expected_status": 200,
      "timeout": 30
    }
  ],
  "alert_thresholds": {
    "response_time": 1000,
    "error_rate": 5,
    "success_rate": 95
  }
}
```

---

## 💡 设计思路

1. **极简主义** - 保持代码简洁，单文件实现所有功能
2. **零依赖** - 仅使用Python标准库，降低使用门槛
3. **可扩展性** - 支持配置文件，方便扩展更多端点
4. **用户友好** - 彩色终端输出，直观展示状态

---

## 📄 开源协议

本项目采用 **MIT License** 开源协议。

---

<p align="center">
  <strong>Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a></strong>
  <br>
  <sub>支持一下 ⭐ 如果这个项目对您有帮助！</sub>
</p>
