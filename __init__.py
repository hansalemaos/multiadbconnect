import os
import re
import shutil
import subprocess
from time import sleep, time
import numpy as np
import pandas as pd
import psutil
from subprocess_alive import is_process_alive
from shortpath83 import get_short_path_name
from a_pandas_ex_apply_ignore_exceptions import pd_add_apply_ignore_exceptions
from typing import Union

netstatexe = shutil.which("netstat.exe")

pd_add_apply_ignore_exceptions()
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
creationflags = subprocess.CREATE_NO_WINDOW
invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
    "start_new_session": True,
}


class ADBCommand:
    def __init__(self, adb_path, serialnumber):
        self.adb_path = adb_path
        self.serialnumber = serialnumber
        self.cmd = f"{self.adb_path} -s {self.serialnumber}"

    def __str__(self):
        return self.cmd

    def __repr__(self):
        return self.__str__()

    def __call__(self, cmd, **kwargs):
        kwargs.update(invisibledict)
        kwargs.update({"stdout": subprocess.PIPE, "stderr": subprocess.PIPE})
        return subprocess.Popen(
            f"{self.adb_path} -s {self.serialnumber} {cmd.lstrip()}", **kwargs
        )


def connect_to_all_emulators(
    adbexe: str,
    restart_server: bool = False,
    connect_timeout: Union[float, int] = 15,
    alive_sleep: Union[float, int] = 3,
):
    r"""
    Connect to all Android emulators or devices using the specified ADB executable.

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
    """
    adbexepureexe = adbexe.split(os.sep)[-1]
    adbexe = get_short_path_name(adbexe)
    if restart_server:
        subprocess.run(f"{adbexe} kill-server", shell=True, **invisibledict)
        subprocess.run(f"{adbexe} start-server", shell=True, **invisibledict)

    p = subprocess.run(
        [netstatexe, "-a", "-b", "-n", "-o", "-p", "TCP"],
        capture_output=True,
        **invisibledict,
    )

    df = pd.DataFrame(
        [
            x.decode("utf-8").strip().split()
            for x in p.stdout.splitlines()
            if b"LISTENING" in x
        ]
    )
    df.columns = ["aa_protcol", "aa_ip_and_port", "aa_local", "aa_status", "aa_pid"]
    df = df.loc[
        df["aa_ip_and_port"].str.contains(
            "(?:0.0.0.0|127.0.0.1):", regex=True, na=False
        )
    ].reset_index(drop=True)
    df["aa_output"] = df["aa_ip_and_port"].ds_apply_ignore(
        pd.NA,
        lambda x: subprocess.Popen(
            rf"{adbexe} connect {x}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            **invisibledict,
        ),
    )
    df["aa_subprocesspid"] = df["aa_output"].ds_apply_ignore(pd.NA, lambda x: x.pid)
    df["aa_subprocessalive"] = df.aa_subprocesspid.ds_apply_ignore(
        pd.NA, lambda x: is_process_alive(x)
    )
    finaltimeout = time() + connect_timeout
    while not df.loc[df.aa_subprocessalive].empty:
        df["aa_subprocessalive"] = df.aa_subprocesspid.ds_apply_ignore(
            pd.NA, lambda x: is_process_alive(x)
        )
        if time() > finaltimeout:
            break
        sleep(alive_sleep)
    df.loc[df.aa_subprocessalive].ds_apply_ignore(pd.NA, lambda x: x.kill())
    df["aa_out_stdout"] = df["aa_output"].ds_apply_ignore(
        pd.NA, lambda x: x.stdout.read()
    )
    df["aa_out_stdout"] = df["aa_out_stdout"].ds_apply_ignore(
        pd.NA, lambda x: x.decode("utf-8").strip()
    )
    df["aa_out_stderr"] = df["aa_output"].ds_apply_ignore(
        pd.NA, lambda x: x.stderr.read()
    )
    df["aa_out_stderr"] = df["aa_out_stderr"].ds_apply_ignore(
        pd.NA, lambda x: x.decode("utf-8").strip()
    )

    df = df.loc[
        df.aa_out_stdout.str.contains(
            r"^connected\s+to\s+", na=False, regex=True, flags=re.I
        )
    ]
    df.aa_pid = df.aa_pid.astype("Int64")

    df["aa_psutil"] = df.aa_pid.ds_apply_ignore(pd.NA, psutil.Process)
    df = df[["aa_ip_and_port", "aa_pid", "aa_psutil"]].reset_index(drop=True).copy()
    df["aa_parent"] = df.aa_psutil.ds_apply_ignore(pd.NA, lambda x: x.parent())
    df["aa_children"] = df.aa_psutil.ds_apply_ignore(pd.NA, lambda x: x.children())
    df["aa_cmdline"] = df["aa_psutil"].ds_apply_ignore(
        pd.NA, lambda x: tuple(x.cmdline())
    )

    p2 = subprocess.run(
        [netstatexe, "-a", "-b", "-n", "-o", "-p", "TCP"],
        capture_output=True,
        **invisibledict,
    ).stdout.decode("utf-8", "backslashreplace")

    df4 = pd.DataFrame(p2.split("\r\n ["))
    df4["aa_exefile"] = df4[0].str.extract(r"(^[^\]]+)")
    df4["aa_allconnections"] = df4[0].str.split(r"[\r\n]+", regex=True).str[1:]
    df4 = df4.explode("aa_allconnections").reset_index(drop=True)
    df4.aa_allconnections = df4.aa_allconnections.str.strip()
    df4 = df4.loc[
        df4.aa_allconnections.str.contains("^TCP", regex=True, na=False)
    ].reset_index(drop=True)
    df4 = df4.iloc[1:].reset_index(drop=True)
    df4 = df4[df4.columns[1:]].copy()
    df4 = pd.concat(
        [df4.aa_exefile, df4.aa_allconnections.str.split(n=4, expand=True)], axis=1
    )
    df4.columns = [
        "aa_exefile",
        "aa_proto",
        "aa_local_address",
        "aa_foreign_address",
        "aa_state",
        "aa_pid",
    ]
    df5 = df4.loc[df4.aa_foreign_address.isin(df4.aa_local_address)]
    dfadb = df5.loc[
        df5.aa_foreign_address.isin(
            df5.loc[df5.aa_exefile == adbexepureexe].aa_local_address
        )
    ].copy()

    subprocess.run(f"{adbexe} reconnect offline", shell=True, **invisibledict)
    dfdevices = pd.DataFrame(
        [
            g.split(maxsplit=1)
            for q in subprocess.run(
                f"{adbexe} devices -l", capture_output=True, **invisibledict
            )
            .stdout.decode("utf-8", "backslashreplace")
            .splitlines()
            if (g := q.strip())
        ]
    )
    dfdevices = dfdevices.loc[dfdevices[1].str.contains("transport_id:")].reset_index(
        drop=True
    )
    dfdevices.columns = ["aa_serial", "aa_details"]
    dfdevices["aa_online"] = dfdevices.aa_details.str.contains(
        "^offline", regex=True, na=False
    ).ds_apply_ignore(pd.NA, lambda x: not x)
    dfdevices["aa_tmp_number"] = dfdevices.aa_serial.str.split(
        "[:-]", regex=True, n=1, expand=True
    )[1].astype("Int64")

    connectiondf = []
    for pro in psutil.process_iter():
        try:
            cons = pro.connections()
            if not cons:
                continue
            n = pro.name()
            for c in cons:
                connectiondf.append([n, pro.cmdline(), pro.pid, c])

        except Exception as fe:
            pass
    dfc = pd.DataFrame(connectiondf)
    dfc.columns = ["aa_exe", "aa_cmdline", "aa_pid", "aa_connection"]
    dfc["laddr_ip"] = dfc["aa_connection"].ds_apply_ignore(pd.NA, lambda x: x.laddr.ip)
    dfc["laddr_port"] = dfc["aa_connection"].ds_apply_ignore(
        pd.NA, lambda x: x.laddr.port
    )
    dfc["raddr_ip"] = dfc["aa_connection"].ds_apply_ignore(pd.NA, lambda x: x.raddr.ip)
    dfc["raddr_port"] = dfc["aa_connection"].ds_apply_ignore(
        pd.NA, lambda x: x.raddr.port
    )
    dfc = dfc.loc[dfc.aa_pid != 0].reset_index(drop=True)
    dfexactport = dfc.loc[dfc.laddr_port.isin(dfdevices.aa_tmp_number)].copy()
    dfc = dfc.loc[np.setdiff1d(dfc.index, dfexactport.index)]
    dfdevicesnotexact = dfdevices.loc[
        ~dfdevices.aa_tmp_number.isin(dfexactport.laddr_port)
    ]
    dfnotexactport = dfc.loc[dfc.laddr_port.isin(dfdevicesnotexact.aa_tmp_number + 1)]

    dfprocs = pd.concat([dfnotexactport, dfexactport])
    dfprocs = dfprocs.dropna(subset="raddr_ip").copy()
    dfprocs.aa_cmdline = dfprocs.aa_cmdline.apply(tuple)
    dfprocs = dfprocs.drop_duplicates(
        subset=["aa_cmdline", "aa_pid", "laddr_port"]
    ).copy()

    dfdevices1exact = dfdevices.loc[
        dfdevices.aa_tmp_number.isin(dfprocs.laddr_port)
    ].copy()
    dfdevices1exact["tmp_joiner"] = dfdevices1exact.aa_tmp_number.copy()
    dfdevices2notexact = dfdevices.loc[
        ~dfdevices.aa_tmp_number.isin(dfprocs.laddr_port)
    ].copy()
    dfdevices2notexact["tmp_joiner"] = dfdevices2notexact.aa_tmp_number + 1
    devicesdfjoined = pd.concat(
        [dfdevices1exact, dfdevices2notexact], ignore_index=True
    )
    dfprocs["tmp_joiner"] = dfprocs.laddr_port.copy()
    dfprocs = dfprocs.reset_index(drop=True)
    df = (
        pd.merge(devicesdfjoined, dfprocs, right_on="tmp_joiner", left_on="tmp_joiner")
        .sort_values(by="aa_online", ascending=False)
        .drop(
            columns=[
                "aa_tmp_number",
                "tmp_joiner",
                "aa_connection",
                "raddr_ip",
                "raddr_port",
            ]
        )
        .copy()
    )
    df = df.rename(columns={"laddr_ip": "aa_addr_ip", "laddr_port": "aa_addr_port"})
    df["aa_psutil"] = df.aa_pid.ds_apply_ignore(pd.NA, lambda x: psutil.Process(int(x)))

    df["aa_adb"] = df.aa_serial.ds_apply_ignore(pd.NA, lambda x: ADBCommand(adbexe, x))
    return df
