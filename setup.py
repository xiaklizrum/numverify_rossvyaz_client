import os
import setuptools

dir_path = os.path.dirname(os.path.realpath(__file__))

setuptools.setup(
    author='Oleg Shtanko',
    author_email='xiaklizrum@gmail.com',
    name='numverify_rossvyaz_client',
    version='0.1',
    description='numverify for russian phone numbers',
    url='https://github.com/xiaklizrum/numverify_rossvyaz_client',
    license='MIT',
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': [dir_path +  '/numverify_rossvyaz_client/loader/files/dump.sql']},
)
