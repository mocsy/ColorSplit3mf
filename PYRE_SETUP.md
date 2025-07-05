# PyreFly Type Checker Setup

This document explains how to set up and use PyreFly type checker for the ColorSplit project.

## What is PyreFly?

PyreFly is a type checker for Python with optional IDE integration.

## Installation Using UV (Recommended)

```bash
uvx pyrefly init
uvx pyrefly check
```

See: https://pyrefly.org/en/docs/installation/

## Usage

Run type checking on the entire project:

```bash
pyrefly check
```

### Upgrading PyreFly

When upgrading PyreFly or third-party libraries, you may encounter new type errors. Here's a systematic approach:

```bash
# Step 1: Suppress errors temporarily
pyrefly check --suppress-errors

# Step 2: Run your formatter of choice
# (e.g., black, isort, etc.)

# Step 3: Remove unused ignores
pyrefly check --remove-unused-ignores
```

Repeat these steps until you achieve a clean formatting run and a clean type check.
