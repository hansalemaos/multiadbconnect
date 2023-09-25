# Establish an ADB connection to different emulators at the same time (Bluestacks, MEmu, MuMu, LdPlayer ...) - Windows only

## Tested against Windows 10 / Python 3.11 / Anaconda

## pip install multiadbconnect

### The module is designed to facilitate the connection to Android emulators or devices using the Android Debug Bridge (ADB) tool. It offers several advantages and use cases:

#### Automated Connection to Multiple Emulators/Devices of different brands: 

The function allows you to connect to multiple emulators or devices at once 

#### Restarting ADB Server: 

It provides an option (restart_server) to restart the ADB server before connecting, 
which can help in resolving connection issues or ensuring a clean start.

#### Timeout Handling: 

You can specify a connect_timeout, which is the maximum time the function will wait 
for the connections to be established. This feature prevents the script from hanging 
indefinitely if a connection cannot be established.

#### Process Monitoring: 

The function monitors the state of the ADB connections by checking if the underlying ADB processes are alive. 
If a connection becomes unresponsive, it kills the associated process, 
ensuring reliable connections.

#### Structured Output: 

It returns a Pandas DataFrame containing information about the connected emulators/devices. 
This structured output makes it easy to work with the data, filter, and perform operations on specific devices.


```python

Args:
	adbexe (str): The path to the ADB executable.
	restart_server (bool, optional): Whether to restart the ADB server before connecting.
		Defaults to False.
	connect_timeout (Union[float, int], optional): The maximum time (in seconds) to wait for
		the connections to be established. Defaults to 15 seconds.
	alive_sleep (Union[float, int], optional): The time (in seconds) to sleep between checking
		if the ADB connections are alive. Defaults to 3 seconds.

Returns:
	pd.DataFrame: A DataFrame containing information about the connected emulators/devices.

Example:
	from multiadbconnect import connect_to_all_emulators
	df = connect_to_all_emulators(
		adbexe=r"C:\Android\android-sdk\platform-tools\adb.exe",
		restart_server=True,
		connect_timeout=15,
		alive_sleep=3,
	)

	# print(df.to_string())
	#          aa_serial                                                                               aa_details  aa_online              aa_exe                                                                                                                                             aa_cmdline  aa_pid aa_addr_ip aa_addr_port                                                                                   aa_psutil                                                   aa_adb
	# 0  127.0.0.1:21503                    device product:SM-N975F model:SM_N975F device:SM-N975F transport_id:6       True    MEmuHeadless.exe                (C:\Program Files\Microvirt\MEmuHyperv\MEmuHeadless.exe, --comment, MEmu, --startvm, 20230924-aaaa-aaaa-aaaa-000000000000, --vrde, off)   20064  127.0.0.1        21503    psutil.Process(pid=20064, name='MEmuHeadless.exe', status='running', started='23:03:52')  C:\Android\ANDROI~1\PLATFO~1\adb.exe -s 127.0.0.1:21503
	# 1   127.0.0.1:5565              device product:OnePlus5 model:ONEPLUS_A5000 device:OnePlus5 transport_id:37       True       HD-Player.exe                                                                                  (C:\Program Files\BlueStacks_nxt\HD-Player.exe, --instance, Nougat64)    7896  127.0.0.1         5565        psutil.Process(pid=7896, name='HD-Player.exe', status='running', started='23:02:33')   C:\Android\ANDROI~1\PLATFO~1\adb.exe -s 127.0.0.1:5565
	# 2    emulator-5564              device product:OnePlus5 model:ONEPLUS_A5000 device:OnePlus5 transport_id:38       True       HD-Player.exe                                                                                  (C:\Program Files\BlueStacks_nxt\HD-Player.exe, --instance, Nougat64)    7896  127.0.0.1         5565        psutil.Process(pid=7896, name='HD-Player.exe', status='running', started='23:02:33')    C:\Android\ANDROI~1\PLATFO~1\adb.exe -s emulator-5564
	# 3   127.0.0.1:7555  device product:cancro_overseas_x86_64 model:MuMu device:x86_64_overseas transport_id:10       True   Muvm6Headless.exe  (C:\PROGRA~1\MUVM6V~1\HYPERV~1\Muvm6Headless.exe, --comment, nemu-12.0-x64-overseas, --startvm, b702f309-c448-4f23-958b-6e5696ec6887, --vrde, config)   10312  127.0.0.1         7555   psutil.Process(pid=10312, name='Muvm6Headless.exe', status='running', started='19:41:34')   C:\Android\ANDROI~1\PLATFO~1\adb.exe -s 127.0.0.1:7555
	# 4   127.0.0.1:7556  device product:cancro_overseas_x86_64 model:MuMu device:x86_64_overseas transport_id:20       True   Muvm6Headless.exe  (C:\PROGRA~1\MUVM6V~1\HYPERV~1\Muvm6Headless.exe, --comment, nemu-12.0-x64-overseas, --startvm, b702f309-c448-4f23-958b-6e5696ec6887, --vrde, config)   10312  127.0.0.1         7556   psutil.Process(pid=10312, name='Muvm6Headless.exe', status='running', started='19:41:34')   C:\Android\ANDROI~1\PLATFO~1\adb.exe -s 127.0.0.1:7556
	# 5    emulator-5554                device product:SM-S908N model:SM_S908N device:star2qltechn transport_id:1       True  Ld9BoxHeadless.exe               (C:\Program Files\ldplayer9box\Ld9BoxHeadless.exe, --comment, leidian0, --startvm, 20160302-aaaa-aaaa-0eee-000000000000, --vrde, config)    4716  127.0.0.1         5555   psutil.Process(pid=4716, name='Ld9BoxHeadless.exe', status='running', started='22:41:39')    C:\Android\ANDROI~1\PLATFO~1\adb.exe -s emulator-5554
	# 6    emulator-5556                device product:SM-S901N model:SM_S901N device:star2qltechn transport_id:2       True  Ld9BoxHeadless.exe               (C:\Program Files\ldplayer9box\Ld9BoxHeadless.exe, --comment, leidian1, --startvm, 20160302-aaaa-aaaa-0eee-000000000001, --vrde, config)   13288  127.0.0.1         5557  psutil.Process(pid=13288, name='Ld9BoxHeadless.exe', status='running', started='20:46:59')    C:\Android\ANDROI~1\PLATFO~1\adb.exe -s emulator-5556
	# 7    emulator-5558                device product:SM-N976N model:SM_N976N device:star2qltechn transport_id:3       True  Ld9BoxHeadless.exe               (C:\Program Files\ldplayer9box\Ld9BoxHeadless.exe, --comment, leidian2, --startvm, 20160302-aaaa-aaaa-0eee-000000000002, --vrde, config)    6148  127.0.0.1         5559   psutil.Process(pid=6148, name='Ld9BoxHeadless.exe', status='running', started='20:47:10')    C:\Android\ANDROI~1\PLATFO~1\adb.exe -s emulator-5558
	# 8    emulator-5560                device product:SM-G970N model:SM_G970N device:star2qltechn transport_id:4       True  Ld9BoxHeadless.exe               (C:\Program Files\ldplayer9box\Ld9BoxHeadless.exe, --comment, leidian3, --startvm, 20160302-aaaa-aaaa-0eee-000000000003, --vrde, config)   17992  127.0.0.1         5561  psutil.Process(pid=17992, name='Ld9BoxHeadless.exe', status='running', started='20:47:22')    C:\Android\ANDROI~1\PLATFO~1\adb.exe -s emulator-5560

	# To send a key event to all connected devices/emulators (e.g., KEYCODE_HOME) and sleep 0.2 seconds between each command:
	df.aa_adb.apply(lambda x: x('shell input keyevent KEYCODE_HOME') if not sleep(.2) else None)

```