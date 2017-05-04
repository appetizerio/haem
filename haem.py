import click
import sys
import subprocess
import os

ANDROID_SDK = '/opt/android/'
SDK_MANAGER = os.path.join(ANDROID_SDK, 'tools', 'bin', 'sdkmanager')
AVD_MANAGER = os.path.join(ANDROID_SDK, 'tools', 'bin', 'avdmanager')
EMULATOR = os.path.join(ANDROID_SDK, 'tools', 'emulator')
EMULATOR_CHECK = os.path.join(ANDROID_SDK, 'tools', 'emulator-check')
ADB = os.path.join(ANDROID_SDK, 'platform-tools', 'adb')

@click.group()
def cli():
    pass

@cli.command()
@click.argument('target')
@click.option('--abi', type=click.Choice(['x86', 'x86_64', 'armeabi-v7a', 'arm64-v8']), default="x86")
def install(target, abi):
    systemimg = 'system-images;%s;default;%s' % (target, abi)
    print(systemimg)
    subprocess.call([SDK_MANAGER, systemimg])

@cli.command()
@click.argument('avd')
@click.argument('target')
@click.option('--abi', type=click.Choice(['x86', 'x86_64', 'armeabi-v7a', 'arm64-v8']), default="x86")
def create(avd, target, abi):
    systemimg = 'system-images;%s;default;%s' % (target, abi)
    print(systemimg)
    subprocess.call([AVD_MANAGER, 'create', 'avd', '--name', avd, '--package', systemimg])

@cli.command()
@click.argument('avd')
def delete(avd):
    subprocess.call([AVD_MANAGER, 'delete', 'avd', '--name', avd])

@cli.command()
def list():
    subprocess.call([AVD_MANAGER, 'list', 'avd'])

@cli.command()
@click.argument('avd')
def start(avd):
    print("Execute the following command with nohup")
    cmd = "%s -avd %s -no-audio -no-window" % (EMULATOR, avd)
    print(cmd)

@cli.command()
def running():
    subprocess.call([ADB, 'devices'])

@cli.command()
@click.argument('port')
def stop(port):
    with open(os.path.join(os.path.expanduser('~'), '.emulator_console_auth_token'), 'r') as f:
        token = f.read().rstrip()
    telnet_cmd = 'auth %s\nkill\n' % (token, )
    subprocess.call('echo "%s" | telnet 127.0.0.1 %s' % (telnet_cmd, port, ), shell=True)

@cli.command()
def check():
    subprocess.call([EMULATOR_CHECK, 'accel'])


if __name__ == '__main__':
    print('Headless Android Emulator Manager (haem)')
    print('Terminology:')
    print('target - something like android-19 android-23')
    print('abi - x86 x86_64 armeabi-v7a or arm64-v8')
    print('avd - an arbitrary name for an Android Virtual Device (AVD)')
    print('port - every emulator listen on a local port, which can be inferred from its adb serialno, e.g., emulator-5444')
    cli()
