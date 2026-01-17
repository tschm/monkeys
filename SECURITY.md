# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.x.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue,
please report it responsibly.

### How to Report

1. **Do NOT open a public GitHub issue** for security vulnerabilities.

2. **Email the maintainer directly** or use GitHub's private vulnerability
   reporting feature:
   - Go to the repository's Security tab
   - Click "Report a vulnerability"
   - Provide detailed information about the vulnerability

### What to Include

When reporting a vulnerability, please include:

- A description of the vulnerability
- Steps to reproduce the issue
- Potential impact assessment
- Any suggested fixes (optional)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution Target**: Within 30 days for critical issues

### What to Expect

1. We will acknowledge receipt of your report
2. We will investigate and validate the vulnerability
3. We will work on a fix and coordinate disclosure timing
4. We will credit you in the security advisory (unless you prefer anonymity)

## Security Measures

This project implements the following security practices:

### Static Analysis

- **Ruff with Bandit rules (S)**: Automated security vulnerability detection
- **CodeQL scanning**: Weekly security analysis via GitHub Actions
- **Pre-commit hooks**: Validate code before commits

### Dependency Management

- **Renovate**: Automated dependency updates
- **Dependabot alerts**: GitHub security alerts for vulnerable dependencies
- **Lock files**: Reproducible builds with `uv.lock`

### Code Review

- All changes require pull request review
- CI/CD must pass before merging
- Security-sensitive changes receive additional scrutiny

## Known Limitations

This is a simulation/demonstration project and should not be used for:

- Actual financial trading decisions
- Production financial systems
- Handling sensitive financial data

The random portfolio simulations are for educational and research purposes only.
