git remote add origin 'https://github.com/jimmat33/ecopax-shipping-updater.git'
git pull origin main

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
setx PATH "%PATH%;C:\Python310\Scripts"

cd ecopax-shipping-updater-code-files
pip install -r requirements.txt