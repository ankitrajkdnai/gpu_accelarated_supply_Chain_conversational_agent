# # First install libmamba solver in base environment
# conda install -n base conda-libmamba-solver

# # Then activate our environment
# conda activate geograph

# # Now install RAPIDS with the libmamba solver
# conda install --solver=libmamba -c rapidsai -c conda-forge -c nvidia \
#     rapids=25.02 'cuda-version>=12.0,<=12.8' \
#     graphistry jupyterlab networkx nx-cugraph=25.02 dash xarray-spatial -y


# conda install --solver=libmamba -c nvidia cuda-cudart cuda-version=12



# Activate the virtual environment (replace 'geograph' with your actual venv path)
source venv/bin/activate  # For macOS/Linux
# geograph\Scripts\activate  # For Windows (if applicable)

# Install RAPIDS dependencies
pip install graphistry jupyterlab networkx dash xarray-spatial

# Install RAPIDS (RAPIDS packages are primarily built for conda, but you may need to install specific dependencies manually)
pip install cudf cugraph dask-cuda cupy

# Install NVIDIA CUDA libraries
pip install nvidia-pyindex
pip install nvidia-cuda-runtime-cu12