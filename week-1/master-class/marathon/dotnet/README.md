# How to run dotnet on Linux?

## Setup .NET on your Linux server

'''
    sudo yum install libunwind libicu
    curl -sSL -o dotnet.tar.gz https://go.microsoft.com/fwlink/?LinkID=809131
    sudo mkdir -p /opt/dotnet && sudo tar zxf dotnet.tar.gz -C /opt/dotnet
    sudo ln -s /opt/dotnet/dotnet /usr/bin
'''

## Setup .NET on your Mac (optional) 

    https://www.microsoft.com/net/core#macos

## Create a C# application on your Mac

'''
    mkdir hello1
    cd hello1
    dotnet new
    dotnet restore
    dotnet run
    dotnet publish
'''

