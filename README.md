# behave-template-generator
An NLP-powered BDD tool that uses spaCy to generate template Python Behave test.

# spaCy-Driven Behave Test Generator

An automated tool to parse Gherkin `.feature` testing structures and auto-construct Python `behave` step using natural language processing (NLP).

## Project Architecture
```text
├── features/
│   ├── steps/
│   │   └── hospital_monitor_steps.py        # Example clinical step scenarios
│   ├── hospital_monitor.feature             # Patient monitor feature definition
│   └── hospital_monitor_steps_template      # Clinical step scenarios template
├── generate_steps.py                        # spaCy structural generation parser
└── README.md                                # Documentation setup handbook
```

## Quick Start Configuration

1. Install all structural ecosystem prerequisites:
```bash
pip install behave spacy
python -m spacy download en_core_web_sm
```

2. Pass your raw `.feature` document into the custom pipeline generator to compile condensed placeholder files automatically:
```bash
python generate_steps.py features/hospital_monitor.feature
```

3. Run the valid structural tests locally to confirm validation metrics pass properly:
```bash
behave
```
