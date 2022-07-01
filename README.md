# Explanation

Some timing comparisons as additional resources are parented to the previous object. In this case we have a resource group, a Cosmos Account, a database and a container.

Of course timing numbers are going to be machine specific as the amount of memory and CPU changes, however you will see that adding in each additional parent will add more time regardless of machine capability.

This repo was init'ed with

```shell
pulumi new azure-python
```

## Pulumi About

```shell
pulumi about
```

CLI

Version      3.35.2

Go Version   go1.17.11

Go Compiler  gc

Plugins

NAME          VERSION

azure-native  1.66.0

python        unknown

Host

OS       ubuntu

Version  20.04

Arch     x86_64

This project is written in python: executable='/usr/bin/python3' version='3.8.10'

Current Stack: cosmostest

Found no resources associated with cosmostest

Found no pending operations associated with cosmostest

Backend

Name           pulumi.com

URL            <https://app.pulumi.com/ericschild>

User           ericschild

Organizations  ericschild

Dependencies:

NAME                 VERSION

pip                  22.1.2

pkg_resources        0.0.0

pulumi-azure-native  1.66.0

setuptools           62.6.0

wheel                0.37.1

## The timing results

With lines 15, 42, 51 commented out:

```shell
time pulumi preview
```

* real    0m3.195s
* user    0m0.083s
* sys     0m0.137s

Remove the comment from line 15 leaving 42 and 51 commented:

```shell
time pulumi preview
```

* real    0m3.834s
* user    0m0.173s
* sys     0m0.053s

Remove the comment from line 42 leaving only 51 commented:

```shell
time pulumi preview
```

* real    0m23.685s
* user    0m0.173s
* sys     0m0.095s

Now remove the final comment on line 51:

```shell
time pulumi preview
```

* real    28m42.349s
* user    0m1.451s
* sys     0m0.653s

What the heck just happened.  This test was repeated twice just to confirm something else on my laptop had not gone crazy and used up all my resources.
