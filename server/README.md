1. Clone the repository:
```shell
git clone git@github.com:
```

2. Install hdf5, set the environment variable and install tables
```bash
brew install hdf5
export HDF5_DIR=/opt/homebrew/opt/hdf5
pip install tables
```

3. Set up a Python virtual environment and install the required packages by running the setup script:
```shell
chmod +x setup.sh
./setup.sh
```
