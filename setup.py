import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='stringencrypt',

    version='1.0.0',

    description='StringEncrypt page allows you to encrypt strings and files using randomly generated algorithm, generating a unique decryption code (so called polymorphic code) each time in the selected programming language.',
    long_description=long_description,
    long_description_content_type="text/markdown",

    keywords = "encryption string file string-encryption file-encryption security cryptography",

    url='https://www.stringencrypt.com',

    author='Bartosz Wójcik',
    author_email='support@pelock.com',

    license='Apache-2.0',

    packages=['stringencrypt'],

    zip_safe=False,

    classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Natural Language :: English",
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
      ],
)