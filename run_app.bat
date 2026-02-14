@echo off
echo Starting Scriptoria...
:: Fix for OpenBLAS Memory Allocation Errors
SET OPENBLAS_NUM_THREADS=1
SET OMP_NUM_THREADS=1
py -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0
pause
