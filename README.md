# Idealista 18 - Valuation model

Este proyecto es un ejemplo de un modelo de valoración basado en el dataset idealista18. Para más información se pueden consultar dos artículos:

* [Artículo data in brief](https://journals.sagepub.com/doi/10.1177/23998083241242844), donde se explica como se ha construido el dataset.
* Artículo de aplicación "[Using machine learning to identify spatial market segments. A reproducible study of major Spanish markets](https://journals.sagepub.com/doi/full/10.1177/23998083231166952)", donde se aplica este dataset para integrar una aproximación de valoración basada en ML y econometría tradicional.
* [Dataset en formato csv](https://github.com/davidreyblanco/ml-training/tree/master/data/idealista18) 

## Tabla de contenidos

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Instalación

1. **Clone the repository:**
   ```
   git clone <repository_url>
   cd ml-idealista-18
   ```
2. **Create and activate a virtual environment using [uv](https://github.com/astral-sh/uv):**
    ```
    uv venv
    uv sync
    source .venv/bin/activate  # On macOS/Linux
    .\.venv\Scripts\activate   # On Windows
    ```
3. **Install required packages:**
   ```
   pip install -r requirements.txt
   ```

   uv run wandb login

## Uso

Para el registro de modelos y experimentos se ha utilizado la plataforma [Weights & Biases](https://docs.wandb.ai/guides/), en los ejemplos usados se utiliza un token como variable de entorno que debe estar en el fichero .env donde deberíamos tener algo así:

```
WANDB_API_KEY=f0d.....8sa
```

**Disclaimer:** No obstante el uso de W&B que se hace en los ejemplos y las utilidades es bastante básico.

## Contributing

Guidelines for contributing to the project.

## License

Include license details.
