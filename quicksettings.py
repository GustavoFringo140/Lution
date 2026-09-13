from pathlib import Path
import fflags

SOBER_APP_ID = "org.vinegarhq.Sober"
SOBER_CONFIG = Path.home() / ".var/app" / SOBER_APP_ID / "config/sober/config.json"


def get_renderer():
    data, _ = fflags.load_config()
    return "OpenGL" if data.get("use_opengl") else "Vulkan"


def set_renderer(value):
    data, comments = fflags.load_config()
    data["use_opengl"] = (value == "OpenGL")
    fflags.save_config(data, comments)


def get_discord_rpc():
    data, _ = fflags.load_config()
    return data.get("discord_rpc_enabled", True)


def set_discord_rpc(enabled):
    data, comments = fflags.load_config()
    data["discord_rpc_enabled"] = bool(enabled)
    fflags.save_config(data, comments)


LIGHTING_FLAGS = {
    "DFFlagDebugRenderForceTechnologyVoxel",
    "FFlagDebugForceFutureIsBrightPhase2",
    "FFlagDebugForceFutureIsBrightPhase3",
}

LIGHTING_OPTIONS = {
    "Default": {},
    "Voxel (Phase 1)": {
        "DFFlagDebugRenderForceTechnologyVoxel": True,
        "FFlagDebugForceFutureIsBrightPhase2":   False,
        "FFlagDebugForceFutureIsBrightPhase3":   False,
    },
    "Shadowmap (Phase 2)": {
        "DFFlagDebugRenderForceTechnologyVoxel": False,
        "FFlagDebugForceFutureIsBrightPhase2":   True,
        "FFlagDebugForceFutureIsBrightPhase3":   False,
    },
    "Future (Phase 3)": {
        "DFFlagDebugRenderForceTechnologyVoxel": False,
        "FFlagDebugForceFutureIsBrightPhase2":   False,
        "FFlagDebugForceFutureIsBrightPhase3":   True,
    },
}

MSAA_FLAGS = {"FFlagDebugDisableMSAA", "FIntMSAASampleCount"}

MSAA_OPTIONS = {
    "Default": {},
    "Off":     {"FFlagDebugDisableMSAA": True},
    "x1":      {"FFlagDebugDisableMSAA": False, "FIntMSAASampleCount": 1},
    "x2":      {"FFlagDebugDisableMSAA": False, "FIntMSAASampleCount": 2},
    "x4":      {"FFlagDebugDisableMSAA": False, "FIntMSAASampleCount": 4},
}

TEXTURE_FLAGS = {"DFFlagTextureQualityOverrideEnabled", "DFIntTextureQualityOverride"}

TEXTURE_LEVELS = {
    "Default":          None,
    "Potato (Level 0)": 0,
    "Low (Level 1)":    1,
    "Medium (Level 2)": 2,
    "High (Level 3)":   3,
    "Ultra (Level 4)":  4,
}


def get_lighting():
    flags = fflags.get_fflags()
    if flags.get("DFFlagDebugRenderForceTechnologyVoxel"):
        return "Voxel (Phase 1)"
    if flags.get("FFlagDebugForceFutureIsBrightPhase2"):
        return "Shadowmap (Phase 2)"
    if flags.get("FFlagDebugForceFutureIsBrightPhase3"):
        return "Future (Phase 3)"
    return "Default"


def set_lighting(option):
    flags = fflags.get_fflags()
    for k in LIGHTING_FLAGS:
        flags.pop(k, None)
    flags.update(LIGHTING_OPTIONS.get(option, {}))
    fflags.save_fflags(flags)


def get_msaa():
    flags = fflags.get_fflags()
    if flags.get("FFlagDebugDisableMSAA"):
        return "Off"
    count = flags.get("FIntMSAASampleCount")
    return {1: "x1", 2: "x2", 4: "x4"}.get(count, "Default")


def set_msaa(option):
    flags = fflags.get_fflags()
    for k in MSAA_FLAGS:
        flags.pop(k, None)
    flags.update(MSAA_OPTIONS.get(option, {}))
    fflags.save_fflags(flags)


def get_texture():
    flags = fflags.get_fflags()
    if not flags.get("DFFlagTextureQualityOverrideEnabled"):
        return "Default"
    val = flags.get("DFIntTextureQualityOverride", -1)
    names = {0: "Potato (Level 0)", 1: "Low (Level 1)",
             2: "Medium (Level 2)", 3: "High (Level 3)", 4: "Ultra (Level 4)"}
    return names.get(val, "Default")


def set_texture(option):
    flags = fflags.get_fflags()
    for k in TEXTURE_FLAGS:
        flags.pop(k, None)
    val = TEXTURE_LEVELS.get(option)
    if val is not None:
        flags["DFFlagTextureQualityOverrideEnabled"] = True
        flags["DFIntTextureQualityOverride"] = val
    fflags.save_fflags(flags)


def get_shadows_disabled():
    return fflags.get_fflags().get("FIntRenderShadowIntensity", 75) == 0


def set_shadows_disabled(disable):
    flags = fflags.get_fflags()
    if disable:
        flags["FIntRenderShadowIntensity"] = 0
    else:
        flags.pop("FIntRenderShadowIntensity", None)
    fflags.save_fflags(flags)


def get_chat_disabled():
    val = fflags.get_fflags().get("FFlagEnableBubbleChatFromChatService", True)
    return not val


def set_chat_disabled(disable):
    flags = fflags.get_fflags()
    if disable:
        flags["FFlagEnableBubbleChatFromChatService"] = False
    else:
        flags.pop("FFlagEnableBubbleChatFromChatService", None)
    fflags.save_fflags(flags)
