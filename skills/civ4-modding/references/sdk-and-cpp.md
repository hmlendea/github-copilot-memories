# The SDK: `CvGameCoreDLL` in C++

## When the SDK Is Required

Python and XML together cover content, interface, and reactions. Exactly three classes of change need the engine source:

1. **A new behaviour that the tables cannot express** — a rule that must be recomputed in the middle of combat, growth, or AI evaluation.
2. **A new piece of data on an existing object** — a new XML tag (which needs both a schema element and a member on the corresponding `CvInfo` class) or a new piece of state on a city, unit, or player.
3. **A performance-critical rule** — anything that must run per plot, per unit, or per turn without an interpreter boundary.

Anything else built in C++ is a fork of the engine for no gain, and a fork carries the entire compatibility burden described at the end of this file.

Modiki's *Civ4 SDK* page lists the two source trees the SDK contains:

| Tree | Contents |
|------|----------|
| `Cv*` (C++) | The engine: `CvGameCoreDLL`, `CvGame`, `CvPlayer`, `CvCity`, `CvUnit`, `CvTeam`, `CvMap`, `CvPlot`, `CvArea`, `CvSelectionGroup`, `CvDeal`, `CvInfos`, `CvEnums`, `CvGlobals`, `CvXMLLoadUtility`, `CvDLLPython`, `CvEventReporter`, and the `Cv*AI` files that hold the AI |
| `Cy*` (C++) | The Python interface layer: `CyGame`, `CyPlayer`, `CyCity`, `CyUnit`, `CyPlot`, `CyTeam`, `CyArea`, `CyGlobalContext`, `CyMessageControl`, `CyEnumsInterface`, `CyInfoInterface1–3`, `CyGameTextMgr`, `CyHallOfFameInfo`, `CyReplayInfo`, `CyArgsList`, and the `*Interface*` files that expose methods |

The AI is in `CvPlayerAI`, `CvCityAI`, `CvUnitAI`, `CvTeamAI`, `CvGameAI`, and `CvSelectionGroupAI`. `CvGameInterface` is the C++ side that calls into Python for the `CvGameUtils` answers, and `CvGameTextMgr` composes the engine's own text.

## Toolchain

Modiki's *How to Install the SDK* and the *Civ4 Useful Programs* page record the community toolchain:

- **Compiler.** Visual Studio 2008 Express is the recommended build environment; CodeBlocks is described as obsolete and unable to produce a debug DLL. The older Microsoft Platform SDK, the VC++ Toolkit 2003, and the `msvcrt.lib`, `msvcrtd.lib`, `msvcprt.lib` import libraries appear in the same instructions because older build recipes needed them.
- **Source.** The `CvGameCoreDLL` sources shipped in the BtS 3.19 SDK folder, or the community's clean dumps of the same; the file list above is the folder's own list.
- **Output.** `CvGameCoreDLL.dll`, placed in the mod folder (`Mods\<Mod>\CvGameCoreDLL.dll`) or in the install. The engine loads the mod's DLL in preference to the base one when the mod is active.
- **Debugging.** A debug build can attach to the running game; the community's `_precompile`, `FAssert`, and `FAStarNode` files exist around the debugging and pathfinding internals, and the `Database of C++ Build Errors` and `How to Resolve Some Compilation Errors` pages are the field guide.

The build is a plain `vcproj` per the SDK folder. Because the compiler is fixed at VS2008, a modern toolchain cannot produce a compatible DLL without the community's compatibility work, and that is the practical barrier to entry.

## Adding a New XML Column

This is the canonical first SDK change and it touches a fixed set of places:

1. **Schema.** Add the element to the matching `*Schema.xml` in the position it must occupy. Order matters (`references/xml-reference.md`).
2. **Info class member.** Add the member and its default to the class in `CvInfos.h`/`CvInfos.cpp`.
3. **XML read.** Add the `pXML->GetChildXmlValByName(...)` (or the list equivalent) call in that class's `read` function, in the same order as the schema.
4. **Copy constructor** and the class's other serialised operations, so the value is carried when the info is copied.
5. **Consumers.** Read the member where the behaviour is needed; until something reads it, the new tag is inert even though it loads.
6. **Exposure to Python (optional).** If Python must read the value, add an accessor to the `CvInfos` class and to the corresponding `CyInfoInterface*` file, then rebuild; a `CvInfos` accessor alone is not visible to the interpreter.

The community's `Adding New XML Values` tutorial is exactly this procedure; the *Common SDK Mistakes* page collects the ways it is done incompletely (a schema entry with no read call, a read call with no default, an accessor exposed in `CvInfos` but not in the `Cy*` layer, a value not propagated in the copy constructor).

## Exposing a Function to Python

Modiki's *Exposing New Functions to Python* and *Calling Function from a Custom Python Module in the SDK* describe the two directions:

- **C++ → Python.** `CvDLLPython` and `CvDLLPythonEvents` hold the bridge; a call is a `Cy*` method invocation or an event report through `CvEventReporter`. A new call site means adding the report and the `CvEventManager` handler together.
- **Python → C++.** Add the method to the `Cy*` class in the `Cy*Interface*` file that exposes that class's methods, rebuild the DLL, and the interpreter sees it after the mod's DLL loads. There is no reflection: the method must exist at compile time.

Because the SWIG-equivalent layer is hand-written, the interface is a fixed compile-time surface. A function whose absence is the reason for an SDK change is added here, and everything a mod adds becomes an obligation for every future merge with another DLL mod.

## Change Categories and Their Cost

| Change | Cost |
|--------|------|
| New XML column | Schema + info class + read + copy + consumer, and optionally the `Cy*` accessor |
| New rule reading existing data | Add the code in the relevant `Cv*` file; no content change needed |
| New city/unit/player state | The new member, its initialisation, its save/load, and its interface accessor |
| Modified AI | The `Cv*AI` files; the most conflict-prone area because AI mods overlap heavily |
| New `CvGameUtils` question | C++ call site + `PythonCallbackDefines` switch + the Python answer |
| Performance work | The point of the exercise, but it must be measured against the Python alternative |

**Save compatibility is explicit in C++.** A new member on a serialised class changes the save format; the class's read/write must handle an older save or the mod is incompatible with existing games — the mod's `AffectsSavedGames`-equivalent statement is a manual claim the author must make honestly.

## Compatibility Burden

- **One DLL per mod, and it must match the expansion and the patch.** A DLL built for BtS 3.19 substitutes the base DLL only in a 3.19 game; the same mod under Warlords needs a different build.
- **DLL mods do not stack.** Two mods that both ship a `CvGameCoreDLL.dll` cannot both be active. Because Civ4 has no mod stacking at all (`references/mod-packaging.md`), the practical form of this is that a DLL mod must be merged into whatever other DLL mod the player uses.
- **A merged DLL must be rebuilt by the merger.** Shipping a binary and asking another modder to merge it is not possible; the sources must be combined and recompiled.
- **AI changes conflict by definition** because every AI mod edits the same `Cv*AI` files.
- **Steam and patch updates overwrite the install's DLL**, so a mod's DLL must live in the mod folder to survive.
- **Multiplayer requires identical DLLs.** A DLL mismatch is a hard incompatibility, not a soft one.

## Working Method

1. **Exhaust XML and Python first.** Write the rule in Python with a switched-on callback, measure it, and only then move it into C++. The shipped documentation makes the same recommendation.
2. **Take the smallest diff.** Change the one function that must change; leave the rest of the engine alone, so that merging with the next DLL mod is a small operation.
3. **Rebuild and test the whole chain.** XML → Python → DLL, with logging on, because a DLL mismatch masks everything else.
4. **Record the exact expansion and patch level** in the README and the mod description, and state the save-compatibility consequence of any new serialised member.
