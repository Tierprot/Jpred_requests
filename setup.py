from cx_Freeze import setup, Executable

setup(
    name = "JPredOnlineFetcher",
    version = "1.0",
    description = "Secondary structure prediction over internet",
    executables = [Executable("jpred_queque.py")]
)