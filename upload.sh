pip3 install -r requirements.txt
python3 setup.py bdist_wheel
twine upload dist/*
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/