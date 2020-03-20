# totp-manager

A tool for generating time-based one-time passwords (TOTP) for services requiring multi-factor authentication (MFA), and
for encrypting/managing the underlying MFA secret keys. Basically, a command line replacement for the phone-based Google
Authenticator app.


## Requirements

* Python >=2.7


## Installing the TOTP Manager Tool

```
python setup_totp.py install
```

OR, if needed:

```
sudo python setup_totp.py install
```


## Using the TOTP Manager Tool

The TOTP Manager tool allows you to dynamically generate OTP tokens using the command line instead of a mobile device.
All MFA secret keys are stored locally in 256-bit encrypted form (in `~/.totp-encr`), and generating an OTP token
requires entering a personalized PIN.

The TOTP Manager tool consists of two Python scripts, which can be run as commands:
- `totp-encryptor` - for adding/configuring OTP token-generation for services requiring MFA.
- `totp` - for generating OTP tokens for the added MFA-enabled services.


### Setting up the Encryptor

The TOTP Manager tool relies on a JSON file with the following structure:

```
{
    "aws": {
        "description": "Amazon Web Services (name@company.com)",
        "encr_secret": "d9jhHSj892kjsBjSD34dbWD9jHSDjio923hwn12nJKH9sjkbqseh/ibHHUI90mbn"
    },
    "github": {
        "description": "GitHub (username)",
        "encr_secret": "zSDWsx4f59GtGBDed6s8hsa98H9hJSBjij0789hKLnJg8DG8h2shGf10SxD+YEGC"
    },
    ...
}
```

The `totp-encryptor` tool provides a guided interface for generating and managing this file automatically. This file
will contain one entry per service that requires MFA for access.

The entries `aws` and `github` in this example are arbitrary; you can use this tool for any service that requires MFA,
and you can name your services whatever you like, e.g. `aws-personal`, `aws-work`, `github-alice`, `gitlab-bob`, etc.

Each time your use the `totp-encryptor` tool to add a new service, you will be prompted to create and verify a PIN code.
This code is used to encrypt your MFA secret key, and will be requested each time you generate an OTP token for the
service. The PIN can contain any alpha-numeric characters, but must be at least 8 characters/digits long. You can have a
separate PIN per service, or use the same PIN for all services. If you lose your PIN, it is not recoverable.

**Note:** The `-a`/`--all` flags will only produce valid OTP tokens if the same PIN is used for all services.

When setting up a new service that requires MFA, you are normally presented with a QR code that allows you to add the
service to e.g. Google Authenticator. At this stage, retrieve the "manual configuration key" (the MFA secret key) from
the service instead, and paste it into the `totp-encryptor` tool when prompted. In AWS this can be found by clicking
`Show secret key` when configuring MFA. If you like, you can still register the service on your mobile device as well;
the TOTP mechanism permits multiple enrolled devices.


### Generating OTP Tokens

The TOTP Manager tool is run from the command line to generate OTP tokens for the services requiring MFA. To show all
available MFA-enabled services that have been registered via the `totp-encryptor` script, type:

```
totp --help
```

If an available service is e.g. `github`, generate an OTP token for this service as follows:

```
totp --github
```

The above command will prompt you for a PIN code. The output to the console will be in the following format:

```
SUCCESS (12s)
312686
```

The line indicating `SUCCESS (##s)` includes a count of the number of seconds remaining before the displayed OTP token
expires. The OTP token itself is written to `sys.stdout`, whereas the `SUCCESS (##s)` line is written to `sys.stderr`.
This allows the generated OTP token to be passed to your system clipboard (default behavior), so it can be quickly and
easily pasted wherever it is needed.

The flag `--suppress-copy` can be used to disable the default `totp` function behavior of copying the generated OTP
token to the system clipboard, since this is usually not desired when embedding `totp` into another function.

#### Embedding the functionality

The TOTP Manager tool can be used in combination with other commands and within functions. The following example shows
this usage within an AWS CLI command.

For Bash/ZSH shells:

```
aws sts assume-role --role-arn <value> \
                    --role-session-name <value> \
                    --serial-number <value> \
                    --token-code $(totp --aws --suppress-copy)
```

For fish shells:

```
aws sts assume-role --role-arn <value> \
                    --role-session-name <value> \
                    --serial-number <value> \
                    --token-code (totp --aws --suppress-copy)
```
