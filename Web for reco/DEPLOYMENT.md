# Deployment Guide for Render

This guide will help you deploy your Crop and Fertilizer Recommendation System to **Render.com**, a free and easy-to-use cloud platform.

## Prerequisites

1.  **GitHub Account**: You need a GitHub account to host your code.
2.  **Render Account**: Sign up at [dashboard.render.com](https://dashboard.render.com/).

## Step 1: Push Code to GitHub

1.  **Initialize Git** (if not already done):
    Open your terminal in the `d:/FEAT/Minor Project/Web for reco` folder and run:
    ```bash
    git init
    git add .
    git commit -m "Initial commit for deployment"
    ```
    *Note: If you are already tracking the parent directory, just commit your changes.*

2.  **Create a New Repository**:
    - Go to [GitHub.com](https://github.com/new).
    - Create a new repository (e.g., `crop-recommendation-app`).
    - **Do NOT** check "Initialize with README", .gitignore, or license.

3.  **Push to GitHub**:
    Copy the commands provided by GitHub (under "...or push an existing repository from the command line") and run them in your terminal. They will look like this:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/crop-recommendation-app.git
    git branch -M main
    git push -u origin main
    ```

## Step 2: Deploy on Render

1.  **New Web Service**:
    - Go to your [Render Dashboard](https://dashboard.render.com/).
    - Click **"New +"** and select **"Web Service"**.

2.  **Connect GitHub**:
    - Select "Build and deploy from a Git repository".
    - Connect your GitHub account if prompted.
    - Find your `crop-recommendation-app` repository and click **"Connect"**.

3.  **Configure Service**:
    - **Name**: Give your app a name (e.g., `crop-reco-app`).
    - **Region**: Choose the one closest to you (e.g., Singapore, Frankfurt).
    - **Branch**: `main`
    - **Root Directory**: `Web for reco` (Entering this is important if you pushed the entire 'Minor Project' folder) OR leave blank if you only pushed the 'Web for reco' folder.
    - **Runtime**: **Python 3**
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `gunicorn app:app`
    - **Free Instance**: Select the "Free" plan.

4.  **Deploy**:
    - Click **"Create Web Service"**.
    - Render will start building your app. You can watch the logs.
    - Once it says **"Live"**, click the URL at the top (e.g., `https://crop-reco-app.onrender.com`) to see your app online!

## Troubleshooting

-   **"Build failed"**: Check the logs. Did you include `requirements.txt`?
-   **"Internal Server Error"**: Check the logs. Are the `.pkl` model files in the repository? (They should be).
-   **"Application Error"**: Ensure your `Start Command` is exactly `gunicorn app:app` and you are in the correct directory.
