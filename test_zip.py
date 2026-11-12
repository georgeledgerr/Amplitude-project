import zipfile


if zipfile.is_zipfile("amplitude_data/good_test.zip"):
    print("This is a valid zip file.")
else:
    print("This is not a valid zip file.")

if zipfile.is_zipfile("amplitude_data/partial_test.zip"):
    print("This is a valid zip file.")
else:
    print("This is not a valid zip file.")