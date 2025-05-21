# Social Mantra AI - Full Documentation

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [API Integration](#api-integration)
6. [Web Interface (React)](#web-interface-react)
7. [Core Modules](#core-modules)
8. [Advanced Features](#advanced-features)
9. [Security Practices](#security-practices)
10. [Contributing](#contributing)
11. [Acknowledgements](#acknowledgements)

## Overview

This is an AI-powered automation tool for creating, publishing, and analyzing short-form videos for social media platforms. The application integrates with various AI services for content generation, voice synthesis, and video creation, while providing a user-friendly interface through React for managing the entire workflow.

## System Architecture

The application follows a modular architecture organized into distinct functional components:

```
social-mantra-ai/
├── analytics/              # Analytics and performance tracking
├── assets/                 # Static assets like music
├── backend/                # FastAPI backend
│   ├── api/                # API endpoints
│   ├── models/             # Data models
│   └── main.py             # API server entry point
├── config/                 # Configuration files
├── data/                   # Stored data and results
├── frontend/               # React frontend
│   ├── public/             # Static files
│   ├── src/                # React source code
│   │   ├── components/     # UI components
│   │   ├── pages/          # Application pages
│   │   └── utils/          # Frontend utilities
│   ├── package.json        # Frontend dependencies
│   └── README.md           # Frontend documentation
├── generation/             # Content generation
├── research/               # Trend research
├── uploads/                # Platform uploaders
├── utils/                  # Utility functions
├── .env                    # Environment variables
├── .env.example            # Environment template
├── .gitignore              # Git ignore file
├── main.py                 # CLI entry point
├── README.md               # Project overview
└── requirements.txt        # Python dependencies
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn
- Git

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/social-mantra-ai.git
   cd social-mantra-ai
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit the .env file with your API keys and configurations
   ```

5. Start the application:
   - For the API backend:
     ```bash
     cd backend
     uvicorn main:app --reload
     ```
   - For the React frontend:
     ```bash
     cd frontend
     npm start
     ```

## Web Interface (React)

The application provides a user-friendly web interface built with React.

### Front-end Architecture

The frontend application is structured using modern React practices:

- Component-based architecture
- React Router for navigation
- Context API for state management
- Material UI for consistent styling

### Key Features

- Responsive design that works on desktop and mobile
- Dark/light theme support
- Multi-step workflows with progress tracking
- Real-time analytics visualization
- API integration with error handling

The application uses React context for managing user data and workflow progression.

## Core Modules

1. **Research**: Analyzes trending content and topics across platforms
2. **Generation**: Creates content ideas, metadata, audio, and videos
3. **Uploads**: Handles content distribution to social media platforms
4. **Analytics**: Tracks performance and provides optimization suggestions
5. **UI**: Provides a user-friendly interface for the application

## Advanced Features

### Predictive Performance Modeling

The application uses machine learning models to predict the performance of generated content.

### A/B Testing

The application allows for A/B testing of different content variations to determine the most effective approach.

### Competitive Analysis

The application provides insights into the performance of competitors' content.

## Security Practices

### API Key Management

API keys are stored securely in environment variables.

### Data Encryption

Sensitive data is encrypted using industry-standard encryption algorithms.

### Regular Security Audits

The application undergoes regular security audits to identify and address potential vulnerabilities.

## Contributing

Contributions to the project are welcome! Here's how to contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please follow coding standards and include tests for new functionality.

## Acknowledgements

- Thanks to the open-source community for providing excellent tools and libraries
- Special thanks to the React team for their excellent framework
