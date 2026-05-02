# Watchtower Test Fixes

⚠️ **WARNING: This repository contains intentionally vulnerable code for testing purposes.**

**DO NOT use this code in production!**

## Purpose

This repository is designed to test Watchtower's AI-powered vulnerability remediation system. It contains:

1. **CVE Vulnerabilities** - Old package versions with known security issues
2. **Hardcoded Secrets** - Example credentials that should be environment variables
3. **Code Quality Issues** - SQL injection, command injection, path traversal

## Testing Instructions

1. Scan this repository with Watchtower
2. Click "PR Ready" to trigger AI remediation
3. Review the generated pull request
4. Verify fixes are correct and tests pass

## Vulnerabilities Included

### CVEs (Package Vulnerabilities)
- `requests==2.25.0` - CVE-2023-32681 (fixed in 2.31.0)
- `flask==1.1.1` - CVE-2023-30861 (fixed in 2.3.2)
- `pillow==8.0.0` - CVE-2023-44271 (fixed in 10.0.0)
- `pyyaml==5.3.0` - CVE-2020-14343 (fixed in 5.4)

### Secrets
- Hardcoded AWS credentials
- Hardcoded database passwords
- Hardcoded API keys

### Code Quality
- SQL Injection vulnerability
- Command Injection vulnerability
- Path Traversal vulnerability

---

**Created for:** Watchtower AI Remediation Testing
**Last Updated:** 2026-05-02
