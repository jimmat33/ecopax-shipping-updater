git remote add origin 'https://github.com/jimmat33/ecopax-shipping-performance-reviewer.git'
git pull origin main
pause
cd ecopax-shipping-updater-code-files
.\venv\Scripts\activate
python ecopax_shipping_updater.py
deactivate