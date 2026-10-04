# API Keys Guide

## WHAT IS AN API KEY?
An API (Application Programming Interface) key is a secret string of characters that acts like a password. It allows your software to communicate with a remote service (like Jev AI) and proves that you are authorized to use that service.

## WHY DO WE NEED IT?
In this project, the Tool Decider can optionally use an external AI service to make complex decisions about which tool to use. The API key tells the external service whose account is making the request so they can track usage and apply limits.

## DO I NEED ONE?
**No, you do not need an API key to run this repository.**
By default, the project runs in Mock Mode, which is entirely local and offline. You only need an API key if you want to experiment with the advanced AI-driven `JevSelector`.

## HOW TO USE MOCK MODE
You don't have to do anything special! Mock mode is the default. If you want to be explicit, you can set an environment variable:
```bash
export DECIDER_MODE=mock
```

## HOW TO GET A JEV KEY
If you choose to use Jev AI:
1. Go to the official Jev documentation: https://www.jevai.org/docs
2. Follow their instructions to create an account.
3. Generate a new API key. The key for this project is a **Bearer token** obtained from their `/agent/keys` endpoint.

## HOW TO STORE IT LOCALLY
Never put your API key directly into the Python code. Instead, use environment variables.

On Linux/macOS:
```bash
export JEV_API_KEY="your_actual_api_key_here"
export DECIDER_MODE=jev
```

On Windows (Command Prompt):
```cmd
set JEV_API_KEY=your_actual_api_key_here
set DECIDER_MODE=jev
```

On Windows (PowerShell):
```powershell
$env:JEV_API_KEY="your_actual_api_key_here"
$env:DECIDER_MODE="jev"
```

## HOW TO TEST IT
Once the environment variables are set, you can run the application or specific tests designed for Jev mode. The `JevClient` will automatically pick up the `JEV_API_KEY` from your environment.

## HOW TO REMOVE IT
When you are done testing, you can clear the environment variable so it isn't accidentally used later.

On Linux/macOS: `unset JEV_API_KEY`
On Windows: `set JEV_API_KEY=` or `$env:JEV_API_KEY=""`

## HOW TO AVOID LEAKING IT
- **Never** commit your API key to Git.
- **Never** paste your API key in GitHub issues, Discord, or public forums.
- **Never** print the API key in your code logs or standard output.
- Add `.env` to your `.gitignore` file so you don't accidentally commit local environment files.
