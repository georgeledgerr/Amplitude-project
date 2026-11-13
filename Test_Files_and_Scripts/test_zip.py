import zipfile


if zipfile.is_zipfile("Test_Files_and_Scripts/invalid.zip"):
    print("This is a valid zip file.")
else:
    print("This is not a valid zip file.")

if zipfile.is_zipfile("Test_Files_and_Scripts/valid.zip"):
    print("This is a valid zip file.")
else:
    print("This is not a valid zip file.")