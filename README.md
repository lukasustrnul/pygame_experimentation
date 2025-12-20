# pygame_experimentation

Experimentation space for building small games and reusable helpers with [pygame](https://www.pygame.org/).

## Layout

- `pygame_experimentation/common/` — shared helpers such as configuration, scene management, and the main loop.
- `pygame_experimentation/projects/` — individual experiments and demos. Each project is its own package so it can depend on the shared helpers without leaking project-specific code.
- `requirements.txt` — dependencies for the shared virtual environment.

## Running the sandbox demo

The sandbox uses the shared helpers to demonstrate a minimal loop and scene.

```bash
python -m pygame_experimentation.projects.sandbox.main
```

Press **ESC** to quit the window.
