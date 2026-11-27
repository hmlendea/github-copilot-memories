# DLL Modding

DLL modding is version-coupled. The historical guide uses Visual Studio 2019 or Mono, a Class Library targeting at least .NET Framework 4, Unity 2019.4 LTS, and assemblies from the game's `OldWorld_Data/Managed/` directory, including `UnityEngine.dll`, `UnityEngine.CoreModule`, `UnityEngine.UI.dll`, and `TenCrowns.GameCore.dll`. Current game versions may differ; inspect the installed assemblies first.

The documented entry point derives from `ModEntryPointAdaptor` and overrides `Initialize()`. Compile against the exact supported API, copy the resulting DLL into the mod folder, enable the mod, and verify a visible initialisation signal and `Logs/output.txt`.

Do not distribute copied game assemblies. Do not rely on a historical method signature when the installed game has changed. Rebuild after game updates and isolate API failures from XML or asset failures.
