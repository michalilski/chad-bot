# Chad-Bot project prototype

## This repository contains a chatbot middle layer prototype.
- This project was implemented under AITech project.
- Authors: Jakub Balicki, Michał Ilski, Jan Pawłowski, Patryk Rygiel
- Affiliation: Wrocław University of Science and Technology


## Project setup
Create a `config.yaml` file similar to `example_config.yaml`

### Locally
1. Environment installation
```bash
pip install -r requirements.txt
```

### Docker
1. Build
```bash
docker compose build
```
2. Run
```bash
docker compose up -d
```

### App start
```bash
gradio app/main.py
```
