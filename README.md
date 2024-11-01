# IDS-DRR-Automation

This repository features a suite of Selenium-based Python scripts designed to automate testing for the Intelligent Data Solution for Disaster Risk Reduction (IDS-DRR) project. These scripts facilitate comprehensive validation of the platform's functionalities, ensuring performance and reliability in supporting disaster management authorities.

## About IDS-DRR

The **Intelligent Data Solution for Disaster Risk Reduction (IDS-DRR)** is an open-source platform designed to empower state-level and district-level Disaster Management Authorities. This platform facilitates timely, data-driven decision-making, enabling authorities to prioritize the expenditure of public funds and conduct public procurement in ways that enhance long-term disaster risk reduction. It aims to protect the most vulnerable populations from the adverse effects of extreme weather events and climate change.

IDS-DRR integrates a diverse array of high-value datasets, including satellite imagery, environmental data, social and economic indicators, demographic information, infrastructure details, and loss & damage assessments. By consolidating these datasets, the platform provides critical insights that support effective disaster management strategies.

For more information, visit the project repository: [IDS-DRR GitHub Repository](https://github.com/CivicDataLab/IDS-DRR)

## Developer Setup

The project leverages [uv](https://pypi.org/project/uv/) for package and project management. Before you begin the setup process, please ensure that you have [uv](https://pypi.org/project/uv/) installed on your system. This will facilitate a smoother experience when managing the project's requirements and configurations. If you haven't installed it yet, you can do so by following the instructions provided on the uv documentation page. For more detailed information on using uv, please refer to the [uv documentation](https://pypi.org/project/uv/).

Note: Make sure to have `wkhtmltopdf` installed on your system for the report generation to work properly.

To set up the project, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd ids-drr-automation
   ```

2. **Create a Virtual Environment**:
   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   uv venv
   ```

3. **Activate the Virtual Environment**:
   - On Windows:

     ```bash
     .venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source .venv/bin/activate
     ```

4. **Install Dependencies**:
   Use `uv` to install the required dependencies listed in `pyproject.toml`.

   ```bash
   uv install
   ```

5. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add the necessary environment variables:

   ```plaintext
   HOME_URL_USERNAME=<your_username>
   HOME_URL_PASSWORD=<your_password>
   HOME_URL_4=<your_home_url>
   MEDIUM_URL=https://medium.com/
   LOCAL=false  # or true based on your setup
   REMOTE_LINK=<your_remote_link>  # if applicable
   ```

6. **Run the Script**:
   After setting up, you can run the script using:

   ```bash
   python broken_link.py
   ```

7. **Generate Reports**:
   The reports will be generated in the `reports` directory after the script execution.
