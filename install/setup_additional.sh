# sudo systemctl start arangodb3
# sudo systemctl enable arangodb3  # to start on boot


# conda activate geograph
# pip install langchain langgraph


# # Install Jupyter for development
# conda install jupyter jupyterlab



# Start and enable ArangoDB service
sudo systemctl start arangodb3
sudo systemctl enable arangodb3 # to start on boot

# Activate the virtual environment (replace 'geograph' with your actual venv path)
source venv/bin/activate  # For macOS/Linux
# geograph\Scripts\activate  # For Windows (if applicable)

# Install required packages
pip install langchain langgraph

# Install Jupyter for development
pip install jupyter jupyterlab