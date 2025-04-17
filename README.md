# TextSnap API

A powerful FastAPI-based service for image processing and text rendering with features like background removal, watermark removal, and text wrapping.

![TextSnap API](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/solelianus/textsnap-api.git
cd textsnap-api

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python -m app.main
```

The API will be available at `http://localhost:8080/api/v1`

## Features

### Core Features
- 🖼️ Image processing with text overlay
- 🎨 Background removal
- 💧 Watermark removal
- 📝 Text wrapping with custom fonts
- 🎯 SVG support
- 📤 Multiple output formats (PNG, JPEG, WebP, PDF)

### Advanced Features
- ⚡ Fast and efficient image processing
- 🔒 Rate limiting and security
- 📊 Comprehensive logging
- 🌐 CORS support
- 🔄 Font management system
- 🧩 Modular architecture

## Documentation

For detailed documentation, please visit our [documentation site](https://solelianus.github.io/textsnap-api/) or check the `docs/` directory:

- [Installation Guide](docs/installation.md)
- [Configuration](docs/configuration.md)
- [Architecture](docs/architecture.md)
- [API Reference](docs/api.md)
- [Development Guide](docs/development.md)
- [Testing Guide](docs/testing.md)

## Roadmap

### v1.1.0 (Next Release)
- [ ] Batch processing support
- [ ] Custom font upload via web interface
- [ ] Image optimization options
- [ ] Advanced text effects
- [ ] Webhook notifications

### v1.2.0 (Planned)
- [ ] Docker support
- [ ] Kubernetes deployment
- [ ] Monitoring and metrics
- [ ] Rate limiting dashboard
- [ ] User authentication system

## Support

### Community Support
- [GitHub Discussions](https://github.com/solelianus/textsnap-api/discussions)
- [Discord Community](https://discord.gg/textsnap)

### Professional Support
For professional support, please contact:
- Email: support@textsnap.com
- Website: https://textsnap.com/support

### Bug Reports and Feature Requests
Please use our [GitHub Issues](https://github.com/solelianus/textsnap-api/issues) to:
- Report bugs
- Request features
- Ask questions

## Contributing

We welcome contributions! Please see our [Contributing Guide](docs/development.md#contributing) for details.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the amazing web framework
- [Pillow](https://python-pillow.org/) for image processing
- [ReportLab](https://www.reportlab.com/) for PDF generation
- All our contributors and supporters

---

Made with ❤️ by solelianus 