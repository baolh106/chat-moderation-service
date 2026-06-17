chat-moderation-service/
├── src/
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   └── entities.py
│   ├── use_cases/
│   │   ├── __init__.py
│   │   └── moderation.py
│   └── infrastructure/
│       ├── __init__.py
│       ├── ai/
│       │   ├── __init__.py
│       │   └── nudenet_detector.py
│       └── web/
│           ├── __init__.py
│           └── fastapi_app.py
├── requirements.txt
└── main.py