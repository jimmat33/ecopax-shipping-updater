git remote add origin 'https://github.com/jimmat33/ecopax-shipping-updater.git'
git pull origin main
cd ecopax-shipping-updater-code-files
pause
.\venv\Scripts\activate
pause
python ecopax_shipping_updater.py
pause
deactivate
pause