# Security Policy

Security is a top priority for the Agentic Tool Decider. Please follow these guidelines to ensure the system remains safe and secure.

## API Key Safety
- **Never commit secrets**: Do not commit `.env` files, config files containing secrets, or hardcoded tokens to the repository.
- **Never share API keys**: Keep your `JEV_API_KEY` private. Do not share it in screenshots, logs, or issues.
- **Never log API keys**: Ensure that logging mechanisms mask or omit API keys and bearer tokens.
- **Never print API keys**: Avoid `print()` statements that might accidentally output an API key to standard out.
- **Never send keys to external services**: API keys should only be sent to their intended provider (e.g., Jev API). Do not pass them as arguments to untrusted tools.

## Data Privacy
- **Do not send unnecessary private data to Jev**: When using the `JevSelector`, only send the necessary context required to make a tool decision. Avoid sending PII (Personally Identifiable Information) or highly sensitive internal data to external APIs.

## Validation and Authorization
- **Validate provider responses**: Always validate the structure and content of responses received from external APIs (like Jev) before processing them. Use JSON schemas.
- **Tool selection is not authorization**: The Tool Decider only suggests a tool to run. It **does not** authorize the execution.
- **Selected tools still require caller-side validation and authorization**: The Agent Runtime or the system executing the tool is entirely responsible for validating tool arguments, checking permissions, and ensuring the action is safe to run on the host system.
