mkdir testFiles
mkdir receivedFiles

cd ./testFiles

# empty line
touch empty.txt

# single line
touch singleLine.txt && echo "print('hello')" > singleLine.txt

# multiple lines
touch multiLine.txt && echo "a = 1\nb = 2\bc = 3\nprint('values: ', a, b, c)\nprint(a+b+c)" > multiline.txt

# python file
touch py.py && echo "print('I hope this file works')\nprint('If it does I finished :)')" > py.py

cd ../

# starting server
python3 fileServer.py &

# starting stammerProxy.py
python3 ../stammer-proxy/stammerProxy.py
