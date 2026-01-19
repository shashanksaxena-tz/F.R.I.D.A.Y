# External Integrations

## Philosophy
Each integration is a "Tool" that the Brain can select.

## Integration Interface (`friday/integrations/base.py`)

```python
class Integration:
    def get_name(self):
        return "Generic Tool"

    def get_commands(self):
        """Returns list of regex or keywords this tool handles."""
        return []

    def execute(self, command, context):
        """Performs the action."""
        pass
```

## Supported Services

### 1. News Feed (RSS)
- **Source**: Google News RSS / BBC.
- **Action**: Fetch headlines, read them out via TTS.
- **UI**: Display scrolling ticker in HUD.

### 2. Gmail / Outlook
- **Auth**: OAuth2 flow required.
- **Actions**:
    - `list_messages(limit=5)`
    - `send_message(to, subject, body)`
- **Security**: Store tokens in `secrets/tokens.json` (GitIgnored).

### 3. Microsoft Planner / Teams
- **API**: Microsoft Graph API.
- **Actions**:
    - `get_tasks()`
    - `post_channel_message()`

### 4. WhatsApp
- **API**: Twilio or Meta Business API.
- **Action**: Send alerts to user's phone.

### 5. GitHub
- **API**: GitHub REST API.
- **Actions**: List issues, Check PR status.

## Implementation Plan
1. Start with **News** (No Auth required).
2. Build the Plugin Manager to load these classes.
3. Add Gmail (Skeleton with placeholders for Client ID/Secret).
