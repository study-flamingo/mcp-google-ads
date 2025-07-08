---
**Company/Developer Name:** ixigo (Le Travenues Technology Ltd.)
**Contact Person:** Joel Casimir
**Contact Email:** <jcasimirdds@dtedental.net>
**Google Ads Manager Account (MCC) ID for API Token:** 296-477-1845

## 2. Application Overview

* **Application Name:** Google Ads FastMCP
* **Application Website/URL:** <https://github.com/ixigo/mcp-google-ads>
* **Brief Description:**
    Our application, "Google Ads MCP," is a backend server that connects the Google Ads API to Large Language Model (LLM) assistants like Anthropic's Claude and the Cursor AI code editor. It allows advertising professionals and developers to query, analyze, and understand their Google Ads data using natural language prompts within a chat interface, abstracting away the complexity of the Google Ads UI and GAQL.

* **Target Audience:**
    Our target audience consists of digital marketing professionals, data analysts, and developers who use AI assistants for productivity. They use our tool to quickly retrieve performance metrics, analyze campaign effectiveness, and integrate advertising data into their development workflows without leaving their primary work environment (chat or code editor).

* **Value Proposition:**
    Our tool's primary value is providing a powerful, conversational interface to the Google Ads API. Users can ask complex analytical questions in plain English (e.g., "Which of my campaigns had the best CTR last week?") and receive immediate, formatted answers. This significantly lowers the barrier to entry for data analysis, saves time by eliminating the need to navigate the Google Ads UI for routine checks, and enables novel workflows by integrating ad data directly into AI-powered code editors.

## 3. Google Ads API Usage

* **OAuth 2.0 Scopes:** We will be using the `https://www.googleapis.com/auth/adwords` scope.
  * **Justification:** While this is a read/write scope, our application's current implementation is **strictly read-only**. We request this scope to provide a complete solution for users, with the potential to add opt-in write capabilities (like pausing campaigns) in the future based on user demand. All current tools only fetch data.

* **API Services and Functionality:**
    Our application exclusively uses read-only services to provide reporting and analytics. We do **not** perform any write operations (mutates).

  * **`GoogleAdsService (Search/SearchStream)` (Read-only):** This is the core service used by nearly all of our tools (`run_gaql`, `get_campaign_performance`, `get_ad_performance`, `get_ad_creatives`, `analyze_image_assets`, etc.). We use it to execute GAQL queries to retrieve performance metrics (impressions, clicks, cost, conversions), entity attributes (names, statuses, IDs), and asset details. This data powers all the analytical capabilities of our tool.
  * **`CustomerService (listAccessibleCustomers)` (Read-only):** This service is used by our `list_accounts` tool. It allows the user to see all the Google Ads accounts they have access to with their authenticated credentials, so they can select the correct `customer_id` for subsequent queries.

## 4. Data Flow and Storage

* **Data Retrieved from API:**
    We retrieve various entity and metric fields based on the user's request. Common fields include: `customer.id`, `customer.currency_code`, `campaign.id`, `campaign.name`, `campaign.status`, `ad_group.name`, `ad_group_ad.ad.id`, `ad_group_ad.ad.name`, `ad_group_ad.ad.responsive_search_ad.headlines`, `asset.id`, `asset.name`, `asset.image_asset.full_size.url`, and metrics such as `metrics.clicks`, `metrics.impressions`, `metrics.cost_micros`, `metrics.conversions`, and `metrics.ctr`.

* **Data Storage and Security:**
  * **Storage:** Our application is a stateless server designed to be run on the user's local machine or private infrastructure. **It does not have a central database and does not store any Google Ads performance or entity data.** Data is fetched from the API, held in memory for the duration of a single request, formatted, and immediately returned to the user's client (the LLM assistant).
  * **Security:** The only piece of information persisted is the user's OAuth 2.0 refresh token, which is stored in a `google_ads_token.json` file on the user's local filesystem, giving them full control. For Service Account authentication, the key file is also managed directly by the user. All communication with the Google Ads API is encrypted in transit via TLS. The developer of the tool (ixigo) never has access to user credentials or their advertising data.
  * **Data Retention:** No Google Ads data is retained by our application. It is processed in-memory and discarded after each API call.

## 5. User Interface (UI) Mockups

Our application does not have a traditional graphical user interface (GUI). It serves as a backend toolset for LLM assistants. The user interacts with the tool via a chat interface. Below are mockups of typical interactions.

### Interaction 1: Listing Accounts and Checking Performance

**Description:** The user first lists their accounts and then asks for a performance report for a specific account. The tool returns a formatted text table directly in the chat.

```text
USER PROMPT:
list my google ads accounts

TOOL EXECUTION & RESPONSE:
> Calling tool "list_accounts"...
< Accessible Google Ads Accounts:
< --------------------------------------------------
< Account ID: 1234567890
< Account ID: 9876543210

USER PROMPT:
show me the campaign performance for account 1234567890 for the last 30 days

TOOL EXECUTION & RESPONSE:
> Calling tool "get_campaign_performance" with customer_id="1234567890" and days=30...
< Query Results for Account 1234567890:
< --------------------------------------------------------------------------------
< campaign.name      | campaign.status | metrics.clicks | metrics.cost_micros
< --------------------------------------------------------------------------------
< Brand Campaign     | ENABLED         | 1,502          | 25000000
< Non-Brand Search   | ENABLED         | 850            | 45000000
< Display Retargeting| PAUSED          | 301            | 12000000
```

## 6. System Architecture

* **Architecture Diagram:**
    The diagram below illustrates how a user interacts with our tool through an LLM assistant.

    ```
    +-------------+       +-----------------+       +-----------------+       +------------------+
    |  End User   | <---> |  LLM Assistant  | <---> | Google Ads FastMCP  | <---> | Google Ads API   |
    | (in Claude/ |       | (Claude/Cursor) |       | (Python Server) |       +------------------+
    |   Cursor)   |       +-----------------+       +-----------------+
    +-------------+
    ```

* **Description of Data Flow:**
    1. The end-user runs the Python MCP server on their local machine or a private server.
    2. For OAuth 2.0, the user is directed through the standard Google consent flow in their browser to authorize the application. The resulting refresh token is stored in a local `google_ads_token.json` file. For Service Accounts, the user provides a path to their key file.
    3. The user interacts with their LLM Assistant (e.g., Claude).
    4. The LLM interprets the user's prompt and determines that a Google Ads tool is needed.
    5. The LLM makes a local request to the Google Ads MCP server, calling a specific tool (e.g., `get_campaign_performance`).
    6. Our server uses the stored credentials to make a secure, authenticated API call to the appropriate Google Ads API endpoint.
    7. The Google Ads API returns the requested data.
    8. Our server formats the data into a human-readable text string (e.g., a table).
    9. The formatted string is sent back to the LLM, which presents it to the user in the chat interface, often with additional AI-driven analysis or summarization.

## 7. Policy Compliance

* **Required Minimum Functionality (RMF):**
    "Our tool is a **Reporting-Only** tool that fully complies with Google's RMF policy. It provides comprehensive reporting functionality through a suite of tools that allow users to retrieve performance data for campaigns, ad groups, ads, and keywords. Users can specify custom date ranges and receive detailed, formatted reports. The tool provides significant added value by offering a natural language interface for complex data retrieval and analysis, empowering non-technical users to query their ad performance without writing GAQL or navigating the Google Ads UI."

* **Data Privacy and Security:**
    "We are deeply committed to user data privacy and security. Our application is designed to be run entirely within the user's own environment (local machine or private server). **The developers of the tool (ixigo) never have access to, transmit, or store any user credentials or Google Ads data.** The tool is stateless and does not retain any advertising data after a request is complete. Our data handling practices are transparently detailed in our public GitHub repository's README file, which serves as our primary documentation: <https://github.com/ixigo/mcp-google-ads/blob/main/README.md>"
