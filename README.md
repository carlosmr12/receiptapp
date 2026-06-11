# Receipt Management with LLM-based Text Extraction

This is a Django-based web application for uploading, parsing, and managing receipts. It uses a Large Language Model (LLM) for Optical Character Recognition (OCR) to extract details from receipt images, allows users to review and edit the extracted information, and provides data analysis and reporting features.

## How It Works

The system is composed of a Django web application and a background processing pipeline for handling receipt images.

1.  **Upload:** Users upload receipt images through the web interface.
2.  **LLM-based Extraction:** The uploaded image is processed by an OCR service (powered by a Large Language Model via OpenRouter API) to extract text and identify key information like the vendor, date, total amount, and individual line items.
3.  **Data Storage:** The extracted data is saved to a PostgreSQL database, and the original receipt image is stored in Google Cloud Storage.
4.  **Review & Edit:** Users can view the extracted receipt data, compare it with the original image, and make any necessary corrections.
5.  **Dashboard & Reports:** The application provides a dashboard to visualize spending patterns and generate reports from the receipt data.

The application is designed to be deployed as a containerized service on Google Cloud Run, with a Cloud SQL for PostgreSQL instance for the database and Google Cloud Storage for file storage.

## Dependencies

The application is built with Python and Django. Key dependencies include:

*   **Django:** Web framework
*   **Gunicorn:** WSGI HTTP Server
*   **dj-database-url:** Database URL configuration for Django
*   **django-storages & gcsfs:** For using Google Cloud Storage as a file backend
*   **psycopg2-binary:** PostgreSQL adapter for Python
*   **Pillow:** Image processing library
*   **OpenAI:** For interacting with LLM services via OpenRouter.
*   **Plotly:** For generating charts and visualizations

For a complete list of dependencies, see the `requirements.txt` file.

## Local Development Setup

These instructions will guide you through setting up the project for local development using `miniforge` and `mamba`.

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd receiptapp
    ```

2.  **Create and activate the conda environment:**

    It is recommended to use `miniforge` to manage your Python environment.

    ```bash
    mamba env create -f environment.yml
    mamba activate receiptapp
    ```

    If you don't have an `environment.yml` file, you can create one with the following content:

    ```yaml
    name: receiptapp
    channels:
      - conda-forge
    dependencies:
      - python=3.12 # Or your desired python version
      - pip
      - pip:
        - -r requirements.txt
    ```

3.  **Install dependencies:**

    If you didn't use an `environment.yml` file, you can install the dependencies directly using pip:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    Create a `.env` file in the project root and add the following environment variables. For local development, you can use a local SQLite database.

    ```
    DEBUG=True
    SECRET_KEY='a-strong-secret-key-for-development'
    DATABASE_URL='sqlite:///db.sqlite3'
    OPENROUTER_API_KEY='your-openrouter-api-key'
    OPENROUTER_MODEL='your-openrouter-model'
    ```

    #### OpenRouter API Key

    This project uses [OpenRouter](https://openrouter.ai) to interact with various Large Language Models for the text extraction functionality. OpenRouter provides a unified interface to access different models from providers like OpenAI, Google, Anthropic, and more.

    To get your `OPENROUTER_API_KEY`:
    1.  Sign up for an account on [OpenRouter.ai](https://openrouter.ai).
    2.  Navigate to your account settings to generate a new API key.
    3.  Copy the key and add it to your `.env` file.

    You can also specify which model to use by setting the `OPENROUTER_MODEL` variable.

5.  **Run database migrations:**

    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    The application will be available at `http://127.0.0.1:8000`.

## Cloud Deployment

The application is configured for continuous deployment to Google Cloud Run via GitHub Actions. The workflow is defined in `.github/workflows/deploy.yml`.

### Deployment Process

1.  **Trigger:** A push to the `master` branch triggers the GitHub Actions workflow.
2.  **Authentication:** The workflow authenticates with Google Cloud using a service account key stored as a GitHub secret.
3.  **Build & Push Image:** A Docker image is built, tagged with the commit SHA, and pushed to Google Artifact Registry.
4.  **Deploy to Cloud Run:** The new container image is deployed to the Cloud Run service. The service is configured with environment variables and secrets from Google Secret Manager.
5.  **Database Migrations & Static Files:** After deployment, the workflow connects to the Cloud SQL database using the Cloud SQL Auth Proxy to run database migrations (`manage.py migrate`) and collect static files (`manage.py collectstatic`).

### Required GCP Services

*   **Cloud Run:** For running the containerized application.
*   **Cloud SQL for PostgreSQL:** As the managed database.
*   **Google Cloud Storage:** For storing uploaded receipt images and static files.
*   **Artifact Registry:** For storing Docker container images.
*   **Secret Manager:** For securely storing sensitive information like API keys and database credentials.
*   **IAM:** To manage permissions for the service account used in the deployment workflow.
