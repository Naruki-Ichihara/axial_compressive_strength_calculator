# VMM-FRC Documentation

This directory contains the documentation website for VMM-FRC, built with [Docusaurus](https://docusaurus.io/).

## Development

### Prerequisites

- Node.js 20 or higher
- npm
- Python 3.11+ (for API documentation generation)
- pydoc-markdown (`pip install pydoc-markdown`)

### Installation

```bash
cd docs
npm install
```

### Local Development

```bash
npm start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### Build

```bash
npm run build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### API Documentation Generation

API documentation is automatically generated from Python docstrings using pydoc-markdown:

```bash
npm run api:generate
```

To clean generated API docs:

```bash
npm run api:clean
```

## Deployment

The documentation is automatically deployed to GitHub Pages when changes are pushed to the `main` branch. See `.github/workflows/deploy-docs.yml` for the deployment configuration.

The documentation is available at: https://naruki-ichihara.github.io/vmm-frc/
