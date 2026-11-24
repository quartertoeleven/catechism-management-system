# Programing Guidelines

- Each endpoint should have it's own implementation (query / command and their handlers) in application layer.
- The controller only use `mediator` to "send the request" to their corresponding query / command handlers.